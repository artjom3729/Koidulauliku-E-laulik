"""
Scrapy spider for ERR Kultuur
Structured scraping of cultural articles from kultuur.err.ee
"""

import scrapy
from datetime import datetime

class ERRKultuurSpider(scrapy.Spider):
    name = 'err_kultuur'
    allowed_domains = ['kultuur.err.ee']
    start_urls = ['https://kultuur.err.ee/']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,
    }
    
    def parse(self, response):
        """Parse main page and extract articles"""
        # Find article elements
        articles = response.css('article.list-article, div.news-item, div.article-card')
        
        for article in articles[:10]:  # Limit to 10 articles
            yield {
                'title': self._extract_text(article, 'h1, h2, h3, a'),
                'description': self._extract_text(article, 'p.lead, p.description, div.excerpt'),
                'link': self._extract_link(article, response.url),
                'date': self._extract_text(article, 'time, span.date, span.published'),
                'source': 'ERR Kultuur',
                'image': self._extract_image(article, response.url),
                'scraped_at': datetime.now().isoformat()
            }
    
    def _extract_text(self, element, selector):
        """Extract text from element using CSS selector"""
        result = element.css(f'{selector}::text').get()
        return result.strip() if result else ''
    
    def _extract_link(self, element, base_url):
        """Extract and normalize link"""
        link = element.css('a::attr(href)').get()
        if link:
            if not link.startswith('http'):
                return base_url.rstrip('/') + '/' + link.lstrip('/')
            return link
        return ''
    
    def _extract_image(self, element, base_url):
        """Extract image URL"""
        img = element.css('img::attr(src)').get()
        if img:
            if not img.startswith('http'):
                return base_url.rstrip('/') + '/' + img.lstrip('/')
            return img
        return None
