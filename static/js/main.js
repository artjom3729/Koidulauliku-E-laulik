// Koidulauliku E-laulik - Main JavaScript

// Search functionality
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            // Clear previous timeout
            clearTimeout(searchTimeout);
            
            if (query.length < 2) {
                searchResults.classList.remove('show');
                searchResults.innerHTML = '';
                return;
            }
            
            // Debounce search
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 500);
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.remove('show');
            }
        });
    }
});

function performSearch(query) {
    const searchResults = document.getElementById('search-results');
    
    // Show loading
    searchResults.innerHTML = '<div style="padding: 1rem; text-align: center;">Otsin...</div>';
    searchResults.classList.add('show');
    
    // Make API call
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            displaySearchResults(data);
        })
        .catch(error => {
            console.error('Search error:', error);
            searchResults.innerHTML = '<div style="padding: 1rem; text-align: center; color: #dc3545;">Otsingu viga</div>';
        });
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div style="padding: 1rem; text-align: center;">Tulemusi ei leitud</div>';
        return;
    }
    
    let html = '';
    results.forEach(item => {
        const category = item.category || 'Info';
        const title = item.title || 'Pealkiri puudub';
        const description = item.description || item.content || '';
        const link = item.link || '#';
        
        html += `
            <div class="search-result-item" onclick="window.open('${link}', '_blank')">
                <div style="font-size: 0.85rem; color: #00A3E0; font-weight: 600; margin-bottom: 0.25rem;">
                    ${category}
                </div>
                <div style="font-weight: 500; margin-bottom: 0.25rem;">
                    ${title}
                </div>
                ${description ? `<div style="font-size: 0.9rem; color: #666;">${description.substring(0, 100)}...</div>` : ''}
            </div>
        `;
    });
    
    searchResults.innerHTML = html;
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', function() {
    const animatedElements = document.querySelectorAll('.news-item, .event-card, .culture-item, .category-card, .gallery-card');
    const fallbackSvg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="640" height="420">
            <rect width="640" height="420" fill="#f8f1e5"/>
            <rect x="60" y="80" width="520" height="260" rx="20" fill="#0055A4" opacity="0.85"/>
            <text x="50%" y="52%" font-size="30" text-anchor="middle" fill="#ffffff" font-family="Roboto, Arial">Pilt puudub</text>
            <text x="50%" y="67%" font-size="18" text-anchor="middle" fill="#ffffff" font-family="Roboto, Arial">Ajalooline vaade</text>
        </svg>
    `;
    const fallbackImage = `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(fallbackSvg)}`;
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(el);
    });

    const galleryImages = document.querySelectorAll('.gallery-image img');
    galleryImages.forEach(img => {
        img.addEventListener('error', () => {
            if (img.dataset.fallbackApplied) {
                return;
            }
            img.dataset.fallbackApplied = 'true';
            img.src = fallbackImage;
            img.alt = 'Pilt puudub';
        });
    });
});
