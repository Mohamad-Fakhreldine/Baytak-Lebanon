import { useEffect, useState } from "react";
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
    const [listings, setListings] = useState([]);
    const [currentPage, setCurrentPage] = useState(() => {
        const params = new URLSearchParams(
            window.location.search
        );
        const page = parseInt(
            params.get("page") || "1",
            10
        );
        return page > 0 ? page : 1;
    });

    const [totalPages, setTotalPages] = useState(1);
    const [totalListings, setTotalListings] = useState(0);
    const [totalSources, setTotalSources] = useState(0);
    const [isListingOpen, setIsListingOpen] = useState(false);
    const [selectedListingId, setSelectedListingId] = useState(null);

    useEffect(() => {
        const params = new URLSearchParams(
            window.location.search
        );
        params.set(
            "page",
            currentPage
        );
        fetch(
            `http://127.0.0.1:5000/api/listings/?${params.toString()}`
        )
            .then(response => {
                if (!response.ok) {
                    throw new Error(
                        "Failed to fetch listings"
                    );
                }
                return response.json();
            })
            .then(data => {
                setListings(
                    data.listings || []
                );
                setTotalPages(
                    data.pagination.pages
                );
                setTotalListings(
                    data.pagination.total
                );
                setTotalSources(
                    data.pagination.sources
                );
            })
            .catch(error => {
                console.error(
                    "Failed to fetch listings:",
                    error
                );
            });
    }, [currentPage]);
    const handleListingClick = listingId => {
        setSelectedListingId(
            listingId
        );
        setIsListingOpen(
            true
        );
    };
    const handleCloseListing = () => {
        setIsListingOpen(
            false
        );
        setSelectedListingId(
            null
        );
    };
    const handlePageChange = page => {
        const params =
            new URLSearchParams(
                window.location.search
            );
        params.set(
            "page",
            page
        );
        window.history.replaceState(
            {},
            "",
            `/listings?${params.toString()}`
        );
        setCurrentPage(
            page
        );
        window.scrollTo({
            top: 0,
            behavior: "smooth"
        });
    };
    return (
        <>
            <div
                className={
                    isListingOpen
                        ? "listings-page blurred"
                        : "listings-page"
                }
            >
                <Header />
                <main className="listings-main">
                    <ListingsFilters />
                    <div className="listings-status">
                        <span className="status-line"></span>
                        <div className="status-text">
                            <span className="status-symbol">
                                ✦
                            </span>
                            Browsing{" "}
                            <span className="listing-count">
                                {totalListings.toLocaleString()}
                            </span>{" "}
                            listings from{" "}
                            <span className="listing-count">
                                {totalSources}
                            </span>{" "}
                            different sources
                        </div>
                        <span className="status-line"></span>
                    </div>
                    <div className="listings-grid">
                        {listings.map(
                            listing => (
                                <ListingCard
                                    key={listing.id}
                                    listing={listing}
                                    onClick={() =>
                                        handleListingClick(
                                            listing.id
                                        )
                                    }
                                />
                            )
                        )}
                    </div>
                    <Pagination
                        currentPage={
                            currentPage
                        }
                        totalPages={
                            totalPages
                        }
                        onPageChange={
                            handlePageChange
                        }
                    />
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
export default Listings;