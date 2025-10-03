import tldextract

def normalize_domain(url_or_domain):
    """
    Return domain.suffix for a URL or domain-like string.
    Examples:
      - 'https://openai.com/about' -> 'openai.com'
      - 'openai.com' -> 'openai.com'
    """
    if not url_or_domain:
        return ""
    ext = tldextract.extract(url_or_domain)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return url_or_domain
