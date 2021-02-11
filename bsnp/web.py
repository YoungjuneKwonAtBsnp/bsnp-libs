import requests

class Session():
    def __init__(self, prefix=''):
        self.session = requests.Session()
        self.default_header = {'User-Agent':'Mozilla/5.0', 'Cache-Control': 'no-cache'}
        self.url_prefix = prefix
        self.post_direct = self.session.post

    def header_with(self, headers):
        h=dict(self.default_header)
        h.update(headers)
        return h
    
    def validate_url(self, url):
        return self.url_prefix + url if url.startswith("/") else url 

    def post(self, url, body={}, files=None, headers={}, parse_level=1): 
        r=self.session.post(self.validate_url(url),
                            body, files=files,
                            headers=self.header_with(headers))
        return self.parse_by_level(r.content, parse_level)

    def put(self, url, body={}, headers={}, parse_level=1): 
        r=self.session.put(self.validate_url(url),
                            body,
                            headers=self.header_with(headers))
        return self.parse_by_level(r.content, parse_level)

    def get(self, url, headers={}, parse_level=1):
        r=self.session.get(self.validate_url(url),
                           headers=self.header_with(headers))
        return self.parse_by_level(r.content, parse_level)
        
    def parse_by_level(self, content, level):
        return self.parse(content) if level > 0 else content

    def parse(self, content):
        from bs4 import BeautifulSoup
        return BeautifulSoup(content, 'html5lib')
    
    def enumerate_page(self, pattern, max_page=1000, parse_level=1, headers={}, start=1):
        from urllib import parse
        page = start
        while page < max_page:
            url = pattern%(page)
            yield (page, 
                   self.get(url, headers=headers, parse_level=parse_level))
            page += 1
