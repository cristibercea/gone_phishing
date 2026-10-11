'''
Added features:
popular_domain_ranking - Return Int with ranking in popular domains, 0 if not  
is_shortened - Binary flag (1/0): If url is shortened
is_punnycode - Binary flag (1/0): If any part of the fqdn is punnycode
suspcious_tld - Binary flag (1/0): If tld is commonly used for phising

TODO:
ADD MORE
'''
import pandas as pd
from features.selector import select_feature
from urllib.parse import urlparse
import tldextract

df = pd.read_csv("databases/popular_domains.csv")

# create dictionary for fast lookup with key: domain, value:ranking

POPULAR_DOMAINS = dict(zip(df["domain"],df["position"]))

SHORTENED_DOMAIN = {
    "bit.ly",
    "tinyurl.com",
    "goo.gl",
    "ow.ly",
    "t.co",
}

TOP_TLDS_BY_PHISING_SCORE = [
    "xin",
    "win",
    "icu",
    "garden",
    "cfd",
    "pro",
    "help",
    "mom",
    "rest",
    "mobi",
    "qpon",
    "live",
    "ink",
    "best",
    "lat",
    "cyou",
    "top",
    "wang",
    "life",
    "homes"
]

@select_feature("popular_domain_ranking")
def popular_domain_ranking(url):
    extract = tldextract.extract(url)
    domain = extract.top_domain_under_public_suffix

    return int(POPULAR_DOMAINS.get(domain,0))



@select_feature("is_shortened")
def is_shortened(url):
    hostname = urlparse(url).hostname

    if not hostname:
        return 0
    
    for domain in SHORTENED_DOMAIN:
        if hostname == domain or hostname.endswith("." + domain):
            return 1
    
    return 0

@select_feature("is_punnycode")
def is_punnycode(url):
    hostname = urlparse(url).hostname or ""
    return int(any(part.startswith("xn--") for part in hostname.split(".")))

@select_feature("suspcious_tld")
def suspcious_tld(url):
    domain_parts = urlparse(url).hostname or ""
    tld = domain_parts.split(".")[-1]
    return int(tld in TOP_TLDS_BY_PHISING_SCORE)


