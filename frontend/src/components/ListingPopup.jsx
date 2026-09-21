import { useEffect, useState } from "react";

function ListingPopup({
    isOpen,
    listingId,
    onClose
}) {
    const [listing, setListing] = useState(null);
    const [error, setError] = useState(null);
    const [loadedListingId, setLoadedListingId] = useState(null);
    useEffect(() => {
        if (!isOpen || !listingId) {
            return;
        }
        const controller =
            new AbortController();
        fetch(
            `http://127.0.0.1:5000/api/listings/${listingId}`,
            {
                signal: controller.signal
            }
        )
            .then(response => {
                if (!response.ok) {
                    throw new Error(
                        "Failed to fetch listing"
                    );
                }
                return response.json();
            })
            .then(data => {
                if (controller.signal.aborted) {
                    return;
                }
                setListing(
                    data.listing || data
                );
                setLoadedListingId(
                    listingId
                );
                setError(
                    null
                );
            })
            .catch(error => {
                if (error.name === "AbortError") {
                    return;
                }
                console.error(
                    "Failed to fetch listing:",
                    error
                );
                setListing(
                    null
                );
                setLoadedListingId(
                    listingId
                );
                setError(
                    "Unable to load this listing."
                );
            });
        return () => {
            controller.abort();
        };
    }, [isOpen, listingId]);
    if (!isOpen) {
        return null;
    }
    const isLoading =
        loadedListingId !== listingId;
    if (isLoading) {
        return (
            <div className="listing-overlay active">
                <div className="listing-popup">
                    <button
                        className="listing-close"
                        onClick={onClose}
                        aria-label="Close listing"
                    >
                        ×
                    </button>
                    <div className="listing-popup-content">
                        <div className="listing-popup-loading">
                            Loading listing...
                        </div>
                    </div>
                </div>
            </div>
        );
    }
    if (error) {
        return (
            <div className="listing-overlay active">
                <div className="listing-backdrop"></div>
                <div className="listing-popup">
                    <button
                        className="listing-close"
                        onClick={onClose}
                        aria-label="Close listing"
                    >
                        ×
                    </button>
                    <div className="listing-popup-content">
                        <div className="listing-popup-loading">
                            {error}
                        </div>
                    </div>
                </div>
            </div>
        );
    }
    if (!listing) {
        return null;
    }
    const displayValue = value => {
        if (
            value === null ||
            value === undefined ||
            value === ""
        ) {
            return "Unspecified";
        }
        return value;
    };
    const title =
        displayValue(listing.title);
    const propertyType =
        displayValue(listing.property_type);
    const city =
        displayValue(listing.city);
    const area =
        displayValue(listing.area);
    const price =
        displayValue(listing.price);
    const currency =
        displayValue(listing.currency);
    const bedrooms =
        displayValue(listing.bedrooms);
    const bathrooms =
        displayValue(listing.bathrooms);
    const size =
        listing.size === null ||
        listing.size === undefined ||
        listing.size === ""
            ? "Unspecified"
            : `${listing.size} m²`;
    const furnished =
        displayValue(listing.furnished);
    const description =
        displayValue(listing.description);
    const sellerName =
        displayValue(listing.seller_name);
    const source =
        displayValue(listing.source);
    const listingUrl =
        displayValue(listing.url);
    const images =
        Array.isArray(listing.images)
            ? listing.images.filter(
                image =>
                    image &&
                    (
                        typeof image === "string" ||
                        image.image_url
                    )
            )
            : [];
    return (
        <div className="listing-overlay active">
            <div className="listing-popup">
                <button
                    className="listing-close"
                    onClick={onClose}
                    aria-label="Close listing"
                >
                    ×
                </button>
                <div className="listing-popup-content">
                    <div className="listing-popup-images">
                        {images.length > 0 ? (
                            <div
                                id="listingCarousel"
                                className="carousel slide"
                                data-bs-ride="carousel"
                                data-bs-interval="4000"
                            >
                                {images.length > 1 && (
                                    <div className="carousel-indicators">
                                        {images.map(
                                            (image, index) => (
                                                <button
                                                    key={index}
                                                    type="button"
                                                    data-bs-target="#listingCarousel"
                                                    data-bs-slide-to={index}
                                                    className={
                                                        index === 0
                                                            ? "active"
                                                            : ""
                                                    }
                                                    aria-current={
                                                        index === 0
                                                            ? "true"
                                                            : undefined
                                                    }
                                                    aria-label={
                                                        `Image ${index + 1}`
                                                    }
                                                ></button>
                                            )
                                        )}
                                    </div>
                                )}
                                <div className="carousel-inner">
                                    {images.map(
                                        (image, index) => {
                                            const imageUrl =
                                                typeof image === "string"
                                                    ? image
                                                    : image.image_url;
                                            return (
                                                <div
                                                    key={index}
                                                    className={
                                                        `carousel-item ${
                                                            index === 0
                                                                ? "active"
                                                                : ""
                                                        }`
                                                    }
                                                >
                                                    <img
                                                        src={imageUrl}
                                                        className="d-block w-100"
                                                        alt={
                                                            `${title} - Image ${index + 1}`
                                                        }
                                                    />
                                                </div>
                                            );
                                        }
                                    )}
                                </div>
                            </div>
                        ) : (
                            <div className="listing-popup-no-images">
                                No images available
                            </div>
                        )}
                    </div>
                    <div className="listing-popup-info">
                        <div className="listing-popup-header">
                            <span className="listing-popup-property-type">
                                {propertyType}
                            </span>
                            <h2>
                                {title}
                            </h2>
                            <div className="listing-popup-location">
                                {area !== "Unspecified"
                                    ? `${area}, ${city}`
                                    : city}
                            </div>
                            <div className="listing-popup-price">
                                {currency} {price}
                            </div>
                        </div>
                        <div className="listing-popup-details">
                            <div className="listing-detail">
                                <span className="detail-label">
                                    Property Type
                                </span>
                                <span className="detail-value">
                                    {propertyType}
                                </span>
                            </div>
                            <div className="listing-detail">
                                <span className="detail-label">
                                    Bedrooms
                                </span>
                                <span className="detail-value">
                                    {bedrooms}
                                </span>
                            </div>
                            <div className="listing-detail">
                                <span className="detail-label">
                                    Bathrooms
                                </span>
                                <span className="detail-value">
                                    {bathrooms}
                                </span>
                            </div>
                            <div className="listing-detail">
                                <span className="detail-label">
                                    Size
                                </span>
                                <span className="detail-value">
                                    {size}
                                </span>
                            </div>
                            <div className="listing-detail">
                                <span className="detail-label">
                                    Furnished
                                </span>
                                <span className="detail-value">
                                    {furnished}
                                </span>
                            </div>
                            <div className="listing-detail">
                                <span className="detail-label">
                                    City
                                </span>
                                <span className="detail-value">
                                    {city}
                                </span>
                            </div>
                        </div>
                    </div>
                    <div className="listing-popup-description">
                        <h3>
                            Description
                        </h3>
                        <p>
                            {description}
                        </p>
                    </div>
                    <div className="listing-popup-footer">
                        <div className="listing-seller">
                            <span className="detail-label">
                                Seller
                            </span>
                            <span className="detail-value">
                                {sellerName}
                            </span>
                        </div>
                        <div className="listing-source">
                            <span className="detail-label">
                                Source
                            </span>
                            <span className="detail-value">
                                {source}
                            </span>
                        </div>
                        {listingUrl !== "Unspecified" ? (
                            <a
                                className="listing-source-button"
                                href={listingUrl}
                                target="_blank"
                                rel="noopener noreferrer"
                            >
                                View Listing
                            </a>
                        ) : (
                            <span className="listing-source-button">
                                View Listing
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ListingPopup;