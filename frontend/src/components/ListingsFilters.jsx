import { useEffect, useRef, useState } from "react";

function ListingsFilters() {
    const [location, setLocation] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("location") || "";
    });
    const [selectedLocation, setSelectedLocation] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("location") || "";
    });
    const [propertyType, setPropertyType] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("property_type") || "";
    });
    const [minPrice, setMinPrice] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("min_price") || "";
    });
    const [maxPrice, setMaxPrice] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("max_price") || "";
    });
    const [minSize, setMinSize] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("min_size") || "";
    });
    const [maxSize, setMaxSize] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("max_size") || "";
    });
    const [furnished, setFurnished] = useState(() => {
        const params = new URLSearchParams(window.location.search);
        return params.get("furnished") || "";
    });
    const [suggestions, setSuggestions] = useState([]);
    const [propertyTypes, setPropertyTypes] = useState([]);
    const [propertyTypeOpen, setPropertyTypeOpen] = useState(false);
    const [furnishedOpen, setFurnishedOpen] = useState(false);
    const locationRequest = useRef(null);
    useEffect(() => {
        fetch(
            "http://127.0.0.1:5000/api/listings/property-types"
        )
            .then(response => {
                if (!response.ok) {
                    throw new Error(
                        `Failed to load property types: ${response.status}`
                    );
                }
                return response.json();
            })
            .then(data => {
                setPropertyTypes(
                    Array.isArray(data.property_types)
                        ? data.property_types
                        : []
                );
            })
            .catch(error => {
                console.error(
                    "Failed to load property types:",
                    error
                );
                setPropertyTypes([]);
            });
    }, []);
    const handleLocationChange = event => {
        const value = event.target.value;
        setLocation(value);
        setSelectedLocation("");
        if (locationRequest.current) {
            clearTimeout(locationRequest.current);
        }
        if (value.trim().length < 2) {
            setSuggestions([]);
            return;
        }
        locationRequest.current = setTimeout(() => {
            fetch(
                `http://127.0.0.1:5000/api/listings/locations?q=${encodeURIComponent(
                    value.trim()
                )}`
            )
                .then(response => {
                    if (!response.ok) {
                        throw new Error(
                            `Failed to load location suggestions: ${response.status}`
                        );
                    }
                    return response.json();
                })
                .then(data => {
                    setSuggestions(
                        Array.isArray(data.locations)
                            ? data.locations.slice(0, 3)
                            : []
                    );
                })
                .catch(error => {
                    console.error(
                        "Failed to load location suggestions:",
                        error
                    );
                    setSuggestions([]);
                });
        }, 250);
    };
    const handleApply = () => {
        const params = new URLSearchParams();
        const locationValue =
            selectedLocation.trim() !== ""
                ? selectedLocation.trim()
                : location.trim();
        if (locationValue !== "") {
            params.set(
                "location",
                locationValue
            );
        }
        if (propertyType !== "") {
            params.set(
                "property_type",
                propertyType
            );
        }
        if (minPrice !== "") {
            params.set(
                "min_price",
                minPrice
            );
        }
        if (maxPrice !== "") {
            params.set(
                "max_price",
                maxPrice
            );
        }
        if (minSize !== "") {
            params.set(
                "min_size",
                minSize
            );
        }
        if (maxSize !== "") {
            params.set(
                "max_size",
                maxSize
            );
        }
        if (furnished !== "") {
            params.set(
                "furnished",
                furnished
            );
        }
        params.set(
            "page",
            "1"
        );
        window.location.href =
            `/listings?${params.toString()}`;
    };
    const selectedPropertyType =
        propertyTypes.find(
            type => type === propertyType
        );
    const propertyTypeLabel =
        selectedPropertyType ||
        "Any Property Type";
    const furnishedLabel =
        furnished === "furnished"
            ? "Furnished"
            : furnished === "appliances_only"
                ? "Appliances only"
                : furnished === "unfurnished"
                    ? "Unfurnished"
                    : "Any Furnishing";
    return (
        <section className="listings-filters">
            <div className="filters-header-div">
                Not quite what you had in mind?
            </div>
            {/* Location */}
            <div className="filter-field">
                <input
                    id="listing-location"
                    type="text"
                    placeholder="Location"
                    value={location}
                    onChange={handleLocationChange}
                    autoComplete="off"
                />
                {suggestions.length > 0 && (
                    <div className="location-suggestions">
                        {suggestions.map(
                            suggestion => (
                                <button
                                    key={suggestion}
                                    type="button"
                                    className="location-suggestion"
                                    onClick={() => {
                                        setLocation(
                                            suggestion
                                        );
                                        setSelectedLocation(
                                            suggestion
                                        );
                                        setSuggestions([]);
                                    }}
                                >
                                    {suggestion}
                                </button>
                            )
                        )}
                    </div>
                )}
            </div>
            {/* Property Type */}
            <div className="filter-field">
                <div className="custom-select">
                    <button
                        type="button"
                        className="custom-select-button"
                        onClick={() =>
                            setPropertyTypeOpen(
                                !propertyTypeOpen
                            )
                        }
                    >
                        {propertyTypeLabel}
                        <span
                            className={`custom-select-arrow ${
                                propertyTypeOpen
                                    ? "open"
                                    : ""
                            }`}
                        >
                            ▾
                        </span>
                    </button>
                    {propertyTypeOpen && (
                        <div className="custom-select-options">
                            <button
                                type="button"
                                className={`custom-select-option ${
                                    propertyType === ""
                                        ? "selected"
                                        : ""
                                }`}
                                onClick={() => {
                                    setPropertyType("");
                                    setPropertyTypeOpen(
                                        false
                                    );
                                }}
                            >
                                Any Property Type
                            </button>
                            {propertyTypes.map(
                                type => (
                                    <button
                                        key={type}
                                        type="button"
                                        className={`custom-select-option ${
                                            propertyType === type
                                                ? "selected"
                                                : ""
                                        }`}
                                        onClick={() => {
                                            setPropertyType(
                                                type
                                            );
                                            setPropertyTypeOpen(
                                                false
                                            );
                                        }}
                                    >
                                        {type}
                                    </button>
                                )
                            )}
                        </div>
                    )}
                </div>
            </div>
            {/* Price */}
            <div className="filter-inputs">
                <input
                    id="listing-min-price"
                    type="number"
                    placeholder="Min Price"
                    value={minPrice}
                    onChange={event =>
                        setMinPrice(
                            event.target.value
                        )
                    }
                />
                <span>—</span>
                <input
                    id="listing-max-price"
                    type="number"
                    placeholder="Max Price"
                    value={maxPrice}
                    onChange={event =>
                        setMaxPrice(
                            event.target.value
                        )
                    }
                />
            </div>
            {/* Size */}
            <div className="filter-inputs">
                <input
                    id="listing-min-size"
                    type="number"
                    placeholder="Min Size"
                    value={minSize}
                    onChange={event =>
                        setMinSize(
                            event.target.value
                        )
                    }
                />
                <span>—</span>
                <input
                    id="listing-max-size"
                    type="number"
                    placeholder="Max Size"
                    value={maxSize}
                    onChange={event =>
                        setMaxSize(
                            event.target.value
                        )
                    }
                />
            </div>
            {/* Furnished */}
            <div className="filter-field">
                <div className="custom-select">
                    <button
                        type="button"
                        className="custom-select-button"
                        onClick={() =>
                            setFurnishedOpen(
                                !furnishedOpen
                            )
                        }
                    >
                        {furnishedLabel}
                        <span
                            className={`custom-select-arrow ${
                                furnishedOpen
                                    ? "open"
                                    : ""
                            }`}
                        >
                            ▾
                        </span>
                    </button>
                    {furnishedOpen && (
                        <div className="custom-select-options">

                            <button
                                type="button"
                                className={`custom-select-option ${
                                    furnished === ""
                                        ? "selected"
                                        : ""
                                }`}
                                onClick={() => {
                                    setFurnished("");
                                    setFurnishedOpen(
                                        false
                                    );
                                }}
                            >
                                Any Furnishing
                            </button>
                            <button
                                type="button"
                                className={`custom-select-option ${
                                    furnished === "furnished"
                                        ? "selected"
                                        : ""
                                }`}
                                onClick={() => {
                                    setFurnished(
                                        "furnished"
                                    );
                                    setFurnishedOpen(
                                        false
                                    );
                                }}
                            >
                                Furnished
                            </button>
                            <button
                                type="button"
                                className={`custom-select-option ${
                                    furnished === "appliances_only"
                                        ? "selected"
                                        : ""
                                }`}
                                onClick={() => {
                                    setFurnished(
                                        "appliances_only"
                                    );

                                    setFurnishedOpen(
                                        false
                                    );
                                }}
                            >
                                Appliances only
                            </button>
                            <button
                                type="button"
                                className={`custom-select-option ${
                                    furnished === "unfurnished"
                                        ? "selected"
                                        : ""
                                }`}
                                onClick={() => {
                                    setFurnished(
                                        "unfurnished"
                                    );
                                    setFurnishedOpen(
                                        false
                                    );
                                }}
                            >
                                Unfurnished
                            </button>
                        </div>
                    )}
                </div>
            </div>
            {/* Apply */}
            <div className="filter-actions">
                <button
                    type="button"
                    className="apply-filters"
                    onClick={handleApply}
                >
                    Apply
                </button>
            </div>
        </section>
    );
}

export default ListingsFilters;