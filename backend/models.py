from sqlalchemy import ForeignKey, String, Text, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from extensions import db


# ==========================
# LISTING MODEL
# ==========================

class Listing(db.Model):
    __tablename__ = "listings"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text
    )

    source: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    external_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    price: Mapped[float | None]

    currency: Mapped[str | None] = mapped_column(
        String
    )

    city: Mapped[str | None] = mapped_column(
        String
    )

    area: Mapped[str | None] = mapped_column(
        String
    )

    property_type: Mapped[str | None] = mapped_column(
        String
    )

    bedrooms: Mapped[int | None]

    bathrooms: Mapped[int | None]

    size: Mapped[float | None]

    furnished: Mapped[str | None] = mapped_column(
        String
    )

    seller_name: Mapped[str | None] = mapped_column(
        String
    )

    scraped_date: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    # ==========================
    # RELATIONSHIP
    # ==========================

    images: Mapped[list["Image"]] = relationship(
        back_populates="listing",
        cascade="all, delete-orphan"
    )

    # ==========================
    # CONSTRAINTS / INDEXES
    # ==========================

    __table_args__ = (
        UniqueConstraint(
            "source",
            "external_id",
            name="uq_listings_source_external_id"
        ),

        Index(
            "ix_listings_property_type",
            "property_type"
        ),

        Index(
            "ix_listings_price",
            "price"
        ),

        Index(
            "ix_listings_size",
            "size"
        ),

        Index(
            "ix_listings_furnished",
            "furnished"
        ),

        Index(
            "ix_listings_furnished_property_type",
            "furnished",
            "property_type"
        ),
    )


# ==========================
# IMAGE MODEL
# ==========================

class Image(db.Model):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    listing_id: Mapped[int] = mapped_column(
        ForeignKey("listings.id"),
        nullable=False
    )

    image_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    image_order: Mapped[int | None]

    # ==========================
    # RELATIONSHIP
    # ==========================

    listing: Mapped["Listing"] = relationship(
        back_populates="images"
    )