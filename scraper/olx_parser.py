import re


# ============================================================
# Helpers
# ============================================================

def clean_text(text):
    """
    Normalize whitespace and common punctuation differences.
    Keeps both English and Arabic text intact.
    """

    if not text:
        return ""

    text = str(text)

    # Normalize common Unicode punctuation
    text = text.replace("²", "2")
    text = text.replace("،", ",")
    text = text.replace("؛", ";")
    text = text.replace("ـ", "")

    # Collapse repeated whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip().lower()


def to_int(value):
    """
    Safely convert a matched numeric value to int.
    """

    if value is None:
        return None

    try:
        return int(value)
    except (ValueError, TypeError):
        return None


# ============================================================
# SIZE
# ============================================================

def extract_size(text):
    """
    Extract property size in square meters.

    Examples:
        220 sqm
        220 m2
        220 m²
        220 sq m
        220 square meters
        220 square metre
        220 متر مربع
        220 متر
        مساحة 220
        Total area: 210 sqm
    """

    patterns = [

        # ----------------------------------------------------
        # English / international formats
        # ----------------------------------------------------

        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:sqm|sq\.?\s*m|m2|m²|square\s*meters?|square\s*metres?)\b",

        # Area / size followed by number
        r"\b(?:total\s*)?"
        r"(?:area|size|surface\s*area)"
        r"\s*[:\-]?\s*"
        r"(\d+(?:[.,]\d+)?)\b",

        # ----------------------------------------------------
        # Arabic
        # ----------------------------------------------------

        r"(?:مساحة|المساحة)"
        r"\s*(?:الكلية|الإجمالية)?"
        r"\s*[:\-]?\s*"
        r"(\d+(?:[.,]\d+)?)"
        r"\s*(?:متر\s*مربع|متر|م²|م2)?",

        # Number followed by Arabic square-meter wording
        r"\b(\d+(?:[.,]\d+)?)\s*"
        r"(?:متر\s*مربع|متر|م²|م2)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1)

            value = value.replace(",", ".")

            try:
                return float(value)
            except ValueError:
                continue

    return None


# ============================================================
# BEDROOMS
# ============================================================

def extract_bedrooms(text):
    """
    Extract bedroom count.

    Examples:
        3 bedroom
        3 bedrooms
        3 bed
        3 beds
        3 BR
        Bedrooms: 3
        3 Bedrooms (1 Master)
        3 غرف نوم
        3 غرفة نوم
        3 غرف
        3 غرفة
        غرفتين
    """

    patterns = [

        # ----------------------------------------------------
        # English
        # ----------------------------------------------------

        r"\b(\d+)\s*"
        r"(?:bedrooms?|beds?|br)\b",

        r"\b(?:bedrooms?|beds?|br)"
        r"\s*[:\-]?\s*(\d+)\b",

        # ----------------------------------------------------
        # Arabic
        # ----------------------------------------------------

        r"\b(\d+)\s*"
        r"(?:غرف?\s+نوم|غرف\s+للنوم)\b",

        r"\b(\d+)\s*"
        r"(?:غرف?|غرفة)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return to_int(
                match.group(1)
            )

    # --------------------------------------------------------
    # Arabic written numbers
    # --------------------------------------------------------

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


# ============================================================
# BATHROOMS
# ============================================================

def extract_bathrooms(text):
    """
    Extract bathroom count.

    Examples:
        4 bathroom
        4 bathrooms
        4 bath
        4 baths
        4 BA
        Bathrooms: 4
        4 حمام
        4 حمامات
        حمام واحد
        حمامين
    """

    patterns = [

        # ----------------------------------------------------
        # English
        # ----------------------------------------------------

        r"\b(\d+)\s*"
        r"(?:bathrooms?|baths?|ba)\b",

        r"\b(?:bathrooms?|baths?|ba)"
        r"\s*[:\-]?\s*(\d+)\b",

        # ----------------------------------------------------
        # Arabic
        # ----------------------------------------------------

        r"\b(\d+)\s*"
        r"(?:حمام|حمامات|حمّام|حمّامات)\b"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            return to_int(
                match.group(1)
            )

    # --------------------------------------------------------
    # Arabic written numbers
    # --------------------------------------------------------

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


# ============================================================
# MAIN PARSER
# ============================================================

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


# ============================================================
# TESTS
# ============================================================

if __name__ == "__main__":

    test_descriptions = [

        # ----------------------------------------------------
        # English
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Arabic
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # Mixed Arabic / English
        # ----------------------------------------------------

        (
            "Mixed language",
            """
            Apartment for rent.
            3 Bedrooms
            4 حمامات
            Size: 200 m²
            """
        ),

        # ----------------------------------------------------
        # Real OLX-style examples
        # ----------------------------------------------------

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
            1 Kitchen
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

        result = parse_description(
            description
        )

        print("\n---")
        print(name)
        print(result)

        passed += 1


    print("\n" + "=" * 60)
    print(
        f"Tests executed: {passed}"
    )
    print("=" * 60)