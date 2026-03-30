import json
from typing import TypedDict

from openai import OpenAI

client = OpenAI()  # assumes OPENAI_API_KEY env var

class ClassifiedPost(TypedDict):
    is_job_post: bool
    title: str | None
    company: str | None
    location: str | None
    employment_type: str | None
    salary: str | None
    post_url: str | None
    hiring_contact: str | None

SYSTEM_PROMPT = """
You are a job-post classifier and extractor.

Given the text or HTML snippet of a social media post, decide if it is
advertising a specific open job and, if so, extract structured details.

If the input is HTML, use the visible post content and links as your source of
truth and ignore styling or layout markup.

Return ONLY valid JSON in this exact schema:
{
  "is_job_post": boolean,
  "title": string | null,
  "company": string | null,
  "location": string | null,
  "employment_type": string | null,
  "salary": string | null,
  "post_url": string | null,
  "hiring_contact": string | null
}
"""


def _extract_json_object(text: str) -> dict:
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(text[start : end + 1])


def _validate_classification_payload(payload: object, raw_content: str) -> ClassifiedPost:
    if not isinstance(payload, dict):
        raise RuntimeError(
            "OpenAI classification did not return a JSON object. "
            f"Raw content: {raw_content}"
        )

    required_keys = {
        "is_job_post",
        "title",
        "company",
        "location",
        "employment_type",
        "salary",
        "post_url",
        "hiring_contact",
    }
    missing_keys = sorted(required_keys.difference(payload.keys()))
    if missing_keys:
        raise RuntimeError(
            "OpenAI classification JSON was missing required keys: "
            f"{', '.join(missing_keys)}. Raw content: {raw_content}"
        )

    return payload  # type: ignore[return-value]


def _extract_response_text(completion) -> str:
    output_text = getattr(completion, "output_text", None)
    if output_text:
        return output_text

    output = getattr(completion, "output", None) or []
    for item in output:
        content_items = getattr(item, "content", None) or []
        for content in content_items:
            text = getattr(content, "text", None)
            if text:
                return text

    return ""


def _debug_completion_summary(completion) -> str:
    try:
        return completion.model_dump_json(indent=2)[:2000]
    except Exception:
        return repr(completion)


def classify_post(text: str) -> ClassifiedPost:
    print("within classify_post")
    completion = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    content = _extract_response_text(completion)
    if not content:
        print("OpenAI completion did not include extractable text.")
        print(_debug_completion_summary(completion))
        raise RuntimeError("OpenAI completion did not include extractable text.")
    print("Content: ")
    print(content)
    # `content` is JSON string matching ClassifiedPost
    payload = _extract_json_object(content)
    return _validate_classification_payload(payload, content)
