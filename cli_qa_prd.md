# CLI Q&A Tool — PRD

## What It Does

A command-line tool that takes multi-paragraph text and a question, then uses an LLM to answer the question with paragraph-level citations.

## Input

1. Multi-line text entered by the user.
2. The user types `END` on a new line to finish entering text.
3. A question about the provided text.

## Output

An answer based only on the provided text, with citations in the format `[Paragraph X]`.

## Technical Requirements

- Use the OpenRouter API.
- Use model `google/gemma-4-26b-a4b-it:free`.
- Load `OPENROUTER_API_KEY` from `.env`.
- Never print, read aloud, modify, or commit `.env`.
- Use the installed `openai` and `python-dotenv` packages.

## Acceptance Tests

The implementation passes when:

1. The user can paste multi-paragraph text and finish with `END`.
2. The program splits text into paragraphs using blank lines.
3. An answer supported by Paragraph 1 cites `[Paragraph 1]`.
4. Every factual claim includes an appropriate `[Paragraph X]` citation.
5. If the answer is absent, the output is exactly:
   `The text does not provide this information.`
6. Empty text exits with a friendly error before making an API call.
7. A missing API Key produces a clear error without printing the Key.
8. `python -m py_compile cli_qa.py` succeeds.

## Scope

Create `cli_qa.py`.

Do not add:

- A graphical interface
- A database
- PDF support
- User accounts
- A vector database
- Changes to `.env`
