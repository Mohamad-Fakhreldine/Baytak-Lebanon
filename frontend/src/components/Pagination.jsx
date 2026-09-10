function Pagination() {
    return (
        <nav className="pagination" aria-label="Listings pagination">
            <button className="pagination-arrow" disabled>
                ←
            </button>

            <button className="pagination-page active">1</button>
            <button className="pagination-page">2</button>
            <button className="pagination-page">3</button>
            <button className="pagination-page">4</button>
            <button className="pagination-page">5</button>

            <span className="pagination-dots">...</span>

            <button className="pagination-page">148</button>

            <button className="pagination-arrow">
                →
            </button>
        </nav>
    );
}

export default Pagination;