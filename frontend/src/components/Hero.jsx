import lebanonImage from "../assets/lebanon.png";

function Hero() {
    return (
        <section className="hero">
            <div className="hero-content">
                <h2>
                    Find Your Place in {" "}
                    <span className="hero-location">Lebanon</span>
                </h2>

                <ul className="hero-features">
                    <li>
                        <span className="checkmark">✓</span>
                        Search multiple rental sources
                    </li>

                    <li>
                        <span className="checkmark">✓</span>
                        Compare listings in one place
                    </li>

                    <li>
                        <span className="checkmark">✓</span>
                        Completely free — no hidden fees
                    </li>

                    <li>
                        <span className="checkmark">✓</span>
                        No account required
                    </li>
                </ul>

                <a href="#search" className="hero-button">
                    Start Searching
                </a>
            </div>

            <div className="hero-image">
                <div className="hero-image-wrapper">
                    <img
                        src={lebanonImage}
                        alt="Lebanese homes"
                    />
                </div>
            </div>
        </section>
    );
}

export default Hero;