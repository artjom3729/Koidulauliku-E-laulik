"""
Koidulauliku E-laulik - Main Flask Application
A web application for Koidulaulik's spirit to explore modern Estonian culture
"""

from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from scrapers.err_scraper import ERRNewsScraper
from scrapers.postimees_scraper import PostimeesScraper
from scrapers.culture_scraper import CultureScraper
from scrapers.wikipedia_scraper import WikipediaScraper
from scrapers.kultuurikava_scraper import KultuurikavaScraper
from scrapers.piletilevi_scraper import PiletileviScraper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'koidulaulik-secret-key-2026'

# Initialize scrapers
err_scraper = ERRNewsScraper()
postimees_scraper = PostimeesScraper()
culture_scraper = CultureScraper()
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
        err_news = err_scraper.get_news(limit=5)
        postimees_news = postimees_scraper.get_news(limit=5)
        
        # Combine and sort by date
        all_news = err_news + postimees_news
        all_news.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return render_template('uudised.html', news=all_news[:10])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return render_template('uudised.html', news=[], error=str(e))

@app.route('/syndmused')
def syndmused():
    """Events page - cultural events in Estonia"""
    try:
        # Aggregate events from multiple sources
        culture_events = culture_scraper.get_events(limit=5)
        kultuurikava_events = kultuurikava_scraper.get_events(limit=5)
        piletilevi_events = piletilevi_scraper.get_cultural_events(limit=5)
        
        # Combine all events
        all_events = culture_events + kultuurikava_events + piletilevi_events
        
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
            err_news = err_scraper.get_news(limit=20)
            postimees_news = postimees_scraper.get_news(limit=20)
            news = err_news + postimees_news
            
            for item in news:
                if query in item.get('title', '').lower() or query in item.get('description', '').lower():
                    item['category'] = 'Uudised'
                    results.append(item)
        
        if category in ['all', 'syndmused']:
            culture_events = culture_scraper.get_events(limit=20)
            kultuurikava_events = kultuurikava_scraper.get_events(limit=20)
            piletilevi_events = piletilevi_scraper.get_cultural_events(limit=20)
            events = culture_events + kultuurikava_events + piletilevi_events
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

@app.route('/info')
def info():
    """Information page about the application"""
    return render_template('info.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
