import unittest

from scripts.validate_repo import extract_citation_keys, parse_svg_viewbox


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


class SvgBannerTests(unittest.TestCase):
    def test_parses_numeric_viewbox(self) -> None:
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 600"></svg>'
        self.assertEqual((0.0, 0.0, 1800.0, 600.0), parse_svg_viewbox(svg))

    def test_rejects_missing_viewbox(self) -> None:
        svg = '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
        with self.assertRaisesRegex(ValueError, "lacks viewBox"):
            parse_svg_viewbox(svg)

    def test_rejects_nonpositive_dimensions(self) -> None:
        svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1800 0"></svg>'
        with self.assertRaisesRegex(ValueError, "must be positive"):
            parse_svg_viewbox(svg)


if __name__ == "__main__":
    unittest.main()
