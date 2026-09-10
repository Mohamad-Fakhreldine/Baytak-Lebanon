import placeholderImage from "../assets/placeholder.png";

function ListingPopup({ isOpen, onClose }) {
    return (
        <div className={`listing-overlay ${isOpen ? "active" : ""}`}>
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

                        <div
                            id="listingCarousel"
                            className="carousel slide"
                            data-bs-ride="carousel"
                            data-bs-interval="4000"
                        >

                            <div className="carousel-indicators">

                                <button
                                    type="button"
                                    data-bs-target="#listingCarousel"
                                    data-bs-slide-to="0"
                                    className="active"
                                    aria-current="true"
                                    aria-label="Image 1"
                                ></button>

                                <button
                                    type="button"
                                    data-bs-target="#listingCarousel"
                                    data-bs-slide-to="1"
                                    aria-label="Image 2"
                                ></button>

                                <button
                                    type="button"
                                    data-bs-target="#listingCarousel"
                                    data-bs-slide-to="2"
                                    aria-label="Image 3"
                                ></button>

                            </div>

                            <div className="carousel-inner">

                                <div className="carousel-item active">
                                    <img
                                        src={placeholderImage}
                                        className="d-block w-100"
                                        alt="Property"
                                    />
                                </div>

                                <div className="carousel-item">
                                    <img
                                        src={placeholderImage}
                                        className="d-block w-100"
                                        alt="Property"
                                    />
                                </div>

                                <div className="carousel-item">
                                    <img
                                        src={placeholderImage}
                                        className="d-block w-100"
                                        alt="Property"
                                    />
                                </div>

                            </div>

                        </div>

                    </div>

                    <div className="listing-popup-info">

                        <div className="listing-popup-header">

                            <span className="listing-popup-property-type">
                                Apartment
                            </span>

                            <h2>
                                Beautiful Apartment For Rent In Mar Elias
                            </h2>

                            <div className="listing-popup-location">
                                Mar Elias, Beirut
                            </div>

                            <div className="listing-popup-price">
                                USD 1,500
                            </div>

                        </div>

                        <div className="listing-popup-details">

                            <div className="listing-detail">
                                <span className="detail-label">
                                    Property Type
                                </span>
                                <span className="detail-value">
                                    Apartment
                                </span>
                            </div>

                            <div className="listing-detail">
                                <span className="detail-label">
                                    Bedrooms
                                </span>
                                <span className="detail-value">
                                    2
                                </span>
                            </div>

                            <div className="listing-detail">
                                <span className="detail-label">
                                    Bathrooms
                                </span>
                                <span className="detail-value">
                                    1
                                </span>
                            </div>

                            <div className="listing-detail">
                                <span className="detail-label">
                                    Size
                                </span>
                                <span className="detail-value">
                                    120 m²
                                </span>
                            </div>

                            <div className="listing-detail">
                                <span className="detail-label">
                                    Furnished
                                </span>
                                <span className="detail-value">
                                    Furnished
                                </span>
                            </div>

                            <div className="listing-detail">
                                <span className="detail-label">
                                    City
                                </span>
                                <span className="detail-value">
                                    Beirut
                                </span>
                            </div>

                        </div>

                    </div>

                    <div className="listing-popup-description">

                        <h3>Description</h3>

                        <p>
                            Beautiful and spacious apartment available for rent
                            in Mar Elias, Beirut. The property features two
                            bedrooms, one bathroom, a comfortable living area,
                            and modern furnishings. Located in a convenient
                            area close to shops, restaurants, and public
                            transportation.
                        </p>

                    </div>

                    <div className="listing-popup-footer">

                        <div className="listing-seller">

                            <span className="detail-label">
                                Seller
                            </span>

                            <span className="detail-value">
                                John Doe
                            </span>

                        </div>

                        <div className="listing-source">

                            <span className="detail-label">
                                Source
                            </span>

                            <span className="detail-value">
                                OLX Lebanon
                            </span>

                        </div>

                        <a
                            className="listing-source-button"
                            href="https://www.olx.com.lb/"
                            target="_blank"
                            rel="noopener noreferrer"
                        >
                            View Listing
                        </a>

                    </div>

                </div>

            </div>
        </div>
    );
}

export default ListingPopup;