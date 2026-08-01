import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise SystemExit(
        "OPENROUTER_API_KEY is missing. Add it to .env and try again."
    )

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def ask(prompt: str) -> str:
    """Send one prompt to the AI and return the answer text."""
    response = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


# Level A: vague task only
prompt_a = "Explain Python lists"

# Level B: task + role + length constraint
prompt_b = (
    "You are a Python tutor for beginners. "
    "Explain Python lists in under 100 words."
)

# Level C: task + role + required output structure
prompt_c = """You are a Python tutor for beginners. Explain Python lists.
Format:
1) One-sentence definition
2) Three common operations with code examples
3) One common mistake to avoid"""


if __name__ == "__main__":
    prompts = {
        "Level A (Vague)": prompt_a,
        "Level B (Structured)": prompt_b,
        "Level C (Precise)": prompt_c,
    }

    for level, prompt in prompts.items():
        print(f"\n{'=' * 60}")
        print(f"  {level}")
        print(f"  Prompt: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
        print(f"{'=' * 60}")

        answer = ask(prompt)
        print(answer)
