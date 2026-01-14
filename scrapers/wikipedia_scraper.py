"""
Wikipedia Estonian Culture Scraper
Collects information about Estonian culture from Wikipedia
"""

import requests
from bs4 import BeautifulSoup

class WikipediaScraper:
    """Scraper for Wikipedia articles about Estonian culture"""
    
    def __init__(self):
        self.base_url = "https://et.wikipedia.org"
        self.api_url = "https://et.wikipedia.org/w/api.php"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def get_culture_info(self):
        """
        Fetch information about Estonian culture from Wikipedia
        Returns a list of culture topics with title, summary, link
        """
        culture_topics = []
        
        # List of Estonian culture-related Wikipedia pages
        topics = [
            'Eesti_kultuur',
            'Eesti_kirjandus',
            'Eesti_muusika',
            'Eesti_teater',
            'Eesti_kunst',
            'Laulupidu',
            'Koidulauliku_vaim',
            'Eesti_rahvatants',
            'Eesti_rahvariided'
        ]
        
        for topic in topics:
            try:
                # Use Wikipedia API to get page summary
                params = {
                    'action': 'query',
                    'format': 'json',
                    'prop': 'extracts|info',
                    'exintro': True,
                    'explaintext': True,
                    'titles': topic.replace('_', ' '),
                    'inprop': 'url'
                }
                
                response = requests.get(self.api_url, params=params, headers=self.headers, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                pages = data.get('query', {}).get('pages', {})
                
                for page_id, page_data in pages.items():
                    if page_id != '-1':  # Page exists
                        title = page_data.get('title', topic.replace('_', ' '))
                        extract = page_data.get('extract', '')
                        url = page_data.get('fullurl', f"{self.base_url}/wiki/{topic}")
                        
                        # Limit extract length
                        if len(extract) > 500:
                            extract = extract[:500] + '...'
                        
                        culture_topics.append({
                            'title': title,
                            'content': extract,
                            'link': url,
                            'source': 'Wikipedia'
                        })
                        break
                    
            except Exception as e:
                print(f"Error fetching Wikipedia topic {topic}: {e}")
                # Add fallback data for this topic
                culture_topics.append(self._get_fallback_topic(topic))
        
        # If nothing was fetched, return sample data
        if not culture_topics:
            culture_topics = self._get_sample_culture_info()
        
        return culture_topics
    
    def _get_fallback_topic(self, topic):
        """Get fallback information for a topic"""
        topic_name = topic.replace('_', ' ')
        return {
            'title': topic_name,
            'content': f'Informatsioon teema "{topic_name}" kohta. Külastage Wikipediat täpsema info saamiseks.',
            'link': f"{self.base_url}/wiki/{topic}",
            'source': 'Wikipedia'
        }
    
    def _get_sample_culture_info(self):
        """Return sample culture information when scraping fails"""
        return [
            {
                'title': 'Eesti kultuur',
                'content': 'Eesti kultuur on välja kujunenud põhiliselt eestlaste endi tegevuse tulemusena, kuid seda on mõjutanud ka teiste rahvaste, eelkõige saksakeelse kultuuri mõjud. Eesti kultuuriloo olulisimad perioodid on olnud rahvusliku ärkamisaja kultuur 19. sajandil ja Eesti iseseisvumisaegne kultuur 20. sajandil.',
                'link': 'https://et.wikipedia.org/wiki/Eesti_kultuur',
                'source': 'Wikipedia'
            },
            {
                'title': 'Laulupidu',
                'content': 'Laulupidu on Eestis regulaarselt toimuv üldlaulupidu, kus laulavad koorid kogu Eestist. Esimene üldlaulupidu toimus 1869. aastal Tartus. Laulupidu on Eesti kultuuri üks olulisemaid sümboleid ja UNESCO immateriaalse kultuuripärandi nimistus.',
                'link': 'https://et.wikipedia.org/wiki/Laulupidu',
                'source': 'Wikipedia'
            },
            {
                'title': 'Eesti kirjandus',
                'content': 'Eesti kirjandus on eestikeelne ilukirjandus. Eesti kirjanduse alguseks loetakse sageli 17. sajandi algust, kui ilmusid esimesed eestikeelsed trükised. Eesti rahvusliku kirjanduse rajajaks peetakse Fr. R. Kreutzwaldi, kes kogus ja avaldas "Kalevipoega".',
                'link': 'https://et.wikipedia.org/wiki/Eesti_kirjandus',
                'source': 'Wikipedia'
            },
            {
                'title': 'Eesti muusika',
                'content': 'Eesti muusikaelu on rikkalik ja mitmekesine. Eestis on tugev koorilaulutraditsioon, mis tipneb iga viie aasta tagant toimuva laulupeo ja tantsupiduga. Eestis on tuntud heliloojaid nagu Arvo Pärt, Veljo Tormis ja Erkki-Sven Tüür.',
                'link': 'https://et.wikipedia.org/wiki/Eesti_muusika',
                'source': 'Wikipedia'
            },
            {
                'title': 'Eesti rahvatants',
                'content': 'Eesti rahvatants on oluline osa Eesti kultuurist. Rahvatantsu harrastatakse kogu Eestis ja igal aastal toimub üldtantsupidu, kus osalevad tuhanded tantsijad. Rahvatantsu traditsioonid pärinevad sajandite tagustest aegadest.',
                'link': 'https://et.wikipedia.org/wiki/Eesti_rahvatants',
                'source': 'Wikipedia'
            }
        ]
