import { useEffect, useRef, useState } from "react";
import Choices from "choices.js";
import filterImage from "../assets/filter.png";
import abstractImage from "../assets/abstract-option2.png";

function SearchSection({ onOpenFilters, filters }) {
    const propertyTypeRef = useRef(null);
    const locationWrapperRef = useRef(null);
    const [location, setLocation] = useState("");
    const [suggestions, setSuggestions] = useState([]);
    const [propertyTypes, setPropertyTypes] = useState([]);
    const [showSuggestions, setShowSuggestions] = useState(false);
    useEffect(() => {
        fetch(
            "/api/listings/property-types"
        )
            .then(response => {
                if (!response.ok) {
                    throw new Error(
                        "Failed to fetch property types"
                    );
                }
                return response.json();
            })
            .then(data => {
                setPropertyTypes(
                    data.property_types || []
                );
            })
            .catch(error => {
                console.error(
                    "Failed to fetch property types:",
                    error
                );
            });
    }, []);
    useEffect(() => {
        if (
            !propertyTypeRef.current ||
            propertyTypes.length === 0
        ) {
            return;
        }
        const choices = new Choices(
            propertyTypeRef.current,
            {
                searchEnabled: false,
                itemSelectText: "",
                shouldSort: false,
            }
        );
        return () => {
            choices.destroy();
        };
    }, [propertyTypes]);
    useEffect(() => {
        if (location.trim() === "") {
            return;
        }
        const controller =
            new AbortController();
        const timeout = setTimeout(() => {
            fetch(
                `/api/listings/locations?q=${encodeURIComponent(
                    location
                )}`,
                {
                    signal: controller.signal
                }
            )
                .then(response => {
                    if (!response.ok) {
                        throw new Error(
                            "Failed to fetch location suggestions"
                        );
                    }
                    return response.json();
                })
                .then(data => {
                    const locations =
                        data.locations || [];

                    setSuggestions(
                        locations.slice(0, 3)
                    );
                    setShowSuggestions(
                        locations.length > 0
                    );
                })
                .catch(error => {
                    if (
                        error.name !== "AbortError"
                    ) {
                        console.error(
                            "Failed to fetch location suggestions:",
                            error
                        );
                    }
                });
        }, 200);
        return () => {
            clearTimeout(timeout);
            controller.abort();

        };
    }, [location]);
    useEffect(() => {
        const handleClickOutside = event => {
            if (
                locationWrapperRef.current &&
                !locationWrapperRef.current.contains(
                    event.target
                )
            ) {
                setShowSuggestions(false);
            }
        };
        document.addEventListener(
            "mousedown",
            handleClickOutside
        );
        return () => {
            document.removeEventListener(
                "mousedown",
                handleClickOutside
            );
        };
    }, []);
    const handleSuggestionClick = suggestion => {
        setLocation(suggestion);
        setShowSuggestions(false);
    };
    const handleSubmit = event => {
        event.preventDefault();
        const propertyType =
            propertyTypeRef.current?.value || "";
        const params =
            new URLSearchParams();
        if (location.trim() !== "") {
            params.set(
                "location",
                location.trim()
            );
        }
        if (propertyType !== "") {
            params.set(
                "property_type",
                propertyType
            );
        }
        if (filters?.minPrice !== "") {
            params.set(
                "min_price",
                filters.minPrice
            );

        }
        if (filters?.maxPrice !== "") {
            params.set(
                "max_price",
                filters.maxPrice
            );

        }
        if (filters?.minSize !== "") {
            params.set(
                "min_size",
                filters.minSize
            );

        }
        if (filters?.maxSize !== "") {
            params.set(
                "max_size",
                filters.maxSize
            );

        }
        if (
            filters?.furnished !== ""
        ) {

            params.set(
                "furnished",
                filters.furnished
            );

        }
        params.set(
            "page",
            "1"
        );
        window.location.href =
            `/listings?${params.toString()}`;

    };
    return (
        <section
            id="search"
            className="search-section"
            style={{
                backgroundImage: `url(${abstractImage})`,
            }}
        >
            <div className="search-content">
                <h2>
                    Discover What's Available
                </h2>
                <p>
                    Tell us what you are looking for and discover available rentals
                    that fit your needs across Lebanon.
                </p>
                <form
                    className="search-form"
                    onSubmit={handleSubmit}
                >
                    <div
                        className="location-search-wrapper"
                        ref={locationWrapperRef}
                    >
                        <label
                            className="sr-only"
                            htmlFor="location-search"
                        >
                            Search by city or area
                        </label>
                        <input
                            id="location-search"
                            type="text"
                            placeholder="Search by city or area"
                            value={location}
                            onChange={event => {
                                const value =
                                    event.target.value;

                                setLocation(value);

                                if (
                                    value.trim() === ""
                                ) {
                                    setShowSuggestions(
                                        false
                                    );
                                }

                            }}
                            onFocus={() => {

                                if (
                                    suggestions.length > 0
                                ) {
                                    setShowSuggestions(
                                        true
                                    );
                                }

                            }}
                            autoComplete="off"
                        />
                        {showSuggestions && (
                            <div className="location-suggestions">
                                {suggestions
                                    .slice(0, 3)
                                    .map(
                                        suggestion => (
                                            <button
                                                key={suggestion}
                                                type="button"
                                                className="location-suggestion"
                                                onClick={() =>
                                                    handleSuggestionClick(
                                                        suggestion
                                                    )
                                                }
                                            >
                                                {suggestion}
                                            </button>
                                        )
                                    )}
                            </div>
                        )}
                    </div>
                    <label
                        className="sr-only"
                        htmlFor="property-type"
                    >
                        Property type
                    </label>
                    <select
                        ref={propertyTypeRef}
                        id="property-type"
                        name="property-type"
                        defaultValue=""
                    >
                        <option value="">
                            Property type
                        </option>
                        {propertyTypes.map(
                            propertyType => (

                                <option
                                    key={propertyType}
                                    value={propertyType}
                                >
                                    {propertyType}
                                </option>

                            )
                        )}
                    </select>
                    <button
                        type="button"
                        id="open-filters"
                        className="filter-button"
                        aria-label="Open filters"
                        onClick={onOpenFilters}
                    >
                        <img
                            src={filterImage}
                            alt=""
                        />
                    </button>
                    <button
                        type="submit"
                    >
                        Search
                    </button>
                </form>
            </div>
        </section>
    );
}

export default SearchSection;