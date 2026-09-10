import { useState } from "react";

import Header from "../components/Header";
import Footer from "../components/Footer";
import ListingCard from "../components/ListingCard";
import Pagination from "../components/Pagination";
import ListingsFilters from "../components/ListingsFilters";
import ListingPopup from "../components/ListingPopup";

import "../styles/listings.css";
import "../styles/pagination.css";
import "../styles/listingsfilters.css";
import "../styles/listingpopup.css";

function Listings() {

    const [isListingOpen, setIsListingOpen] = useState(false);

    return (
        <>
            <Header />

            <main className="listings-main">

                <ListingsFilters />

                <div className="listings-status">
                    <span className="status-line"></span>

                    <div className="status-text">
                        <span className="status-symbol">✦</span>
                        Browsing <span className="listing-count">7,364</span> listings from 3 different sources
                    </div>

                    <span className="status-line"></span>
                </div>

                <div className="listings-grid">
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                    <ListingCard onClick={() => setIsListingOpen(true)} />
                </div>

                <Pagination />

            </main>

            <Footer />

            <ListingPopup
                isOpen={isListingOpen}
                onClose={() => setIsListingOpen(false)}
            />
        </>
    );
}

export default Listings;