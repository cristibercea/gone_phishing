from urllib.parse import urlparse
import re


URL_MODEL_FEATURES = [
    'DomainLength', 'IsDomainIP', 'TLDLength', 'NoOfSubDomain', 'HasObfuscation',
    'NoOfObfuscatedChar', 'ObfuscationRatio', 'NoOfLettersInURL', 'LetterRatioInURL',
    'NoOfDegitsInURL', 'DegitRatioInURL', 'NoOfEqualsInURL', 'NoOfQMarkInURL',
    'NoOfAmpersandInURL', 'NoOfOtherSpecialCharsInURL', 'SpacialCharRatioInURL', 'IsHTTPS'
]


def extract_features(url: str) -> dict:
    """
    Extracts Phishing URL Model features from a given URL
    :param url: the url to extract features from
    :return: features dictionary for Phishing URL Model of the given URL
    """
    # TODO
    u = str(url)
    p = urlparse(u if '://' in u else 'http://' + u)
    host = p.netloc.split(':')[0]
    parts = host.split('.')
    tld = parts[-1] if len(parts) > 1 else ''
    domain = host
    subdomains = max(len(parts) - 2, 0)

    netloc_clean = urlparse(u).netloc
    if netloc_clean.startswith('www.'):
        netloc_clean = netloc_clean[4:]  # strip 4 chars, not "www"
    n_letters = sum(c.isalpha() for c in netloc_clean + p.path + p.query)

    n_digits  = sum(c.isdigit() for c in u)
    n_len     = max(len(u), 1)

    structured = set('.=?&/:-_#%!*()\'[]<>"\\|`{}^'.replace(' ', ''))
    other_special = sum(1 for c in u
                        if not c.isalnum() and c not in structured)

    n_obfuscated = u.count('%')
    has_ip = int(bool(re.match(r'^\d{1,3}(\.\d{1,3}){3}$', host)))

    return {
        'DomainLength': len(domain),
        'IsDomainIP': has_ip,
        'TLDLength': len(tld),
        'NoOfSubDomain': subdomains,
        'HasObfuscation': int(n_obfuscated > 0),
        'NoOfObfuscatedChar': n_obfuscated,
        'ObfuscationRatio': n_obfuscated / n_len,
        'NoOfLettersInURL': n_letters,
        'LetterRatioInURL': n_letters / n_len,
        'NoOfDegitsInURL': n_digits,
        'DegitRatioInURL': n_digits / n_len,
        'NoOfEqualsInURL': u.count('='),
        'NoOfQMarkInURL': u.count('?'),
        'NoOfAmpersandInURL': u.count('&'),
        'NoOfOtherSpecialCharsInURL': other_special,
        'SpacialCharRatioInURL': other_special / n_len,
        'IsHTTPS': int(p.scheme == 'https'),
    }