import re, ast
import unicodedata

def extract_numbers(instance_id: str) -> str:
    # Extract all the numbers from the instance_id"
    if instance_id is None:
        return None
    match = re.search(r'\d+', instance_id)
    if match:
        return match.group(0)
    
def slugify(text: str, remove_words: list[str] = None) -> str:

    # Normalize unicode to decompose accents (NFD = Normalization Form Decomposed)
    # Then remove combining characters to strip accents
    text = unicodedata.normalize('NFD', text)
    text = ''.join(char for char in text if unicodedata.category(char) != 'Mn')
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove apostrophes - both types:
    # U+0027 = APOSTROPHE (straight ')
    # U+2019 = RIGHT SINGLE QUOTATION MARK (curly ')
    text = text.replace(chr(0x0027), "").replace(chr(0x2019), "")
    
    # Remove specified words if provided
    if remove_words:
        pattern = r'\b(' + '|'.join(map(re.escape, remove_words)) + r')\b'
        text = re.sub(pattern, '', text)
    
    # Replace all non-alphanumeric characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    
    # Collapse multiple hyphens into one
    text = re.sub(r'-+', '-', text)
    
    # Trim leading/trailing hyphens
    return text.strip('-')

TRANSFORMATIONS = {
    "extractID": extract_numbers,
    "slugify": slugify
}

def split_address(address: str) -> dict:
    if address == "" or address is None:
        return {}
    if isinstance(address, dict):
        return address  # Already split
    return {
        "streetAddress": extract_street_address(address),
        "addressLocality": extract_locality(address),
        "addressRegion": extract_region(address),
        "postalCode": extract_postal_code(address),
        "addressCountry": "CA"
    }

def extract_street_address(address: str) -> str:
    # Try to extract street address before the first comma
    street_address = address
    split = address.split(',')
    if split[0] and split[0] != address:
        street_address = split[0].strip()
    # If no comma, try to find common street suffixes
    else:
        for sep in ['street', 'Street', 'St.', 'st.']:
            split = address.split(sep)
            if len(split) > 1:
                street_address = split[0] + sep
                break   
    return street_address     

def extract_region(address: str) -> str:
    # Canadian province codes
    match = re.search(r'\b(BC|AB|ON|QC|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b', address)
    if match:
        return match.group(0)

def extract_postal_code(address: str) -> str:
    # Canadian postal code pattern: A1A 1A1 or A1A1A1
    match = re.search(r'\b[ABCEGHJ-NPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d\b', address, re.IGNORECASE)
    if match:
        postal_code = match.group(0).upper()
        return postal_code
    return None

def extract_locality(address: str) -> str:
    # Try to match "street, locality, province" pattern first
    split = [part.strip() for part in address.split(',')]
    if len(split) >= 3:
        # street, locality, province/postal
        locality = split[1]
        return locality
    else:
        # fallback: try to find the locality before the province code
        match = re.search(r'\b([A-Za-z\s]+)\s+(BC|AB|ON|QC|MB|SK|NS|NB|NL|PE|YT|NT|NU)\b', address)
        if match:
            locality = match.group(1).strip()
            return locality
    return None

def add_additional_info(event: dict, additional_info: dict) -> dict:
    # loop through additional_info keys and add to event if not present
    for key, value in additional_info.items():
        if event.get(key) is None and value is not None:
            placeholders = extract_placeholders(value)
            for placeholder in placeholders:
                if "(" in placeholder and ")" in placeholder:
                    expr = ast.parse(placeholder, mode='eval').body
                    args = []
                    for a in expr.args:
                        try:
                            args.append(ast.literal_eval(a))
                        except Exception:
                            args.append(ast.unparse(a))
                    arg = args[0] # only first arg supported
                    kwargs = {}
                    for kw in expr.keywords:
                        try:
                            kwargs[kw.arg] = ast.literal_eval(kw.value)
                        except Exception:
                            kwargs[kw.arg] = ast.unparse(kw.value)
                    func_name = expr.func.id
                    func = TRANSFORMATIONS.get(func_name)
                    if func:
                        arg_value = event.get(arg)
                        if arg_value is not None:
                            transformed = func(arg_value, **kwargs)
                            value = value.replace(f"{{{placeholder}}}", str(transformed))
                else:
                    placeholder_value = event.get(placeholder)
                    if placeholder_value:
                        value = value.replace(f"{{{placeholder}}}", str(placeholder_value))
            event[key] = value
    return event

def extract_placeholders(s: str) -> list[str]:
    # find all substrings inside {}
    return re.findall(r"\{([^}]+)\}", s)

def replace_empty_with_null(obj):
    if isinstance(obj, dict):
        return {k: replace_empty_with_null(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [replace_empty_with_null(v) for v in obj]
    elif obj == "":
        return None
    else:
        return obj

if __name__ == "__main__":
    # Example usage
    address = "453 St. Francois-Xavier, Montreal, QC, HZY 2T1"
    split = split_address(address)
    print(split)
    print(slugify("The Quick Brown Fox Jumps Over The Lazy Dog", ["the", "over"])) #> "quick-brown-fox-jumps-lazy-dog"