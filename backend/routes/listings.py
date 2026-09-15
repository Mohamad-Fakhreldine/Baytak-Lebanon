from difflib import SequenceMatcher

from flask import Blueprint, jsonify, request
from sqlalchemy import func, or_
from sqlalchemy.orm import selectinload

from extensions import db
from models import Listing, Image


listings_bp = Blueprint(
    "listings",
    __name__,
    url_prefix="/api/listings"
)


# ==========================
# LOCATION HELPERS
# ==========================

def normalize_location(value):
    if not value:
        return ""

    return "".join(
        character.lower()
        for character in value.strip()
        if character.isalnum()
    )


def location_similarity(search, location):

    search_normalized = normalize_location(search)
    location_normalized = normalize_location(location)

    if not search_normalized or not location_normalized:
        return 0

    # Exact match
    if search_normalized == location_normalized:
        return 1

    # One contains the other
    if (
        search_normalized in location_normalized
        or location_normalized in search_normalized
    ):
        return 0.9

    # Normal similarity
    normal_score = SequenceMatcher(
        None,
        search_normalized,
        location_normalized
    ).ratio()

    # Vowel-insensitive similarity
    vowels = "aeiou"

    search_without_vowels = "".join(
        character
        for character in search_normalized
        if character not in vowels
    )

    location_without_vowels = "".join(
        character
        for character in location_normalized
        if character not in vowels
    )

    vowel_insensitive_score = SequenceMatcher(
        None,
        search_without_vowels,
        location_without_vowels
    ).ratio()

    return max(
        normal_score,
        vowel_insensitive_score
    )


def get_location_suggestions(search, limit=3):

    search = search.strip()

    # Don't search for extremely short input
    if len(search) < 2:
        return []

    # Get unique cities
    cities = db.session.execute(
        db.select(Listing.city)
        .where(
            Listing.city.is_not(None),
            Listing.city != ""
        )
        .distinct()
    ).scalars().all()

    # Get unique areas
    areas = db.session.execute(
        db.select(Listing.area)
        .where(
            Listing.area.is_not(None),
            Listing.area != ""
        )
        .distinct()
    ).scalars().all()

    # Combine cities and areas into one unique set
    locations = set()

    for location in cities:
        location = location.strip()

        if location:
            locations.add(location)

    for location in areas:
        location = location.strip()

        if location:
            locations.add(location)

    # Score every possible location
    scored_locations = []

    for location in locations:

        score = location_similarity(
            search,
            location
        )

        if score >= 0.45:
            scored_locations.append(
                (
                    score,
                    location
                )
            )

    # Best match first
    scored_locations.sort(
        key=lambda item: (
            -item[0],
            item[1].lower()
        )
    )

    # Return only the best 3
    return [
        location
        for _, location in scored_locations[:limit]
    ]


# ==========================
# LOCATION SUGGESTIONS
# ==========================

@listings_bp.route("/locations", methods=["GET"])
def get_location_suggestions_route():

    search = request.args.get(
        "q",
        default="",
        type=str
    ).strip()

    if len(search) < 2:
        return jsonify({
            "locations": []
        })

    suggestions = get_location_suggestions(
        search,
        limit=3
    )

    return jsonify({
        "locations": suggestions
    })


# ==========================
# PROPERTY TYPES
# ==========================

@listings_bp.route("/property-types", methods=["GET"])
def get_property_types():

    property_types = db.session.execute(
        db.select(
            Listing.property_type
        )
        .where(
            Listing.property_type.is_not(None),
            Listing.property_type != ""
        )
        .distinct()
        .order_by(
            Listing.property_type
        )
    ).scalars().all()

    return jsonify({
        "property_types": property_types
    })


# ==========================
# SINGLE LISTING
# ==========================

@listings_bp.route("/<int:listing_id>", methods=["GET"])
def get_single_listing(listing_id):

    listing = db.session.execute(
        db.select(Listing)
        .options(
            selectinload(Listing.images)
        )
        .where(
            Listing.id == listing_id
        )
    ).scalar_one_or_none()

    if listing is None:
        return jsonify({
            "error": "Listing not found"
        }), 404

    images = []

    for image in listing.images:

        images.append({
            "id": image.id,
            "listing_id": image.listing_id,
            "image_url": image.image_url,
            "image_order": image.image_order
        })

    result = {
        "id": listing.id,
        "title": listing.title,
        "description": listing.description,
        "source": listing.source,
        "external_id": listing.external_id,
        "url": listing.url,
        "price": listing.price,
        "currency": listing.currency,
        "city": listing.city,
        "area": listing.area,
        "property_type": listing.property_type,
        "bedrooms": listing.bedrooms,
        "bathrooms": listing.bathrooms,
        "size": listing.size,
        "furnished": listing.furnished,
        "seller_name": listing.seller_name,
        "scraped_date": listing.scraped_date,
        "images": images
    }

    return jsonify({
        "listing": result
    })


# ==========================
# LISTINGS
# ==========================

@listings_bp.route("/", methods=["GET"])
def get_listings():

    # ==========================
    # PAGINATION
    # ==========================

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    per_page = 50

    if page < 1:
        page = 1

    # ==========================
    # BASE QUERY
    # ==========================

    query = db.select(Listing).options(
        selectinload(Listing.images)
    )

    # ==========================
    # EXACT-MATCH FILTERS
    # ==========================

    exact_filters = {
        "id": Listing.id,
        "title": Listing.title,
        "description": Listing.description,
        "source": Listing.source,
        "external_id": Listing.external_id,
        "url": Listing.url,
        "currency": Listing.currency,
        "seller_name": Listing.seller_name,
        "scraped_date": Listing.scraped_date,
    }

    for parameter, column in exact_filters.items():

        value = request.args.get(parameter)

        if value is not None:
            query = query.where(
                column == value
            )

    # ==========================
    # FURNISHED FILTER
    # ==========================

    furnished = request.args.get(
        "furnished",
        default="any",
        type=str
    ).strip().lower()

    if furnished == "furnished":

        query = query.where(
            Listing.furnished == "Fully Furnished"
        )

    elif furnished == "appliances_only":

        query = query.where(
            Listing.furnished == "Appliances only"
        )

    elif furnished == "unfurnished":

        query = query.where(
            Listing.furnished == "Unfurnished"
        )

    # ==========================
    # LOCATION FILTER
    # ==========================

    location = request.args.get(
        "location"
    )

    if location:

        location = location.strip()

        if location:
            query = query.where(
                or_(
                    Listing.city == location,
                    Listing.area == location
                )
            )

    # ==========================
    # PROPERTY TYPE
    # ==========================

    property_type = request.args.get(
        "property_type"
    )

    if property_type:

        query = query.where(
            Listing.property_type == property_type
        )

    # ==========================
    # BEDROOMS
    # ==========================

    bedrooms = request.args.get(
        "bedrooms"
    )

    if bedrooms is not None:

        query = query.where(
            Listing.bedrooms == int(
                bedrooms
            )
        )

    # ==========================
    # BATHROOMS
    # ==========================

    bathrooms = request.args.get(
        "bathrooms"
    )

    if bathrooms is not None:

        query = query.where(
            Listing.bathrooms == int(
                bathrooms
            )
        )

    # ==========================
    # PRICE RANGE
    # ==========================

    min_price = request.args.get(
        "min_price"
    )

    if min_price is not None:

        query = query.where(
            Listing.price >= float(
                min_price
            )
        )

    max_price = request.args.get(
        "max_price"
    )

    if max_price is not None:

        query = query.where(
            Listing.price <= float(
                max_price
            )
        )

    # ==========================
    # SIZE RANGE
    # ==========================

    min_size = request.args.get(
        "min_size"
    )

    if min_size is not None:

        query = query.where(
            Listing.size >= float(
                min_size
            )
        )

    max_size = request.args.get(
        "max_size"
    )

    if max_size is not None:

        query = query.where(
            Listing.size <= float(
                max_size
            )
        )

    # ==========================
    # BEDROOM RANGE
    # ==========================

    min_bedrooms = request.args.get(
        "min_bedrooms"
    )

    if min_bedrooms is not None:

        query = query.where(
            Listing.bedrooms >= int(
                min_bedrooms
            )
        )

    # ==========================
    # BATHROOM RANGE
    # ==========================

    min_bathrooms = request.args.get(
        "min_bathrooms"
    )

    if min_bathrooms is not None:

        query = query.where(
            Listing.bathrooms >= int(
                min_bathrooms
            )
        )

    # ==========================
    # IMAGE FILTERS
    # ==========================

    image_url = request.args.get(
        "image_url"
    )

    if image_url is not None:

        query = query.where(
            Listing.images.any(
                Image.image_url == image_url
            )
        )

    image_order = request.args.get(
        "image_order"
    )

    if image_order is not None:

        query = query.where(
            Listing.images.any(
                Image.image_order == int(
                    image_order
                )
            )
        )

    image_id = request.args.get(
        "image_id"
    )

    if image_id is not None:

        query = query.where(
            Listing.images.any(
                Image.id == int(
                    image_id
                )
            )
        )

    # ==========================
    # COUNT MATCHING LISTINGS
    # ==========================

    count_query = db.select(
        func.count()
    ).select_from(
        query.order_by(None).subquery()
    )

    total = db.session.execute(
        count_query
    ).scalar()

    # ==========================
    # COUNT SOURCES
    # ==========================

    filtered_sources_query = db.select(
        func.count(
            func.distinct(
                Listing.source
            )
        )
    ).select_from(
        query.order_by(None).subquery()
    )

    total_sources = db.session.execute(
        filtered_sources_query
    ).scalar()

    # ==========================
    # TOTAL PAGES
    # ==========================

    pages = (
        total + per_page - 1
    ) // per_page

    # ==========================
    # PAGINATION
    # ==========================

    offset = (
        page - 1
    ) * per_page

    query = query.limit(
        per_page
    ).offset(
        offset
    )

    # ==========================
    # EXECUTE
    # ==========================

    listings = db.session.execute(
        query
    ).scalars().all()

    # ==========================
    # BUILD RESPONSE
    # ==========================

    results = []

    for listing in listings:

        images = []

        for image in listing.images:

            images.append({
                "id": image.id,
                "listing_id": image.listing_id,
                "image_url": image.image_url,
                "image_order": image.image_order
            })

        results.append({
            "id": listing.id,
            "title": listing.title,
            "description": listing.description,
            "source": listing.source,
            "external_id": listing.external_id,
            "url": listing.url,
            "price": listing.price,
            "currency": listing.currency,
            "city": listing.city,
            "area": listing.area,
            "property_type": listing.property_type,
            "bedrooms": listing.bedrooms,
            "bathrooms": listing.bathrooms,
            "size": listing.size,
            "furnished": listing.furnished,
            "seller_name": listing.seller_name,
            "scraped_date": listing.scraped_date,
            "images": images
        })

    # ==========================
    # RESPONSE
    # ==========================

    return jsonify({
        "listings": results,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
            "sources": total_sources
        }
    })