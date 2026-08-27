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

    return (
        <>
            <Header />

            <main>
                <Hero />
                <Intro />

                <SearchSection
                    onOpenFilters={() => setIsFilterOpen(true)}
                />

                <SourcesSection />
            </main>

            <Footer />

            <FilterPopup
                isOpen={isFilterOpen}
                onClose={() => setIsFilterOpen(false)}
            />
        </>
    );
}

export default Home;