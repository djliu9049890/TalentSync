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


def classify_post(text: str) -> ClassifiedPost:
    completion = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    content = completion.output[0].content[0].text
    print(content)
    # `content` is JSON string matching ClassifiedPost
    return _extract_json_object(content)
