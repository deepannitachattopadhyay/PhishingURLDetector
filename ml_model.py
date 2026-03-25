import re
from urllib.parse import urlparse

def extract(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path

    suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update',
                           'banking', 'confirm', 'password', 'signin', 'ebayisapi',
                           'webscr', 'free', 'lucky', 'bonus', 'gift']

    return {
        'url_length': len(url),
        'count_dots': url.count('.'),
        'has_at': int('@' in url),
        'has_dash': int('-' in url),
        'has_double_slash': int('//' in url[8:]),
        'https_present': int(url.startswith('https')),
        'is_ip_address': int(bool(re.match(r"\d+\.\d+\.\d+\.\d+", domain))),
        'count_suspicious_chars': sum(url.count(c) for c in ['!', '$', '%', '&', '*', '?']),
        'domain_length': len(domain),
        'path_length': len(path),
        'count_hyphens': url.count('-'),
        'count_slash': url.count('/'),
        'count_digits': sum(c.isdigit() for c in url),
        'count_subdomains': domain.count('.'),
        'has_port': int(':' in domain),
        'has_http_in_path': int('http' in path.lower()),
        'count_suspicious_keywords': sum(kw in url.lower() for kw in suspicious_keywords),
        'ratio_digits': sum(c.isdigit() for c in url) / max(len(url), 1),
        'has_shortening': int(any(s in domain for s in ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly'])),
        'count_equals': url.count('='),
        'count_ampersand': url.count('&'),
    }

features_columns = [
    'url_length', 'count_dots', 'has_at', 'has_dash', 'has_double_slash',
    'https_present', 'is_ip_address', 'count_suspicious_chars',
    'domain_length', 'path_length', 'count_hyphens', 'count_slash',
    'count_digits', 'count_subdomains', 'has_port', 'has_http_in_path',
    'count_suspicious_keywords', 'ratio_digits', 'has_shortening',
    'count_equals', 'count_ampersand'
]