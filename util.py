import re

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