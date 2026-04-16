import pytest
from unittest.mock import patch, MagicMock
from project import get_headlines, get_articles

fake_index_html = """
<html>
  <body>
    <a href="/news/articles/abc67">
      <h2>Test headline 6</h2>
    </a>
    <a href="/news/articles/xyz76">
      <h2>Test headline 7</h2>
    </a>
  </body>
</html>
"""

fake_article_html = """
<html>
  <body>
    <article>
      <p>First paragraph of the article.</p>
      <p>Second paragraph of the article.</p>
      <p>Third paragraph of the article.</p>
    </article>
  </body>
</html>
"""

@pytest.fixture
def headlines():
    mock_response = MagicMock()
    mock_response.text = fake_index_html
    with patch("project.requests.get", return_value=mock_response):
        return get_headlines("news")

@pytest.fixture
def article_body():
    mock_response = MagicMock()
    mock_response.text = fake_article_html
    with patch("project.requests.get", return_value=mock_response):
        return get_articles("https://www.bbc.com/news/articles/abc67")

def test_returns_list(headlines):
    assert isinstance(headlines, list)
    assert len(headlines) == 2

def test_items_are_dicts(headlines):
    for item in headlines:
        assert isinstance(item, dict)
        assert "title" in item
        assert "url" in item
        assert isinstance(item["title"], str)
        assert item["url"].startswith("https://www.bbc.com")

def test_article_returns_string(article_body):
    assert isinstance(article_body, str)
    assert len(article_body) > 0

def test_article_contains_text(article_body):
    assert "First paragraph" in article_body


