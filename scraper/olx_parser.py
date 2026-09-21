import re

def clean_text(text):
    """Normalize whitespace and common punctuation differences."""
    if not text:
        return ""
    text = str(text)
    text = text.replace("²", "2")
    text = text.replace("،", ",")
    text = text.replace("؛", ";")
    text = text.replace("ـ", "")
    return re.sub(r"\s+", " ", text).strip().lower()

def to_int(value):
    """Safely convert a value to an integer."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def find_first_match(text, patterns):
    """Return the first regex match found across a list of patterns."""
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def extract_size(text):
    """Extract property size in square meters."""
    patterns = [
        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:sqm|sq\.?\s*m|m2|m²|square\s*meters?|square\s*metres?)\b",
        r"\b(?:total\s*)?"
        r"(?:area|size|surface\s*area)"
        r"\s*[:\-]?\s*"
        r"(\d+(?:[.,]\d+)?)\b",
        r"(?:مساحة|المساحة)"
        r"\s*(?:الكلية|الإجمالية)?"
        r"\s*[:\-]?\s*"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*(?:متر\s*مربع|متر|م²|م2)?",
        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:متر\s*مربع|متر|م²|م2)\b"
    ]
    value = find_first_match(text, patterns)
    if value is None:
        return None
    try:
        return float(value.replace(",", "."))
    except ValueError:
        return None

def extract_bedrooms(text):
    """Extract bedroom count."""
    patterns = [
        r"\b(\d+)\s*(?:bedrooms?|beds?|br)\b",
        r"\b(?:bedrooms?|beds?|br)"
        r"\s*[:\-]?\s*(\d+)\b",
        r"\b(\d+)\s*"
        r"(?:غرف?\s+نوم|غرف\s+للنوم)\b",
        r"\b(\d+)\s*"
        r"(?:غرف?|غرفة)\b"
    ]
    value = find_first_match(text, patterns)
    if value is not None:
        return to_int(value)
    arabic_numbers = {
        "غرفة واحدة": 1,
        "غرفة": 1,
        "غرفتين": 2,
        "غرفتان": 2,
        "ثلاث غرف": 3,
        "ثلاثة غرف": 3,
        "أربع غرف": 4,
        "اربعة غرف": 4,
        "خمس غرف": 5,
        "خمسة غرف": 5,
        "ست غرف": 6,
        "ستة غرف": 6
    }
    for phrase, number in arabic_numbers.items():
        if phrase in text:
            return number
    return None

def extract_bathrooms(text):
    """Extract bathroom count."""
    patterns = [
        r"\b(\d+)\s*(?:bathrooms?|baths?|ba)\b",
        r"\b(?:bathrooms?|baths?|ba)"
        r"\s*[:\-]?\s*(\d+)\b",
        r"\b(\d+)\s*"
        r"(?:حمام|حمامات|حمّام|حمّامات)\b"
    ]
    value = find_first_match(text, patterns)
    if value is not None:
        return to_int(value)
    arabic_numbers = {
        "حمام واحد": 1,
        "حمام": 1,
        "حمامين": 2,
        "ثلاث حمامات": 3,
        "ثلاثة حمامات": 3,
        "أربع حمامات": 4,
        "اربعة حمامات": 4,
        "خمس حمامات": 5,
        "خمسة حمامات": 5,
        "ست حمامات": 6,
        "ستة حمامات": 6
    }
    for phrase, number in arabic_numbers.items():
        if phrase in text:
            return number
    return None

def parse_description(description):
    """
    Parse useful property information from a listing description.
    Returns:
        {
            "bedrooms": int | None,
            "bathrooms": int | None,
            "size": float | None
        }
    """
    result = {
        "bedrooms": None,
        "bathrooms": None,
        "size": None
    }
    if not description:
        return result
    text = clean_text(description)
    result["size"] = extract_size(text)
    result["bedrooms"] = extract_bedrooms(text)
    result["bathrooms"] = extract_bathrooms(text)
    return result

if __name__ == "__main__":
    test_descriptions = [
        (
            "English standard",
            """
            Beautiful apartment with 3 bedrooms and 2 bathrooms.
            Total area: 220 sqm.
            """
        ),
        (
            "English labels",
            """
            Bedrooms: 4
            Bathrooms: 3
            Size: 180 m2
            """
        ),
        (
            "English shorthand",
            """
            Spacious 2 BR / 2 BA apartment, 150 sq m.
            """
        ),
        (
            "English detailed listing",
            """
            The apartment consists of:
            Total area: 210 sqm
            Bedrooms: 3 (1 Master)
            Bathrooms: 3
            """
        ),
        (
            "Arabic standard",
            """
            شقة بمساحة 180 متر مربع
            مؤلفة من 3 غرف نوم و 2 حمام
            """
        ),
        (
            "Arabic short",
            """
            مساحة 150 متر
            3 غرف و 2 حمامات
            """
        ),
        (
            "Arabic written numbers",
            """
            شقة مؤلفة من ثلاث غرف نوم
            وحمامين ومساحة 160 متر مربع
            """
        ),
        (
            "Mixed language",
            """
            Apartment for rent.
            3 Bedrooms
            4 حمامات
            Size: 200 m²
            """
        ),
        (
            "OLX Rawche example",
            """
            Property Details:

            - 220 sqm
            - 3 Bedrooms (including 1 Master Suite)
            - 4 Bathrooms
            - Spacious Living & Dining Area
            """
        ),
        (
            "OLX Hamra example",
            """
            Size : 130 m2

            This Apartment consists of:

            - 1 Master bedroom
            - 1 Regular Bedroom
            - 3 Bathrooms
            """
        ),
        (
            "OLX Dekwaneh example",
            """
            Size: 125 Square Meters

            1 Salon
            1 Dining Room
            2 Bedrooms
            2 Bathrooms
            """
        ),
        (
            "OLX Arabic office example",
            """
            مساحة المكتب حوالي 60 متر مربع.
            مؤلف من 2 غرفة وصالة استقبال كبيرة.
            و مطبخ و حمام.
            """
        )
    ]
    print("=" * 60)
    print("OLX DESCRIPTION PARSER TEST")
    print("=" * 60)
    passed = 0
    for name, description in test_descriptions:
        result = parse_description(description)
        print("\n---")
        print(name)
        print(result)
        passed += 1
    print("\n" + "=" * 60)
    print(f"Tests executed: {passed}")
    print("=" * 60)