from urllib.parse import quote

def djangology_quote(s):
    return quote(s.replace(" ", "_").encode('utf-8'))

def djangology_unquote(s):
    return s.replace("_", " ")

def djangology_url_special_chars(s):
    specialChars = ["_"]
    if any(ext in s for ext in specialChars):
        return True
    return False