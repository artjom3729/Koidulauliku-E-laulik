# Security Policy

## Supported Versions

This project uses the following versions with their security status:

| Dependency | Version | Security Status |
| ---------- | ------- | --------------- |
| Flask | 3.0.0 | ✅ Secure |
| beautifulsoup4 | 4.12.2 | ✅ Secure |
| requests | 2.31.0 | ✅ Secure |
| Werkzeug | 3.0.1 | ✅ Secure |
| Scrapy | 2.11.2 | ⚠️ See Known Issues |
| lxml | 4.9.3 | ✅ Secure |

## Known Security Issues

### Scrapy Denial of Service Vulnerability

**Status:** ⚠️ Known Issue - No Patch Available

**Details:**
- **Affected Versions:** Scrapy >= 0.7, <= 2.14.1 (includes our version 2.11.2)
- **Vulnerability Type:** Denial of Service (DoS)
- **Severity:** Medium
- **Patched Version:** Not available (as of January 2026)

**Risk Assessment:**
The risk is **LOW** for this application because:
1. The application is not a public-facing scraping service
2. Scrapy is used only for controlled, trusted sources
3. Mitigations are in place to limit exposure
4. Fallback data ensures service continuity

### Mitigation Strategies

The following measures have been implemented to mitigate the DoS risk:

#### 1. Rate Limiting
```python
# scrapy_settings.py
CONCURRENT_REQUESTS = 8  # Limit concurrent requests
DOWNLOAD_DELAY = 1       # 1 second delay between requests
```

#### 2. AutoThrottle
```python
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 3
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
```

#### 3. Request Timeouts
All BeautifulSoup scrapers use 10-second timeouts:
```python
response = requests.get(url, timeout=10)
```

#### 4. Graceful Degradation
- All scrapers have fallback sample data
- Application continues to work even if scraping fails
- Error handling prevents cascading failures

#### 5. HTTP Caching
```python
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 3600
```

## Fixed Vulnerabilities

The following vulnerabilities have been patched by using Scrapy 2.11.2:

### ✅ Authorization Header Leakage (Fixed in 2.11.2)
- **CVE:** Authorization header leaks on same-domain but cross-origin redirects
- **Impact:** High - Could expose authentication credentials
- **Status:** Fixed

### ✅ Authorization Header Leakage on Cross-Domain (Fixed in 2.11.1)
- **Impact:** High - Authorization headers leaked during cross-domain redirects
- **Status:** Fixed

### ✅ Decompression Bomb (Fixed in 2.11.1)
- **Impact:** High - Could cause DoS through malicious compressed responses
- **Status:** Fixed

### ✅ ReDoS in XMLFeedSpider (Fixed in 2.11.1)
- **Impact:** Medium - Regular expression DoS vulnerability
- **Status:** Fixed

## Security Recommendations

### For Development
1. Keep dependencies updated regularly
2. Monitor security advisories for Scrapy
3. Test fallback mechanisms periodically
4. Review error logs for suspicious patterns

### For Deployment
1. Use a production WSGI server (e.g., Gunicorn, uWSGI)
2. Enable HTTPS for all external communications
3. Implement rate limiting at the application level
4. Monitor resource usage (CPU, memory, network)
5. Set up alerts for unusual scraping behavior

### For Production Use
```python
# Recommended production settings
FLASK_DEBUG=False
CONCURRENT_REQUESTS=4  # Lower for production
DOWNLOAD_DELAY=2       # Higher delay for politeness
```

## Reporting Security Issues

If you discover a security vulnerability in this application:

1. **Do NOT** open a public GitHub issue
2. Contact the maintainers privately
3. Provide detailed information about the vulnerability
4. Allow reasonable time for a fix before public disclosure

## Security Updates

This document will be updated as:
- New vulnerabilities are discovered
- Patches become available
- Mitigation strategies are improved

**Last Updated:** January 26, 2026

---

## References

- [Scrapy Security Advisories](https://github.com/scrapy/scrapy/security/advisories)
- [Flask Security](https://flask.palletsprojects.com/en/3.0.x/security/)
- [OWASP Top Ten](https://owasp.org/www-project-top-ten/)
