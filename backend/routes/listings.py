from flask import Blueprint, jsonify, request

from extensions import db
from models import Listing, Image


listings_bp = Blueprint(
    "listings",
    __name__,
    url_prefix="/api/listings"
)


@listings_bp.route("/", methods=["GET"])
def get_listings():

    # ==========================
    # BASE QUERY
    # ==========================

    query = db.select(Listing)

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
        "city": Listing.city,
        "area": Listing.area,
        "address": Listing.address,
        "property_type": Listing.property_type,
        "furnished": Listing.furnished,
        "seller_name": Listing.seller_name,
        "scraped_date": Listing.scraped_date,
    }

    for parameter, column in exact_filters.items():

        value = request.args.get(parameter)

        if value is not None:
            query = query.where(column == value)

    # ==========================
    # NUMERIC EXACT-MATCH FILTERS
    # ==========================

    bedrooms = request.args.get("bedrooms")

    if bedrooms is not None:
        query = query.where(
            Listing.bedrooms == int(bedrooms)
        )

    bathrooms = request.args.get("bathrooms")

    if bathrooms is not None:
        query = query.where(
            Listing.bathrooms == int(bathrooms)
        )

    # ==========================
    # PRICE RANGE FILTERS
    # ==========================

    min_price = request.args.get("min_price")

    if min_price is not None:
        query = query.where(
            Listing.price >= float(min_price)
        )

    max_price = request.args.get("max_price")

    if max_price is not None:
        query = query.where(
            Listing.price <= float(max_price)
        )

    # ==========================
    # SIZE RANGE FILTERS
    # ==========================

    min_size = request.args.get("min_size")

    if min_size is not None:
        query = query.where(
            Listing.size >= float(min_size)
        )

    max_size = request.args.get("max_size")

    if max_size is not None:
        query = query.where(
            Listing.size <= float(max_size)
        )

    # ==========================
    # BEDROOM RANGE FILTER
    # ==========================

    min_bedrooms = request.args.get("min_bedrooms")

    if min_bedrooms is not None:
        query = query.where(
            Listing.bedrooms >= int(min_bedrooms)
        )

    # ==========================
    # BATHROOM RANGE FILTER
    # ==========================

    min_bathrooms = request.args.get("min_bathrooms")

    if min_bathrooms is not None:
        query = query.where(
            Listing.bathrooms >= int(min_bathrooms)
        )

    # ==========================
    # IMAGE FILTERS
    # ==========================

    image_url = request.args.get("image_url")

    if image_url is not None:
        query = query.where(
            Listing.images.any(
                Image.image_url == image_url
            )
        )

    image_order = request.args.get("image_order")

    if image_order is not None:
        query = query.where(
            Listing.images.any(
                Image.image_order == int(image_order)
            )
        )

    image_id = request.args.get("image_id")

    if image_id is not None:
        query = query.where(
            Listing.images.any(
                Image.id == int(image_id)
            )
        )

    # ==========================
    # EXECUTE QUERY
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
            "address": listing.address,
            "property_type": listing.property_type,
            "bedrooms": listing.bedrooms,
            "bathrooms": listing.bathrooms,
            "size": listing.size,
            "furnished": listing.furnished,
            "seller_name": listing.seller_name,
            "scraped_date": listing.scraped_date,
            "images": images
        })

    return jsonify(results)