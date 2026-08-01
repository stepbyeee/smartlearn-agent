import unittest

# Fail clearly if cli_qa.py doesn't exist yet, instead of an unhandled ImportError.
try:
    from cli_qa import split_paragraphs, number_paragraphs
except ImportError:
    raise AssertionError(
        "cli_qa.py does not exist yet. "
        "Create it and define split_paragraphs(text: str) -> list[str] "
        "and number_paragraphs(paragraphs: list[str]) -> str."
    )


class TestParagraphSplitting(unittest.TestCase):
    """Unit tests for paragraph splitting logic in cli_qa.py."""

    # --- split_paragraphs ---------------------------------------------------

    def test_splits_on_single_blank_line(self):
        text = "First paragraph.\n\nSecond paragraph."
        result = split_paragraphs(text)
        self.assertEqual(result, ["First paragraph.", "Second paragraph."])

    def test_splits_on_multiple_blank_lines(self):
        text = "First paragraph.\n\n\n\nSecond paragraph."
        result = split_paragraphs(text)
        self.assertEqual(result, ["First paragraph.", "Second paragraph."])

    def test_splits_on_whitespace_only_line(self):
        text = "First paragraph.\n   \nSecond paragraph."
        result = split_paragraphs(text)
        self.assertEqual(result, ["First paragraph.", "Second paragraph."])

    def test_ignores_leading_blank_lines(self):
        text = "\n\nFirst paragraph.\n\nSecond paragraph."
        result = split_paragraphs(text)
        self.assertEqual(result, ["First paragraph.", "Second paragraph."])

    def test_ignores_trailing_blank_lines(self):
        text = "First paragraph.\n\nSecond paragraph.\n\n"
        result = split_paragraphs(text)
        self.assertEqual(result, ["First paragraph.", "Second paragraph."])

    def test_single_paragraph(self):
        text = "Only one paragraph."
        result = split_paragraphs(text)
        self.assertEqual(result, ["Only one paragraph."])

    def test_preserves_internal_newlines(self):
        text = "Line one.\nLine two.\n\nSecond paragraph."
        result = split_paragraphs(text)
        self.assertEqual(result, ["Line one.\nLine two.", "Second paragraph."])

    def test_trims_leading_trailing_paragraph_whitespace(self):
        text = "  leading spaces\n\n  line one\n  line two\n\ntrailing spaces  "
        result = split_paragraphs(text)
        self.assertEqual(result, [
            "leading spaces",
            "line one\n  line two",
            "trailing spaces",
        ])

    # --- number_paragraphs ---------------------------------------

    def test_numbers_from_one(self):
        paragraphs = ["Alpha", "Bravo", "Charlie"]
        result = number_paragraphs(paragraphs)
        self.assertIn("[Paragraph 1]", result)
        self.assertIn("[Paragraph 2]", result)
        self.assertIn("[Paragraph 3]", result)

    def test_preserves_paragraph_text_when_numbering(self):
        paragraphs = ["The sky is blue.", "Grass is green."]
        result = number_paragraphs(paragraphs)
        self.assertIn("The sky is blue.", result)
        self.assertIn("Grass is green.", result)

    def test_empty_list_produces_empty_string(self):
        result = number_paragraphs([])
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
