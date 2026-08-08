import unittest

from scripts.validate_repo import extract_citation_keys


class CitationExtractionTests(unittest.TestCase):
    def test_ignores_inline_and_fenced_code_examples(self) -> None:
        text = """A supported claim [@real2026].

Contributor example: `[@bibkey]`.

```markdown
A documentation placeholder [@placeholder].
```

~~~text
Another placeholder @not-a-source.
~~~
"""

        self.assertEqual({"real2026"}, extract_citation_keys(text))

    def test_collects_multiple_real_citations(self) -> None:
        text = "A sentence supported by [@alpha2020; @beta2021, pp. 4–5]."

        self.assertEqual({"alpha2020", "beta2021"}, extract_citation_keys(text))


if __name__ == "__main__":
    unittest.main()
