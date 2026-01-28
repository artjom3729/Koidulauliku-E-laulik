"""
Koidulauliku E-laulik - Main Flask Application
A web application for Koidulaulik's spirit to explore modern Estonian culture
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
from itertools import chain
from urllib.parse import quote
import os
from scrapers.err_scraper import ERRNewsScraper
from scrapers.wikipedia_scraper import WikipediaScraper
from scrapers.kultuurikava_scraper import KultuurikavaScraper
from scrapers.piletilevi_scraper import PiletileviScraper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'koidulaulik-secret-key-2026'

# Initialize scrapers
err_scraper = ERRNewsScraper()
wiki_scraper = WikipediaScraper()
kultuurikava_scraper = KultuurikavaScraper()
piletilevi_scraper = PiletileviScraper()

def _safe_text(value):
    if value is None:
        return ''
    if isinstance(value, bytes):
        return value.decode('utf-8', errors='replace')
    return str(value)

def _query_matches(item, query):
    if not isinstance(item, dict):
        return False
    title = _safe_text(item.get('title'))
    description = _safe_text(item.get('description'))
    content = _safe_text(item.get('content'))
    return (
        query in title.lower()
        or query in description.lower()
        or query in content.lower()
    )

def _normalize_search_item(item, category):
    return {
        'title': _safe_text(item.get('title')),
        'description': _safe_text(item.get('description') or item.get('content')),
        'content': _safe_text(item.get('content')),
        'link': _safe_text(item.get('link')),
        'category': category
    }

@app.route('/')
def index():
    """Main page with overview of all categories"""
    return render_template('index.html')

@app.route('/uudised')
def uudised():
    """News page - aggregates news from multiple sources"""
    try:
        err_news = err_scraper.get_news(limit=10)
        return render_template('uudised.html', news=err_news)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return render_template('uudised.html', news=[], error=str(e))

@app.route('/syndmused')
def syndmused():
    """Events page - cultural events in Estonia"""
    try:
        # Aggregate events from multiple sources
        kultuurikava_events = kultuurikava_scraper.get_events(limit=5)
        piletilevi_events = piletilevi_scraper.get_cultural_events(limit=5)
        
        # Combine all events
        all_events = kultuurikava_events + piletilevi_events
        
        return render_template('syndmused.html', events=all_events)
    except Exception as e:
        print(f"Error fetching events: {e}")
        return render_template('syndmused.html', events=[], error=str(e))

@app.route('/kultuur')
def kultuur():
    """Culture page - information about Estonian culture from Wikipedia"""
    try:
        culture_info = wiki_scraper.get_culture_info()
        return render_template('kultuur.html', culture_info=culture_info)
    except Exception as e:
        print(f"Error fetching culture info: {e}")
        return render_template('kultuur.html', culture_info=[], error=str(e))

@app.route('/api/search')
def search():
    """API endpoint for searching across all content"""
    query = request.args.get('q', '').lower()
    category = request.args.get('category', 'all')
    
    results = []
    
    try:
        if category in ['all', 'uudised']:
            news = err_scraper.get_news(limit=20)
            
            for item in news:
                if _query_matches(item, query):
                    results.append(_normalize_search_item(item, 'Uudised'))
        
        if category in ['all', 'syndmused']:
            kultuurikava_events = kultuurikava_scraper.get_events(limit=20)
            piletilevi_events = piletilevi_scraper.get_cultural_events(limit=20)
            events = kultuurikava_events + piletilevi_events
            for item in events:
                if _query_matches(item, query):
                    results.append(_normalize_search_item(item, 'Sündmused'))
        
        if category in ['all', 'kultuur']:
            culture_info = wiki_scraper.get_culture_info()
            for item in culture_info:
                if _query_matches(item, query):
                    results.append(_normalize_search_item(item, 'Kultuur'))
    except Exception as e:
        print(f"Search error: {e}")
    
    return jsonify(results[:20])

@app.route('/galerii')
def galerii():
    """Photo gallery page - recent images from cultural events"""
    try:
        kultuurikava_events = kultuurikava_scraper.get_events(limit=12)
        piletilevi_events = piletilevi_scraper.get_cultural_events(limit=12)
        gallery_items = [
            item for item in chain(kultuurikava_events, piletilevi_events)
            if item.get('image')
        ]

        if len(gallery_items) < 3:
            gallery_items = _get_gallery_fallback()

        return render_template('galerii.html', gallery_items=gallery_items)
    except Exception as e:
        print(f"Error fetching gallery images: {e}")
        return render_template('galerii.html', gallery_items=_get_gallery_fallback(), error=str(e))

@app.route('/info')
def info():
    """Information page about the application"""
    return render_template('info.html')

def _get_gallery_fallback():
    """Fallback gallery items when event images are unavailable"""
    def build_placeholder(config):
        svg = (
            "<svg xmlns='http://www.w3.org/2000/svg' width='640' height='420'>"
            "<defs><linearGradient id='g' x1='0' x2='1'>"
            f"<stop offset='0' stop-color='{config['gradient_start']}'/>"
            f"<stop offset='1' stop-color='{config['gradient_end']}'/>"
            "</linearGradient></defs>"
            "<rect width='640' height='420' fill='url(#g)'/>"
            f"{config['accent_shape']}"
            f"<text x='50%' y='55%' font-size='32' text-anchor='middle' fill='{config['text_color']}' "
            "font-family='Playfair Display, Roboto, Arial'>"
            f"{config['title']}</text>"
            f"<text x='50%' y='70%' font-size='20' text-anchor='middle' fill='{config['text_color']}' "
            "font-family='Roboto, Arial'>"
            f"{config['subtitle']}</text>"
            "</svg>"
        )
        return f"data:image/svg+xml;charset=UTF-8,{quote(svg)}"

    return [
        {
            'title': 'Laulupeo õhtuvalgus',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Tallinn',
            'source': 'Koidulauliku E-laulik',
            'image': build_placeholder({
                'title': 'Laulupidu',
                'subtitle': 'Kultuurihetk',
                'gradient_start': '#0055A4',
                'gradient_end': '#00A3E0',
                'accent_shape': "<circle cx='120' cy='120' r='60' fill='#FFD700'/>",
                'text_color': '#ffffff'
            })
        },
        {
            'title': 'Tantsuõhtu rahvamajas',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Tartu',
            'source': 'Koidulauliku E-laulik',
            'image': build_placeholder({
                'title': 'Rahvatants',
                'subtitle': 'Elav traditsioon',
                'gradient_start': '#f8f1e5',
                'gradient_end': '#f0d9a1',
                'accent_shape': "<rect x='60' y='70' width='520' height='280' rx='24' fill='#0055A4' opacity='0.85'/>",
                'text_color': '#ffffff'
            })
        },
        {
            'title': 'Teatriõhtu vanalinnas',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Pärnu',
            'source': 'Koidulauliku E-laulik',
            'image': build_placeholder({
                'title': 'Teater',
                'subtitle': 'Lavakunst',
                'gradient_start': '#2b2b2b',
                'gradient_end': '#4a4a4a',
                'accent_shape': "<rect x='90' y='80' width='460' height='260' rx='18' fill='#FFD700' opacity='0.8'/>",
                'text_color': '#2b2b2b'
            })
        },
        {
            'title': 'Kontserdipäev rannal',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Haapsalu',
            'source': 'Koidulauliku E-laulik',
            'image': build_placeholder({
                'title': 'Kontsert',
                'subtitle': 'Suveõhtu',
                'gradient_start': '#2f6f4e',
                'gradient_end': '#7fbf7f',
                'accent_shape': "<circle cx='520' cy='120' r='70' fill='#FFD700'/>"
                "<rect x='80' y='220' width='480' height='120' rx='20' fill='#ffffff' opacity='0.85'/>",
                'text_color': '#2f6f4e'
            })
        }
    ]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
