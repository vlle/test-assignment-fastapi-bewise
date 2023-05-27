from urllib.parse import urlencode, urljoin, urlparse

QUIZ_LINK = "https://jservice.io/api/random"
a = urlparse(QUIZ_LINK)
query = urlencode({"count": 3})
api_url_with_qustion_num = urljoin(QUIZ_LINK, query, allow_fragments=False)
print(api_url_with_qustion_num)
