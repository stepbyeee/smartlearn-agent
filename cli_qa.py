import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI


def split_paragraphs(text):
    """Split text into paragraphs on blank or whitespace-only lines.

    Leading/trailing blank lines are ignored.  Leading/trailing whitespace
    on each paragraph is trimmed.  Internal line breaks are preserved.
    """
    paragraphs = []
    current = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current:
                paragraphs.append("\n".join(current).strip())
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append("\n".join(current).strip())
    return paragraphs


def number_paragraphs(paragraphs):
    """Format paragraphs with [Paragraph X] numbering."""
    if not paragraphs:
        return ""
    return "\n".join(
        f"[Paragraph {i}] {p}" for i, p in enumerate(paragraphs, start=1)
    )


def read_text():
    """Read multi-line text from stdin until END appears alone on a line."""
    print("Paste text (type END on a new line to finish):")
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == "END":
            break
        lines.append(line)
    return "\n".join(lines)


def build_messages(numbered_text, question):
    """Build the system and user messages for the LLM call."""
    system_content = (
        "You are a helpful teaching assistant. Answer the user's question "
        "using ONLY the numbered text provided. Cite every factual "
        "claim by referencing the paragraph number using the format "
        "[Paragraph X]. If the answer cannot be found in the text, "
        'respond with exactly: "The text does not provide this information."\n'
        "\n"
        "Example:\n"
        "Text:\n"
        "[Paragraph 1] The sky is blue because of Rayleigh scattering.\n"
        "[Paragraph 2] Water freezes at 0 degrees Celsius.\n"
        "\n"
        "Question: Why is the sky blue?\n"
        "Answer: The sky appears blue due to Rayleigh scattering [Paragraph 1].\n"
        "\n"
        "Question: What is the capital of France?\n"
        'Answer: The text does not provide this information.'
    )
    user_content = f"{numbered_text}\n\nQuestion: {question}"
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Answer questions about provided text using an LLM."
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="Path to a UTF-8 text file to use as the reference text.",
    )
    args = parser.parse_args()

    load_dotenv()

    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print(
            "Error: OPENROUTER_API_KEY not found. "
            "Make sure your .env file contains the key."
        )
        sys.exit(1)

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        except OSError as e:
            print(f"Error: Cannot read file: {e}")
            sys.exit(1)
    else:
        text = read_text()

    if not text.strip():
        print("Error: No text provided. Please enter at least one paragraph.")
        sys.exit(1)

    paragraphs = split_paragraphs(text)
    numbered_text = number_paragraphs(paragraphs)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    while True:
        question = input("Question: ")
        if question.strip().lower() == "quit":
            print("Goodbye!")
            break
        if not question.strip():
            continue

        response = client.chat.completions.create(
            model="google/gemma-4-26b-a4b-it:free",
            messages=build_messages(numbered_text, question),
            temperature=0.0,
        )

        print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
