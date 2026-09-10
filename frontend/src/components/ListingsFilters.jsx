import { useState } from "react";

function ListingsFilters() {

    const [propertyTypeOpen, setPropertyTypeOpen] = useState(false);
    const [propertyType, setPropertyType] = useState("");

    const propertyTypes = [
        { value: "", label: "Any Property Type" },
        { value: "apartment", label: "Apartment" },
        { value: "house", label: "House" },
        { value: "studio", label: "Studio" },
    ];

    const selectedPropertyType =
        propertyTypes.find(type => type.value === propertyType);

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
                />
            </div>

            {/* Property Type */}
            <div className="filter-field">
                <div className="custom-select">

                    <button
                        type="button"
                        className="custom-select-button"
                        onClick={() => setPropertyTypeOpen(!propertyTypeOpen)}
                    >
                        {selectedPropertyType.label}

                        <span className={`custom-select-arrow ${propertyTypeOpen ? "open" : ""}`}>
                            ▾
                        </span>
                    </button>

                    {propertyTypeOpen && (
                        <div className="custom-select-options">

                            {propertyTypes.map(type => (
                                <button
                                    key={type.value}
                                    type="button"
                                    className={`custom-select-option ${
                                        propertyType === type.value ? "selected" : ""
                                    }`}
                                    onClick={() => {
                                        setPropertyType(type.value);
                                        setPropertyTypeOpen(false);
                                    }}
                                >
                                    {type.label}
                                </button>
                            ))}

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
                />

                <span>—</span>

                <input
                    id="listing-max-price"
                    type="number"
                    placeholder="Max Price"
                />
            </div>

            {/* Size */}
            <div className="filter-inputs">
                <input
                    id="listing-min-size"
                    type="number"
                    placeholder="Min Size"
                />

                <span>—</span>

                <input
                    id="listing-max-size"
                    type="number"
                    placeholder="Max Size"
                />
            </div>

            {/* Furnished */}
            <div className="furnished-options">
                <label>
                    <input
                        type="radio"
                        name="listing-furnished"
                        value="furnished"
                        defaultChecked
                    />
                    Furnished
                </label>

                <label>
                    <input
                        type="radio"
                        name="listing-furnished"
                        value="unfurnished"
                    />
                    Unfurnished
                </label>
            </div>

            {/* Apply */}
            <div className="filter-actions">
                <button
                    type="button"
                    className="apply-filters"
                >
                    Apply
                </button>
            </div>

        </section>
    );
}

export default ListingsFilters;