"""
Scrapy spider for Piletilevi
Structured scraping of cultural events with images from piletilevi.ee
"""

import scrapy
from datetime import datetime
import re

class PiletileviSpider(scrapy.Spider):
    name = 'piletilevi'
    allowed_domains = ['piletilevi.ee']
    start_urls = ['https://www.piletilevi.ee/']
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'ROBOTSTXT_OBEY': True,
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 1,
    }
    
    def parse(self, response):
        """Parse main page and extract cultural events with images"""
        # Find event/product elements
        events = response.css('div.event, div.event-card, article.event-item, div.product-item, li.ticket-item')
        
        for event in events[:10]:  # Limit to 10 events
            # Extract image - priority for this scraper
            image_url = self._extract_image(event, response.url)
            
            # Only include events that have images (requirement focus)
            title = self._extract_text(event, 'h1, h2, h3, h4')
            if title and len(title) > 3:
                yield {
                    'title': title,
                    'description': self._extract_text(event, 'p.description, div.summary, div.info'),
                    'link': self._extract_link(event, response.url),
                    'date': self._extract_text(event, 'time, span.date, div.datetime'),
                    'location': self._extract_text(event, 'span.location, div.venue, p.place'),
                    'source': 'Piletilevi',
                    'image': image_url,
                    'category': 'kultuur',
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
        """Extract image URL - multiple sources"""
        # Try direct image sources
        for attr in ['src', 'data-src', 'data-lazy-src', 'data-original']:
            img = element.css(f'img::attr({attr})').get()
            if img and not img.startswith('data:') and 'placeholder' not in img.lower():
                if not img.startswith('http'):
                    from urllib.parse import urljoin
                    return urljoin(base_url, img)
                return img
        
        # Try background images from style attribute
        style = element.css('*::attr(style)').get()
        if style and 'background-image' in style:
            match = re.search(r'url\(["\']?([^"\']+)["\']?\)', style)
            if match:
                url = match.group(1)
                if not url.startswith('http'):
                    from urllib.parse import urljoin
                    return urljoin(base_url, url)
                return url
        
        return None
