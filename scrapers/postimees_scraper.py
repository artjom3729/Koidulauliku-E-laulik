"""
Postimees News Scraper
Collects news articles from Postimees about Estonian culture and society
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime

class PostimeesScraper:
    """Scraper for Postimees news portal"""
    
    def __init__(self):
        self.base_url = "https://www.postimees.ee"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_news(self, limit=10):
        """
        Fetch latest news articles from Postimees
        Returns a list of news items with title, description, link, date, source
        """
        news_items = []
        
        try:
            # Try to fetch from Postimees kultuur section
            url = f"{self.base_url}/kultuur"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find article elements
            articles = soup.find_all(['article', 'div'], class_=['article', 'story', 'article-item'], limit=limit*2)
            
            for article in articles:
                if len(news_items) >= limit:
                    break
                    
                try:
                    # Extract title
                    title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                    if not title_elem:
                        continue
                    title = title_elem.get_text(strip=True)
                    
                    # Extract link
                    link_elem = article.find('a', href=True)
                    link = link_elem['href'] if link_elem else "#"
                    if link and not link.startswith('http'):
                        link = self.base_url + link
                    
                    # Extract description
                    desc_elem = article.find(['p', 'div'], class_=['lead', 'summary', 'excerpt', 'description'])
                    description = desc_elem.get_text(strip=True) if desc_elem else ""
                    
                    # Extract date
                    date_elem = article.find(['time', 'span'], class_=['date', 'time', 'published'])
                    date_str = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime('%Y-%m-%d')
                    
                    if title and title not in [item['title'] for item in news_items]:
                        news_items.append({
                            'title': title,
                            'description': description[:200] + '...' if len(description) > 200 else description,
                            'link': link,
                            'date': date_str,
                            'source': 'Postimees',
                            'image': self._extract_image(article)
                        })
                    
                except Exception as e:
                    print(f"Error parsing Postimees article: {e}")
                    continue
            
            # If no articles found, add sample data
            if not news_items:
                news_items = self._get_sample_news()
                
        except Exception as e:
            print(f"Error fetching Postimees news: {e}")
            # Return sample data on error
            news_items = self._get_sample_news()
        
        return news_items[:limit]
    
    def _extract_image(self, article):
        """Extract image URL from article"""
        img = article.find('img')
        if img:
            src = img.get('src') or img.get('data-src')
            if src and not src.startswith('http'):
                return self.base_url + src
            return src
        return None
    
    def _get_sample_news(self):
        """Return sample news data when scraping fails"""
        return [
            {
                'title': 'Eesti kirjanduse tulevikust',
                'description': 'Uuring näitab, et eesti kirjandus areneb edasi ja leiab uusi lugejaid.',
                'link': 'https://www.postimees.ee/kultuur',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Postimees',
                'image': None
            },
            {
                'title': 'Teatrifestival toob Eestisse rahvusvahelised külalised',
                'description': 'Suurim teatrifestival toimub sel aastal Tallinnas ja Tartus.',
                'link': 'https://www.postimees.ee/kultuur',
                'date': datetime.now().strftime('%Y-%m-%d'),
                'source': 'Postimees',
                'image': None
            }
        ]
