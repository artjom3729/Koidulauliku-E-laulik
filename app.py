"""
Koidulauliku E-laulik - Main Flask Application
A web application for Koidulaulik's spirit to explore modern Estonian culture
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
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
                if query in item.get('title', '').lower() or query in item.get('description', '').lower():
                    item['category'] = 'Uudised'
                    results.append(item)
        
        if category in ['all', 'syndmused']:
            kultuurikava_events = kultuurikava_scraper.get_events(limit=20)
            piletilevi_events = piletilevi_scraper.get_cultural_events(limit=20)
            events = kultuurikava_events + piletilevi_events
            for item in events:
                if query in item.get('title', '').lower() or query in item.get('description', '').lower():
                    item['category'] = 'Sündmused'
                    results.append(item)
        
        if category in ['all', 'kultuur']:
            culture_info = wiki_scraper.get_culture_info()
            for item in culture_info:
                if query in item.get('title', '').lower() or query in item.get('content', '').lower():
                    item['category'] = 'Kultuur'
                    results.append(item)
    except Exception as e:
        print(f"Search error: {e}")
    
    return jsonify(results[:20])

@app.route('/galerii')
def galerii():
    """Photo gallery page - recent images from cultural events"""
    try:
        kultuurikava_events = kultuurikava_scraper.get_events(limit=8)
        piletilevi_events = piletilevi_scraper.get_cultural_events(limit=8)
        gallery_items = [
            item for item in (kultuurikava_events + piletilevi_events)
            if item.get('image')
        ]

        if not gallery_items:
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
    return [
        {
            'title': 'Laulupeo õhtuvalgus',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Tallinn',
            'source': 'Koidulauliku E-laulik',
            'image': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJz48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9J2cxJyB4MT0nMCcgeDI9JzEnPjxzdG9wIG9mZnNldD0nMCcgc3RvcC1jb2xvcj0nIzAwNTVBNCcvPjxzdG9wIG9mZnNldD0nMScgc3RvcC1jb2xvcj0nIzAwQTNFMCcvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJyBmaWxsPSd1cmwoI2cxKScvPjxjaXJjbGUgY3g9JzEyMCcgY3k9JzEyMCcgcj0nNjAnIGZpbGw9JyNGRkQ3MDAnLz48dGV4dCB4PSc1MCUnIHk9JzU1JScgZm9udC1zaXplPSczNicgdGV4dC1hbmNob3I9J21pZGRsZScgZmlsbD0nI2ZmZmZmZicgZm9udC1mYW1pbHk9J1JvYm90bywgQXJpYWwnPkxhdWx1cGlkdTwvdGV4dD48dGV4dCB4PSc1MCUnIHk9JzcwJScgZm9udC1zaXplPScyMCcgdGV4dC1hbmNob3I9J21pZGRsZScgZmlsbD0nI2ZmZmZmZicgZm9udC1mYW1pbHk9J1JvYm90bywgQXJpYWwnPkt1bHR1dXJpaGV0azwvdGV4dD48L3N2Zz4='
        },
        {
            'title': 'Tantsuõhtu rahvamajas',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Tartu',
            'source': 'Koidulauliku E-laulik',
            'image': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJz48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9J2cyJyB4MT0nMCcgeDI9JzEnPjxzdG9wIG9mZnNldD0nMCcgc3RvcC1jb2xvcj0nI2Y4ZjFlNScvPjxzdG9wIG9mZnNldD0nMScgc3RvcC1jb2xvcj0nI2YwZDlhMScvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJyBmaWxsPSd1cmwoI2cyKScvPjxyZWN0IHg9JzYwJyB5PSc3MCcgd2lkdGg9JzUyMCcgaGVpZ2h0PScyODAnIHJ4PScyNCcgZmlsbD0nIzAwNTVBNCcgb3BhY2l0eT0nMC44NScvPjx0ZXh0IHg9JzUwJScgeT0nNTIlJyBmb250LXNpemU9JzMyJyB0ZXh0LWFuY2hvcj0nbWlkZGxlJyBmaWxsPScjZmZmZmZmJyBmb250LWZhbWlseT0nUm9ib3RvLCBBcmlhbCc+UmFodmF0YW50czwvdGV4dD48dGV4dCB4PSc1MCUnIHk9JzY3JScgZm9udC1zaXplPScyMCcgdGV4dC1hbmNob3I9J21pZGRsZScgZmlsbD0nI2ZmZmZmZicgZm9udC1mYW1pbHk9J1JvYm90bywgQXJpYWwnPkVsYXYgdHJhZGl0c2lvb248L3RleHQ+PC9zdmc='
        },
        {
            'title': 'Teatriõhtu vanalinnas',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Pärnu',
            'source': 'Koidulauliku E-laulik',
            'image': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJz48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9J2czJyB4MT0nMCcgeDI9JzEnPjxzdG9wIG9mZnNldD0nMCcgc3RvcC1jb2xvcj0nIzJiMmIyYicvPjxzdG9wIG9mZnNldD0nMScgc3RvcC1jb2xvcj0nIzRhNGE0YScvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJyBmaWxsPSd1cmwoI2czKScvPjxyZWN0IHg9JzkwJyB5PSc4MCcgd2lkdGg9JzQ2MCcgaGVpZ2h0PScyNjAnIHJ4PScxOCcgZmlsbD0nI0ZGRDcwMCcgb3BhY2l0eT0nMC44Jy8+PHRleHQgeD0nNTAlJyB5PSc1NCUnIGZvbnQtc2l6ZT0nMzInIHRleHQtYW5jaG9yPSdtaWRkbGUnIGZpbGw9JyMyYjJiMmInIGZvbnQtZmFtaWx5PSdSb2JvdG8sIEFyaWFsJz5UZWF0ZXI8L3RleHQ+PHRleHQgeD0nNTAlJyB5PSc2OSUnIGZvbnQtc2l6ZT0nMjAnIHRleHQtYW5jaG9yPSdtaWRkbGUnIGZpbGw9JyMyYjJiMmInIGZvbnQtZmFtaWx5PSdSb2JvdG8sIEFyaWFsJz5MYXZha3Vuc3Q8L3RleHQ+PC9zdmc='
        },
        {
            'title': 'Kontserdipäev rannal',
            'date': datetime.now().strftime('%d.%m.%Y'),
            'location': 'Haapsalu',
            'source': 'Koidulauliku E-laulik',
            'image': 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJz48ZGVmcz48bGluZWFyR3JhZGllbnQgaWQ9J2c0JyB4MT0nMCcgeDI9JzEnPjxzdG9wIG9mZnNldD0nMCcgc3RvcC1jb2xvcj0nIzJmNmY0ZScvPjxzdG9wIG9mZnNldD0nMScgc3RvcC1jb2xvcj0nIzdmYmY3ZicvPjwvbGluZWFyR3JhZGllbnQ+PC9kZWZzPjxyZWN0IHdpZHRoPSc2NDAnIGhlaWdodD0nNDIwJyBmaWxsPSd1cmwoI2c0KScvPjxjaXJjbGUgY3g9JzUyMCcgY3k9JzEyMCcgcj0nNzAnIGZpbGw9JyNGRkQ3MDAnLz48cmVjdCB4PSc4MCcgeT0nMjIwJyB3aWR0aD0nNDgwJyBoZWlnaHQ9JzEyMCcgcng9JzIwJyBmaWxsPScjZmZmZmZmJyBvcGFjaXR5PScwLjg1Jy8+PHRleHQgeD0nNTAlJyB5PSc1OCUnIGZvbnQtc2l6ZT0nMzAnIHRleHQtYW5jaG9yPSdtaWRkbGUnIGZpbGw9JyMyZjZmNGUnIGZvbnQtZmFtaWx5PSdSb2JvdG8sIEFyaWFsJz5Lb250c2VydDwvdGV4dD48dGV4dCB4PSc1MCUnIHk9JzcyJScgZm9udC1zaXplPScyMCcgdGV4dC1hbmNob3I9J21pZGRsZScgZmlsbD0nIzJmNmY0ZScgZm9udC1mYW1pbHk9J1JvYm90bywgQXJpYWwnPlN1dmXDtWh0dTwvdGV4dD48L3N2Zz4='
        }
    ]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
