import { useEffect, useState } from "react";


function Header() {

    const [menuOpen, setMenuOpen] =
        useState(false);


    useEffect(() => {

        function handleOutsideClick() {

            setMenuOpen(false);

        }


        document.addEventListener(
            "click",
            handleOutsideClick
        );


        return () => {

            document.removeEventListener(
                "click",
                handleOutsideClick
            );

        };

    }, []);


    return (
        <header>

            <h1>

                <span className="brand-main">
                    Baytak
                </span>{" "}

                <span className="brand-location">
                    Lebanon
                </span>

            </h1>


            <nav className="header-nav">

                <button
                    className="nav-button"
                    onClick={() =>
                        window.location.href =
                            "/home"
                    }
                >
                    Home
                </button>


                <button
                    className="nav-button"
                    onClick={() =>
                        window.location.href =
                            "/listings"
                    }
                >
                    Listings
                </button>


                <button
                    className="nav-button"
                    onClick={() =>
                        window.location.href =
                            "/saved"
                    }
                >
                    Saved
                </button>

            </nav>


            <div
                className="menu-container"
                onClick={(event) =>
                    event.stopPropagation()
                }
            >

                <button
                    className="menu-toggle"
                    aria-label="Open navigation menu"
                    onClick={() =>
                        setMenuOpen(!menuOpen)
                    }
                >
                    ☰
                </button>


                <div
                    className={
                        `menu-popup ${
                            menuOpen
                                ? "active"
                                : ""
                        }`
                    }
                >

                    <button
                        onClick={() =>
                            window.location.href =
                                "/about"
                        }
                    >
                        About Baytak Lebanon
                    </button>

                    <hr />


                    <button
                        onClick={() =>
                            window.location.href =
                                "/contact"
                        }
                    >
                        Contact Us
                    </button>

                    <hr />


                    <button
                        onClick={() =>
                            window.location.href =
                                "/privacy"
                        }
                    >
                        Privacy Policy & Terms Of Service
                    </button>

                </div>

            </div>

        </header>
    );
}


export default Header;