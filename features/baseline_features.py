'''
Functions for original features from the the LegitPhish dataset
Features:
url_length	-   Total number of characters in the URL.
has_ip_address  -	Binary flag (1/0): whether the URL contains an IP address.
dot_count  -  Number of . characters in the URL.
https_flag	-    Binary flag (1/0): whether the URL uses HTTPS.
url_entropy	-    Shannon entropy of the URL string – higher values indicate more randomness.
token_count	-    Number of tokens/words in the URL.
subdomain_count	-    Number of subdomains in the URL.
query_param_count  -	Number of query parameters (after ?).
tld_length  -	Length of the Top-Level Domain (e.g., "com" = 3).
path_length -	Length of the path part after the domain.
has_hyphen_in_domain	Binary flag (1/0):    whether the domain contains a hyphen (-).
number_of_digits -	Total number of numeric characters in the URL.
tld_popularity	Binary flag (1/0): whether the TLD is popular.
suspicious_file_extension	Binary flag (1/0): indicates if the URL ends with suspicious extensions (e.g., .exe, .zip).
domain_name_length	-    Length of the domain name.
percentage_numeric_chars	-  Percentage of numeric characters in the URL.
'''

from features.selector import select_feature
from urllib.parse import urlparse
from ipaddress import ip_address
from scipy.stats import entropy
from collections import Counter
import re

# To be imporved
POPULAR_TLDS = {
    "com",
    "org",
    "net",
    "edu",
    "gov",
}

SUSPICIOUS_EXTENSIONS = (
    ".exe",
    ".msi",
    ".dll",
    ".elf",
    ".bin",
    ".sh",
    ".ps1",
    ".bat",
    ".cmd",
    ".py",
    ".js",
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".deb",
    ".rpm",
    ".dmg",
    ".pkg",
    ".jar",
    ".apk",
    ".aab",
    ".ipa",
    ".apks",
)


@select_feature("url_length")
def url_length(url):
    return len(url)


@select_feature("has_ip_address")
def has_ip_address(url):
    hostname = urlparse(url).hostname
    try:
        ip_address(hostname)
        return 1
    except ValueError:
        return 0

@select_feature("dot_count")
def dot_count(url):
    return url.count(".")


@select_feature("https_flag")
def https_flag(url):
    return int(url.lower().startswith("https://"))

@select_feature("url_entropy")
def url_entropy(url):
    return float(entropy(list(Counter(url).values()), base = 2))

@select_feature("token_count")
def token_count(url):
    return len(re.split(r"[/.?=&]", url))


@select_feature("subdomain_count")
def subdomain_count(url):
    domain_parts = urlparse(url).netloc
    domain_count = len(domain_parts.split("."))
    # -2, 1 for tld, 1 for host
    return domain_count - 2

@select_feature("query_param_count")
def query_param_count(url):
    query = urlparse(url).query
    return len(query.split("&")) if query else 0 


@select_feature("tld_length")
def tld_length(url):
    domain_parts = urlparse(url).netloc.split(".")
    tld = domain_parts[-1]
    return len(tld)

@select_feature("path_length")
def path_length(url):
    path = urlparse(url).path
    return len(path)


@select_feature("has_hyphen_in_domain")
def has_hyphen_in_domain(url):
    fqdn = urlparse(url).netloc
    return int("-" in fqdn) if fqdn else 0


@select_feature("number_of_digits")
def number_of_digits(url):
    return sum(char.isdigit() for char in url)

@select_feature("tld_popularity")
def tld_popularity(url):
    domain_parts = urlparse(url).netloc.split(".")
    tld = domain_parts[-1]
    return int(tld in POPULAR_TLDS)


@select_feature("suspicious_file_extension")
def suspicious_file_extension(url):
    path = urlparse(url).path
    return int(path.lower().endswith(SUSPICIOUS_EXTENSIONS))

@select_feature("domain_name_length")
def domain_name_length(url):
    domain_parts = urlparse(url).netloc.split(".")
    if len(domain_parts) >= 2:
        domain_name = domain_parts[-2]
    else:
        domain_name = domain_parts[0]
    return len(domain_name)

@select_feature("percentage_numeric_chars")
def percentage_numeric_chars(url):
    number_of_digits = sum(char.isdigit() for char in url)
    percentage = number_of_digits / len(url) * 100
    return percentage
