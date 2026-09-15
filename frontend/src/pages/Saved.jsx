import { useState } from "react";

import Header from "../components/Header";
import Footer from "../components/Footer";
import ListingCard from "../components/ListingCard";
import ListingPopup from "../components/ListingPopup";

import heartImage from "../assets/heart.png";

import "../styles/listings.css";
import "../styles/listingpopup.css";

const SAVED_LISTINGS_KEY = "savedListings";

function Saved() {
    const [savedListings, setSavedListings] = useState(() => {
        const storedListings =
            localStorage.getItem(
                SAVED_LISTINGS_KEY
            );

        if (!storedListings) {
            return [];
        }

        try {
            const parsedListings =
                JSON.parse(storedListings);

            return Array.isArray(parsedListings)
                ? parsedListings
                : [];
        } catch (error) {
            console.error(
                "Failed to load saved listings:",
                error
            );

            return [];
        }
    });

    const [isListingOpen, setIsListingOpen] =
        useState(false);

    const [selectedListingId, setSelectedListingId] =
        useState(null);

    const handleListingClick = listingId => {
        setSelectedListingId(listingId);
        setIsListingOpen(true);
    };

    const handleCloseListing = () => {
        setIsListingOpen(false);
        setSelectedListingId(null);
    };

    const handleSavedChange = (
        listingId,
        isSaved
    ) => {
        if (isSaved) {
            return;
        }

        setSavedListings(
            currentListings => {
                const updatedListings =
                    currentListings.filter(
                        listing =>
                            listing.id !== listingId
                    );

                localStorage.setItem(
                    SAVED_LISTINGS_KEY,
                    JSON.stringify(
                        updatedListings
                    )
                );

                return updatedListings;
            }
        );
    };

    return (
        <>
            <div
                className={
                    `listings-page saved-page ${
                        savedListings.length === 0
                            ? "saved-page-empty"
                            : ""
                    } ${
                        isListingOpen
                            ? "blurred"
                            : ""
                    }`
                }
            >
                <Header />

                <main className="listings-main saved-main">
                    <div className="listings-status">
                        <span className="status-line"></span>

                        <div className="status-text">
                            <span className="status-symbol">
                                ✦
                            </span>

                            Saved{" "}

                            <span className="listing-count">
                                {savedListings.length}
                            </span>{" "}

                            {savedListings.length === 1
                                ? "listing"
                                : "listings"}
                        </div>

                        <span className="status-line"></span>
                    </div>

                    {savedListings.length === 0 ? (
                        <div className="saved-empty">
                            <img
                                src={heartImage}
                                alt=""
                                className="saved-empty-image"
                            />

                        </div>
                    ) : (
                        <div className="listings-grid">
                            {savedListings.map(
                                listing => (
                                    <ListingCard
                                        key={
                                            listing.id
                                        }
                                        listing={
                                            listing
                                        }
                                        onClick={() =>
                                            handleListingClick(
                                                listing.id
                                            )
                                        }
                                        onSavedChange={
                                            handleSavedChange
                                        }
                                    />
                                )
                            )}
                        </div>
                    )}
                </main>

                <Footer />
            </div>

            <ListingPopup
                isOpen={
                    isListingOpen
                }
                listingId={
                    selectedListingId
                }
                onClose={
                    handleCloseListing
                }
            />
        </>
    );
}

export default Saved;