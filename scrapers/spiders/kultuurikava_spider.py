"""
Scrapy spider for Kultuurikava
Structured scraping of cultural events from kultuurikava.ee
"""

import scrapy
from datetime import datetime

class KultuurikavaSpider(scrapy.Spider):
    name = 'kultuurikava'
    allowed_domains = ['kultuurikava.ee']
    start_urls = ['https://www.kultuurikava.ee/events/']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,
    }
    
    def parse(self, response):
        """Parse events page and extract event information"""
        # Find event elements
        events = response.css('div.event-card, article.event, div.event-item, div.calendar-event')
        
        for event in events[:10]:  # Limit to 10 events
            yield {
                'title': self._extract_text(event, 'h1, h2, h3, h4'),
                'description': self._extract_text(event, 'p.description, div.summary, p.lead'),
                'link': self._extract_link(event, response.url),
                'date': self._extract_text(event, 'time, span.date, div.event-date'),
                'location': self._extract_text(event, 'span.location, div.venue, p.place'),
                'source': 'Kultuurikava',
                'image': self._extract_image(event, response.url),
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
                from urllib.parse import urljoin
                return urljoin(base_url, link)
            return link
        return ''
    
    def _extract_image(self, element, base_url):
        """Extract image URL"""
        # Try multiple image sources
        for attr in ['src', 'data-src', 'data-lazy-src']:
            img = element.css(f'img::attr({attr})').get()
            if img:
                if not img.startswith('http'):
                    from urllib.parse import urljoin
                    return urljoin(base_url, img)
                return img
        return None
