from flask import Blueprint, jsonify, request
from extensions import db
from models import Image

images_bp = Blueprint(
    "images",
    __name__,
    url_prefix="/api/images"
)
@images_bp.route("/", methods=["GET"])
def get_images():
    query = db.select(Image)
    exact_filters = {
        "id": Image.id,
        "listing_id": Image.listing_id,
        "image_url": Image.image_url,
        "image_order": Image.image_order,
    }
    for parameter, column in exact_filters.items():
        value = request.args.get(parameter)
        if value is not None:
            if parameter in [
                "id",
                "listing_id",
                "image_order"
            ]:
                value = int(value)
            query = query.where(
                column == value
            )
    images = db.session.execute(
        query
    ).scalars().all()
    results = []
    for image in images:
        results.append({
            "id": image.id,
            "listing_id": image.listing_id,
            "image_url": image.image_url,
            "image_order": image.image_order
        })

    return jsonify(results)