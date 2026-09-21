const SAVED_LISTINGS_KEY = "savedListings";

function ListingCard({ listing, onClick, onSavedChange }) {
    const isSaved = () => {
        const savedListings = JSON.parse(
            localStorage.getItem(SAVED_LISTINGS_KEY) || "[]"
        );
        return savedListings.some(
            savedListing => savedListing.id === listing.id
        );
    };
    const handleFavoriteClick = (event) => {
        event.stopPropagation();
        const savedListings = JSON.parse(
            localStorage.getItem(SAVED_LISTINGS_KEY) || "[]"
        );
        const alreadySaved = savedListings.some(
            savedListing => savedListing.id === listing.id
        );
        if (alreadySaved) {
            const updatedListings = savedListings.filter(
                savedListing => savedListing.id !== listing.id
            );
            localStorage.setItem(
                SAVED_LISTINGS_KEY,
                JSON.stringify(updatedListings)
            );
        } else {
            const updatedListings = [
                ...savedListings,
                listing
            ];
            localStorage.setItem(
                SAVED_LISTINGS_KEY,
                JSON.stringify(updatedListings)
            );
        }
        if (onSavedChange) {
            onSavedChange(
                listing.id,
                !alreadySaved
            );
        }
        event.currentTarget
            .closest(".listing-card")
            .querySelector(".checkbox")
            .checked = !alreadySaved;
    };
    return (
        <article
            className="listing-card"
            onClick={onClick}
        >
            <div className="listing-image">
                <img
                    src={listing.images[0].image_url}
                    alt={listing.title}
                />
            </div>
            <div className="listing-info">
                <div className="listing-location">
                    {listing.title}
                </div>
                <div className="listing-price">
                    {listing.currency} {listing.price.toLocaleString()}
                </div>
                <div className="listing-tags">
                    <span className="listing-tag">
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="2"
                            strokeLinecap="round"
                            strokeLinejoin="round"
                        >
                            <path d="M2 4v16" />
                            <path d="M2 8h18a2 2 0 0 1 2 2v10" />
                            <path d="M2 17h20" />
                            <path d="M6 8v9" />
                        </svg>
                        <span className="bedroom-count">
                            {listing.bedrooms}
                        </span>
                    </span>
                    {listing.furnished === "Fully Furnished" && (
                        <span className="listing-tag">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M20 9V6a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v3" />
                                <path d="M2 16a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z" />
                                <path d="M4 18v2" />
                                <path d="M20 18v2" />
                                <path d="M12 4v9" />
                            </svg>
                        </span>
                    )}
                    {listing.furnished === "Appliances only" && (
                        <span className="listing-tag">
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="24"
                                height="24"
                                viewBox="0 0 24 24"
                                fill="none"
                                stroke="currentColor"
                                strokeWidth="2"
                                strokeLinecap="round"
                                strokeLinejoin="round"
                            >
                                <path d="M8 14a2 2 0 0 0-1.963 1.615l-1.018 5.193A1 1 0 0 0 6 22h12a1 1 0 0 0 .981-1.192l-1.018-5.193A2 2 0 0 0 16 14Z" />
                                <path d="m17 2-1 12" />
                                <path d="M8.006 14 7 2" />
                                <path d="M7.565 8.787A5 5 0 0 0 12 8a5 5 0 0 1 4.56-.75" />
                                <path d="M19 2H5a2 2 0 0 1 2-2v5a2 2 0 0 0 .688 1.5" />
                                <path d="M12 18h.01" />
                            </svg>
                        </span>
                    )}
                </div>
            </div>
            <div className="listing-button">
                <div
                    className="heart-container"
                    title="Like"
                    onClick={handleFavoriteClick}
                >
                    <input
                        type="checkbox"
                        className="checkbox"
                        defaultChecked={isSaved()}
                    />
                    <div className="svg-container">
                        <svg
                            viewBox="0 0 24 24"
                            className="svg-outline"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Zm-3.585,18.4a2.973,2.973,0,0,1-3.83,0C4.947,16.006,2,11.87,2,8.967a4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,11,8.967a1,1,0,0,0,2,0,4.8,4.8,0,0,1,4.5-5.05A4.8,4.8,0,0,1,22,8.967C22,11.87,19.053,16.006,13.915,20.313Z" />
                        </svg>
                        <svg
                            viewBox="0 0 24 24"
                            className="svg-filled"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path d="M17.5,1.917a6.4,6.4,0,0,0-5.5,3.3,6.4,6.4,0,0,0-5.5-3.3A6.8,6.8,0,0,0,0,8.967c0,4.547,4.786,9.513,8.8,12.88a4.974,4.974,0,0,0,6.4,0C19.214,18.48,24,13.514,24,8.967A6.8,6.8,0,0,0,17.5,1.917Z" />
                        </svg>
                        <svg
                            className="svg-celebrate"
                            width="100"
                            height="100"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <polygon points="10,10 20,20" />
                            <polygon points="10,50 20,50" />
                            <polygon points="20,80 30,70" />
                            <polygon points="90,10 80,20" />
                            <polygon points="90,50 80,50" />
                            <polygon points="80,80 70,70" />
                        </svg>
                    </div>
                </div>
            </div>
        </article>
    );
}

export default ListingCard;