# classifier.py
from typing import TypedDict
from openai import OpenAI
import json

client = OpenAI()  # assumes OPENAI_API_KEY env var

class ClassifiedPost(TypedDict):
    is_job_post: bool
    title: str | None
    company: str | None
    location: str | None
    employment_type: str | None
    salary: str | None

SYSTEM_PROMPT = """
You are a job-post classifier and extractor.

Given the text of a social media post, decide if it is advertising
a specific open job and, if so, extract structured details.

Return ONLY valid JSON in this exact schema:
{
  "is_job_post": boolean,
  "title": string | null,
  "company": string | null,
  "location": string | null,
  "employment_type": string | null,
  "salary": string | null
}
"""

def classify_post(text: str) -> ClassifiedPost:
    completion = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        response_format={"type": "json_object"},
    )
    content = completion.output[0].content[0].text
    # `content` is JSON string matching ClassifiedPost
    return json.loads(content)