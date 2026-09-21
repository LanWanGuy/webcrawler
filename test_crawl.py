import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html, get_urls_from_html, get_images_from_html, extract_page_data


class TestCrawl(unittest.TestCase):
    def test_normalize_url_with_https(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_https_and_trailing_slash(self):
        input_url = "https://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http(self):
        input_url = "http://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_with_http_and_trailing_slash(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_without_protocol(self):
        input_url = "www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_basic(self):
        input_body = "<html>><body><h1>Test Title</h1></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_no_h1(self):
        input_body = "<html><body><h2>Test Title</h2></body></html>"
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_empty(self):
        input_body = "<html><body>There are no h1 or h2 tags here</body></html>"
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_basic(self):
        input_body = "<html><body><p>Outside Paragraph</p><main><p>Main Paragraph</p></main></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main Paragraph"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_noMain(self):
        input_body = "<html><body><p>Outside Paragraph</p><main></main></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = "Outside Paragraph"
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_noP(self):
        input_body = "<html><body><main></main></body></html>"
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_absolute(self):
        input_body = '<html><body><a href="https://crawler-test.com">Link</a></body></html>'
        input_url = "https://crawler-test.com"
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_body = '<html><body><a href="/relative">Link</a></body></html>'
        input_url = "https://crawler-test.com"
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/relative"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_noAnchor(self):
        input_body = '<html><body><p>No Anchor</p></body></html>'
        input_url = "https://crawler-test.com"
        actual = get_urls_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_body = '<html><body><img src="https://crawler-test.com/image.jpg"></body></html>'
        input_url = "https://crawler-test.com"
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_relative(self):
        input_body = '<html><body><img src="/image.jpg"></body></html>'
        input_url = "https://crawler-test.com"
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/image.jpg"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_noImg(self):
        input_body = '<html><body><p>No Image</p></body></html>'
        input_url = "https://crawler-test.com"
        actual = get_images_from_html(input_body, input_url)
        expected = []
        self.assertEqual(actual, expected)

    def test_extract_page_data_relative(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="/link1">Link 1</a>
                <img src="/image1.jpg" alt="Image 1">
            </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="https://crawler-test.com/link1">Link 1</a>
                <img src="https://crawler-test.com/image1.jpg" alt="Image 1">
            </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                <a href="https://crawler-test.com/link1">Link 1</a>
                <a href="https://crawler-test.com/link2">Link 2</a>
                <a href="https://crawler-test.com/link3">Link 3</a>
                <img src="https://crawler-test.com/image1.jpg" alt="Image 1">
                <img src="https://crawler-test.com/image2.jpg" alt="Image 2">
                <img src="https://crawler-test.com/image3.jpg" alt="Image 3">
            </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1", "https://crawler-test.com/link2", "https://crawler-test.com/link3"],
            "image_urls": ["https://crawler-test.com/image1.jpg", "https://crawler-test.com/image2.jpg", "https://crawler-test.com/image3.jpg"]
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_none(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
                <h1>Test Title</h1>
                <p>This is the first paragraph.</p>
                </body></html>"""
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": [],
            "image_urls": []
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
