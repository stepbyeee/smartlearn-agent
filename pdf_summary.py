import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
import fitz  # PyMuPDF


def extract_text(path):
    """Extract text from a PDF, returning page-numbered text.

    Returns the concatenated text with [Page N] markers, or prints an
    error and exits if the file cannot be read as a PDF.
    """
    try:
        doc = fitz.open(path)
    except fitz.FileDataError:
        print(f"Error: Cannot read PDF file: {path}")
        sys.exit(1)
    except Exception:
        print(f"Error: Cannot open file: {path}")
        sys.exit(1)

    total = len(doc)
    parts = []
    for i, page in enumerate(doc, start=1):
        print(f"Extracting page {i}/{total}...")
        text = page.get_text().strip()
        if text:
            parts.append(f"[Page {i}]\n{text}")
    doc.close()
    return "\n\n".join(parts)


def build_messages(extracted_text):
    """Build the system and user messages for the LLM summarisation call."""
    system_content = (
        "You are a helpful teaching assistant. Summarise the provided lecture "
        "slide text into exactly three sections with these exact headings:\n\n"
        "## Overview\n"
        "## Key Points\n"
        "## Limitations\n\n"
        "Rules:\n"
        "- Overview: 2-3 sentences describing what the slides cover.\n"
        "- Key Points: bullet list. Every bullet MUST end with [Page X] "
        "where X is the page number from the provided text.\n"
        "- Limitations: 2-4 bullets about what the slides do not cover or "
        "what might be missing (e.g. depth, missing examples, ambiguous slides).\n"
        "- Output ONLY the three sections. No preamble, no closing remarks."
    )
    user_content = (
        f"Summarise the following lecture slide text:\n\n{extracted_text}"
    )
    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]


def main():
    parser = argparse.ArgumentParser(
        description="Summarise a PDF file using an LLM."
    )
    parser.add_argument(
        "path",
        type=str,
        help="Path to the PDF file to summarise.",
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

    if not os.path.isfile(args.path):
        print(f"Error: File not found: {args.path}")
        sys.exit(1)

    extracted_text = extract_text(args.path)

    if not extracted_text.strip():
        print("Error: No extractable text found in the PDF.")
        sys.exit(1)

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",
        messages=build_messages(extracted_text),
        temperature=0.0,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
