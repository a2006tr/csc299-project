import os
from typing import List

from openai import OpenAI

# Create a single OpenAI client (reads OPENAI_API_KEY from env)
client = OpenAI()


def summarize_task(description: str) -> str:
    """
    Use Chat Completions to summarize a paragraph-length task description
    into a short phrase (3–7 words).
    """
    response = client.chat.completions.create(
        # NOTE: replace this with the exact model name your instructor wants,
        # e.g. "gpt-5.1-mini" or whatever is documented for ChatGPT-5-mini.
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You summarize tasks as very short phrases, 15 words or less. "
                    "just output the bare summary."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Summarize the following task description as a very short phrase:\n\n"
                    + description
                ),
            },
        ],
        max_tokens=32,
        temperature=0.2,
    )

    # Grab the assistant's reply text
    return response.choices[0].message.content.strip()


def sample_descriptions() -> List[str]:
    """
    Two+ sample paragraph-length task descriptions.
    The program will summarize each of these when run.
    """
    return [
        (
            "Write a 5-page literature review for my communication class, "
            "synthesizing at least eight scholarly sources about how TikTok "
            "affects attention spans in young adults. I need proper APA 7th "
            "edition citations and a clear thesis that connects social media "
            "consumption with focus and academic performance."
        ),
        (
            "Plan a full-week meal prep and training schedule for a lean bulk. "
            "I want around 3,000 calories per day with 180–200 grams of protein, "
            "split across 4–5 meals that are easy to cook in bulk on Sunday. "
            "The schedule should fit around evening lifting sessions and include "
            'simple pre- and post-workout meals I can bring to the gym.'
        ),
    ]


def main() -> None:
    """
    Entry point for `uv run tasks4`.

    Loops over multiple paragraph-length descriptions, calls the OpenAI
    Chat Completions API for each one, and prints the short summaries.
    """
    # Optional: quick sanity check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set; the API call will fail.")
        print("Export your key first, e.g.:")
        print('  export OPENAI_API_KEY="sk-..."')
        # You can return here if you want to hard-stop:
        # return

    descriptions = sample_descriptions()

    for i, desc in enumerate(descriptions, start=1):
        print(f"\n=== Task {i} description ===")
        print(desc)
        print("\n--- Summary ---")
        summary = summarize_task(desc)
        print(summary)
        print("=" * 40)


if __name__ == "__main__":
    main()
