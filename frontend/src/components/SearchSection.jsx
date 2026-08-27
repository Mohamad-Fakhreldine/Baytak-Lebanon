import { useEffect, useRef } from "react";
import Choices from "choices.js";

import filterImage from "../assets/filter.png";
import abstractImage from "../assets/abstract-option2.png";

function SearchSection({ onOpenFilters }) {
    const propertyTypeRef = useRef(null);

    useEffect(() => {
        const choices = new Choices(propertyTypeRef.current, {
            searchEnabled: false,
            itemSelectText: "",
            shouldSort: false,
        });

        return () => {
            choices.destroy();
        };
    }, []);

    return (
        <section
            id="search"
            className="search-section"
            style={{
                backgroundImage: `url(${abstractImage})`,
            }}
        >
            <div className="search-content">
                <h2>Discover What's Available</h2>

                <p>
                    Tell us what you are looking for and discover available rentals
                    that fit your needs across Lebanon.
                </p>

                <form className="search-form">
                    <label className="sr-only" htmlFor="location-search">
                        Search by city or area
                    </label>

                    <input
                        id="location-search"
                        type="text"
                        placeholder="Search by city or area"
                    />

                    <label className="sr-only" htmlFor="property-type">
                        Property type
                    </label>

                    <select
                        ref={propertyTypeRef}
                        id="property-type"
                        name="property-type"
                        defaultValue="apartment"
                    >
                        <option value="apartment">Apartment</option>
                        <option value="house">House</option>
                        <option value="studio">Studio</option>
                    </select>

                    <button
                        type="button"
                        id="open-filters"
                        className="filter-button"
                        aria-label="Open filters"
                        onClick={onOpenFilters}
                    >
                        <img src={filterImage} alt="" />
                    </button>

                    <button type="submit">
                        Search
                    </button>
                </form>
            </div>
        </section>
    );
}

export default SearchSection;