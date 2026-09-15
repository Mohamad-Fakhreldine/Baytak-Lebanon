function Pagination({
    currentPage,
    totalPages,
    onPageChange
}) {

    const getPages = () => {

        if (totalPages <= 7) {
            return Array.from(
                { length: totalPages },
                (_, index) => index + 1
            );
        }

        if (currentPage <= 4) {
            return [
                1,
                2,
                3,
                4,
                5,
                "...",
                totalPages
            ];
        }

        if (currentPage >= totalPages - 3) {
            return [
                1,
                "...",
                totalPages - 4,
                totalPages - 3,
                totalPages - 2,
                totalPages - 1,
                totalPages
            ];
        }

        return [
            1,
            "...",
            currentPage - 1,
            currentPage,
            currentPage + 1,
            "...",
            totalPages
        ];
    };

    const pages = getPages();

    const handleClick = (event, page) => {
        event.preventDefault();
        event.stopPropagation();

        if (page === currentPage) {
            return;
        }

        onPageChange(page);
    };

    return (
        <nav
            className="pagination"
            aria-label="Listings pagination"
        >

            <button
                type="button"
                className="pagination-arrow"
                disabled={currentPage === 1}
                onClick={event =>
                    handleClick(
                        event,
                        currentPage - 1
                    )
                }
            >
                ←
            </button>

            {pages.map((page, index) => {

                if (page === "...") {
                    return (
                        <span
                            className="pagination-dots"
                            key={`dots-${index}`}
                        >
                            ...
                        </span>
                    );
                }

                return (
                    <button
                        type="button"
                        className={`pagination-page ${
                            page === currentPage
                                ? "active"
                                : ""
                        }`}
                        key={page}
                        onClick={event =>
                            handleClick(
                                event,
                                page
                            )
                        }
                    >
                        {page}
                    </button>
                );
            })}

            <button
                type="button"
                className="pagination-arrow"
                disabled={
                    currentPage === totalPages
                }
                onClick={event =>
                    handleClick(
                        event,
                        currentPage + 1
                    )
                }
            >
                →
            </button>

        </nav>
    );
}

export default Pagination;