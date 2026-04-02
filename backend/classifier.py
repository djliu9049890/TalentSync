import json
from typing import TypedDict

from openai import OpenAI

client = OpenAI()  # assumes OPENAI_API_KEY env var

class ClassifiedPost(TypedDict):
    is_job_post: bool
    title: str
    company: str
    location: str | None
    employment_type: str
    experience_level: str
    skills: list[str]
    salary: str | None
    post_url: str | None
    hiring_contact_name: str | None
    hiring_contact_linkedin_url: str | None


EMPLOYMENT_TYPE_OPTIONS = (
    "Full-time",
    "Contract",
    "Remote",
    "Part-time",
)

EXPERIENCE_LEVEL_OPTIONS = (
    "Entry",
    "Mid-level",
    "Senior",
    "Lead",
    "Executive",
)

SYSTEM_PROMPT = """
You are a job-post classifier and extractor.

Given the text or HTML snippet of a social media post, decide if it is
advertising a specific open job and, if so, extract structured details.

If the input is HTML, use the visible post content and links as your source of
truth and ignore styling or layout markup.

Return ONLY valid JSON in this exact schema:
{
  "is_job_post": boolean,
  "title": string,
  "company": string,
  "location": string | null,
  "employment_type": "Full-time" | "Contract" | "Remote" | "Part-time",
  "experience_level": "Entry" | "Mid-level" | "Senior" | "Lead" | "Executive",
  "skills": string[],
  "salary": string | null,
  "post_url": string | null,
  "hiring_contact_name": string | null,
  "hiring_contact_linkedin_url": string | null
}

If the post is a job post, make your best judgment and always choose exactly one
employment_type and exactly one experience_level from the allowed options.
Do not return null for those two fields when is_job_post is true.
For job posts, return a list of the most relevant hard skills, tools, or
technologies mentioned or strongly implied by the post. Prefer concise canonical
skill names like "React", "Python", "SQL", "AWS", "Figma". Return up to 10.
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
        "experience_level",
        "skills",
        "salary",
        "post_url",
        "hiring_contact_name",
        "hiring_contact_linkedin_url",
    }
    missing_keys = sorted(required_keys.difference(payload.keys()))
    if missing_keys:
        raise RuntimeError(
            "OpenAI classification JSON was missing required keys: "
            f"{', '.join(missing_keys)}. Raw content: {raw_content}"
        )

    return payload  # type: ignore[return-value]


def _validate_job_post_fields(payload: ClassifiedPost, raw_content: str) -> ClassifiedPost:
    if not payload["is_job_post"]:
        return payload

    title = payload["title"]
    if not isinstance(title, str) or not title.strip():
        raise RuntimeError(
            "OpenAI classification returned an empty title for a job post. "
            f"Raw content: {raw_content}"
        )

    company = payload["company"]
    if not isinstance(company, str) or not company.strip():
        raise RuntimeError(
            "OpenAI classification returned an empty company for a job post. "
            f"Raw content: {raw_content}"
        )

    employment_type = payload["employment_type"]
    if employment_type not in EMPLOYMENT_TYPE_OPTIONS:
        raise RuntimeError(
            "OpenAI classification returned an invalid employment_type. "
            f"Expected one of {EMPLOYMENT_TYPE_OPTIONS}. Raw content: {raw_content}"
        )

    experience_level = payload["experience_level"]
    if experience_level not in EXPERIENCE_LEVEL_OPTIONS:
        raise RuntimeError(
            "OpenAI classification returned an invalid experience_level. "
            f"Expected one of {EXPERIENCE_LEVEL_OPTIONS}. Raw content: {raw_content}"
        )

    skills = payload["skills"]
    if not isinstance(skills, list):
        raise RuntimeError(
            "OpenAI classification returned a non-list skills field for a job post. "
            f"Raw content: {raw_content}"
        )

    normalized_skills = []
    seen_skills = set()
    for skill in skills:
        if not isinstance(skill, str):
            continue
        normalized_skill = skill.strip()
        if not normalized_skill:
            continue
        dedupe_key = normalized_skill.casefold()
        if dedupe_key in seen_skills:
            continue
        seen_skills.add(dedupe_key)
        normalized_skills.append(normalized_skill)

    payload["skills"] = normalized_skills[:10]

    location = payload["location"]
    if isinstance(location, str):
        normalized_locations = sorted(
            {
                part.strip()
                for part in location.split(";")
                if part.strip()
            },
            key=str.casefold,
        )
        payload["location"] = "; ".join(normalized_locations) if normalized_locations else None

    return payload


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
    validated_payload = _validate_classification_payload(payload, content)
    return _validate_job_post_fields(validated_payload, content)
