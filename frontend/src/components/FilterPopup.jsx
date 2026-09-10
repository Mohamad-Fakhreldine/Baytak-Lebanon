function FilterPopup({ isOpen, onClose }) {
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
                                    value="furnished"
                                    defaultChecked
                                />
                                Furnished
                            </label>

                            <label>
                                <input
                                    type="radio"
                                    name="furnished"
                                    value="unfurnished"
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
                        onClick={onClose}
                    >
                        Apply
                    </button>
                </div>
            </div>
        </div>
    );
}

export default FilterPopup;