import { useState } from "react";

function FilterPopup({ isOpen, onClose, onApply }) {
    const [draftFilters, setDraftFilters] = useState({
        minPrice: "",
        maxPrice: "",
        minSize: "",
        maxSize: "",
        furnished: "",
    });

    const handleChange = (field, value) => {
        setDraftFilters((current) => ({
            ...current,
            [field]: value,
        }));
    };

    const handleApply = () => {
        onApply(draftFilters);
        onClose();
    };

    if (!isOpen) {
        return null;
    }

    return (
        <div id="filter-overlay" className="filter-overlay active">
            <div className="filter-popup">
                <div className="filter-cotent">

                    {/* Price Filter */}
                    <div className="filter-section">
                        <h3>Price</h3>

                        <div className="price-range">
                            <div className="price-input">
                                <label htmlFor="min-price">
                                    Min Price
                                </label>

                                <input
                                    id="min-price"
                                    type="number"
                                    placeholder="Minimum"
                                    value={draftFilters.minPrice}
                                    onChange={(event) =>
                                        handleChange(
                                            "minPrice",
                                            event.target.value
                                        )
                                    }
                                />
                            </div>

                            <div className="price-input">
                                <label htmlFor="max-price">
                                    Max Price
                                </label>

                                <input
                                    id="max-price"
                                    type="number"
                                    placeholder="Maximum"
                                    value={draftFilters.maxPrice}
                                    onChange={(event) =>
                                        handleChange(
                                            "maxPrice",
                                            event.target.value
                                        )
                                    }
                                />
                            </div>
                        </div>
                    </div>

                    {/* Size Filter */}
                    <div className="filter-section">
                        <h3>Size</h3>

                        <div className="size-inputs">
                            <div className="size-input">
                                <label htmlFor="min-size">
                                    Min Size (m²)
                                </label>

                                <input
                                    id="min-size"
                                    type="number"
                                    placeholder="Minimum"
                                    value={draftFilters.minSize}
                                    onChange={(event) =>
                                        handleChange(
                                            "minSize",
                                            event.target.value
                                        )
                                    }
                                />
                            </div>

                            <div className="size-input">
                                <label htmlFor="max-size">
                                    Max Size (m²)
                                </label>

                                <input
                                    id="max-size"
                                    type="number"
                                    placeholder="Maximum"
                                    value={draftFilters.maxSize}
                                    onChange={(event) =>
                                        handleChange(
                                            "maxSize",
                                            event.target.value
                                        )
                                    }
                                />
                            </div>
                        </div>
                    </div>

                    {/* Furnished Filter */}
                    <div className="filter-section">
                        <h3>Furnished</h3>

                        <div className="furnished-options">

                            <label>
                                <input
                                    type="radio"
                                    name="furnished"
                                    value=""
                                    checked={
                                        draftFilters.furnished === ""
                                    }
                                    onChange={(event) =>
                                        handleChange(
                                            "furnished",
                                            event.target.value
                                        )
                                    }
                                />
                                Any
                            </label>

                            <label>
                                <input
                                    type="radio"
                                    name="furnished"
                                    value="furnished"
                                    checked={
                                        draftFilters.furnished ===
                                        "furnished"
                                    }
                                    onChange={(event) =>
                                        handleChange(
                                            "furnished",
                                            event.target.value
                                        )
                                    }
                                />
                                Furnished
                            </label>

                            <label>
                                <input
                                    type="radio"
                                    name="furnished"
                                    value="appliances_only"
                                    checked={
                                        draftFilters.furnished ===
                                        "appliances_only"
                                    }
                                    onChange={(event) =>
                                        handleChange(
                                            "furnished",
                                            event.target.value
                                        )
                                    }
                                />
                                Appliances only
                            </label>

                            <label>
                                <input
                                    type="radio"
                                    name="furnished"
                                    value="unfurnished"
                                    checked={
                                        draftFilters.furnished ===
                                        "unfurnished"
                                    }
                                    onChange={(event) =>
                                        handleChange(
                                            "furnished",
                                            event.target.value
                                        )
                                    }
                                />
                                Unfurnished
                            </label>

                        </div>
                    </div>

                </div>

                {/* Popup Buttons */}
                <div className="filter-actions">
                    <button
                        id="cancel-filters"
                        type="button"
                        onClick={onClose}
                    >
                        Cancel
                    </button>

                    <button
                        id="apply-filters"
                        type="button"
                        onClick={handleApply}
                    >
                        Apply
                    </button>
                </div>
            </div>
        </div>
    );
}

export default FilterPopup;