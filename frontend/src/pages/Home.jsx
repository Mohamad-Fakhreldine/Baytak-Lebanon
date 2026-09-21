import { useState } from "react";

import Header from "../components/Header";
import Hero from "../components/Hero";
import Intro from "../components/Intro";
import SearchSection from "../components/SearchSection";
import FilterPopup from "../components/FilterPopup";
import SourcesSection from "../components/SourcesSection";
import Footer from "../components/Footer";

function Home() {
    const [isFilterOpen, setIsFilterOpen] = useState(false);
    const [filters, setFilters] = useState({
        minPrice: "",
        maxPrice: "",
        minSize: "",
        maxSize: "",
        furnished: "",
    });
    const handleApplyFilters = (newFilters) => {
        setFilters(newFilters);
    };
    return (
        <>
            <Header />
            <main>
                <Hero />
                <Intro />
                <SearchSection
                    onOpenFilters={() => setIsFilterOpen(true)}
                    filters={filters}
                />
                <SourcesSection />
            </main>
            <Footer />
            <FilterPopup
                isOpen={isFilterOpen}
                onClose={() => setIsFilterOpen(false)}
                onApply={handleApplyFilters}
            />
        </>
    );
}
export default Home;