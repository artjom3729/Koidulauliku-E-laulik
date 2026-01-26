"""
Scrapy pipelines for processing cultural events
"""

from datetime import datetime

class CulturalEventsPipeline:
    """Pipeline to process and clean cultural event items"""
    
    def __init__(self):
        self.events = []
    
    def process_item(self, item, spider):
        """Process and clean each scraped item"""
        # Clean title
        if 'title' in item:
            item['title'] = item['title'].strip()
        
        # Clean and truncate description
        if 'description' in item:
            desc = item['description'].strip()
            if len(desc) > 300:
                desc = desc[:300] + '...'
            item['description'] = desc
        
        # Ensure date format
        if 'date' not in item or not item['date']:
            item['date'] = datetime.now().strftime('%d.%m.%Y')
        
        # Ensure location
        if 'location' not in item or not item['location']:
            item['location'] = 'Asukoht täpsustamisel'
        
        # Store processed item
        self.events.append(dict(item))
        
        return item
    
    def close_spider(self, spider):
        """Called when spider is closed"""
        spider.logger.info(f'Scraped {len(self.events)} events')
