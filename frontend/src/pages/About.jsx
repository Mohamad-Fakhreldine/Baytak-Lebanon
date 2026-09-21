import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/about.css";

function About() {
    return (
        <>
            <Header />
            <main className="about-page">
                <section className="about-hero">
                    <p className="about-eyebrow">
                        ABOUT BAYTAK
                    </p>
                    <h2>
                        Finding a place in Lebanon
                        <span> should be easier.</span>
                    </h2>
                    <p className="about-intro">
                        Baytak Lebanon brings property listings
                        from different sources together in one
                        simple place, making it easier to discover
                        homes, apartments, and properties across
                        Lebanon.
                    </p>
                </section>
                <section className="about-section">
                    <div className="about-section-heading">
                        <p className="about-eyebrow">
                            WHAT WE DO
                        </p>
                        <h3>
                            One place to explore
                            <br />
                            what is out there.
                        </h3>
                    </div>
                    <div className="about-section-content">
                        <p>
                            Searching for property online can mean
                            jumping between different websites,
                            comparing listings manually, and trying
                            to keep track of what you have already
                            seen.
                        </p>
                        <p>
                            Baytak was created to make that process
                            simpler. We collect publicly available
                            property listings from multiple sources
                            and bring them together so you can browse
                            them from one place.
                        </p>
                    </div>
                </section>
                <section className="about-features">
                    <article className="about-card">
                        <div className="about-card-number">
                            01
                        </div>
                        <h3>
                            Browse
                        </h3>
                        <p>
                            Explore property listings from across
                            Lebanon without having to search through
                            multiple platforms individually.
                        </p>
                    </article>
                    <article className="about-card">
                        <div className="about-card-number">
                            02
                        </div>
                        <h3>
                            Compare
                        </h3>
                        <p>
                            Filter listings by location, property
                            type, price, size, and other useful
                            details to narrow down your options.
                        </p>
                    </article>
                    <article className="about-card">
                        <div className="about-card-number">
                            03
                        </div>
                        <h3>
                            Discover
                        </h3>
                        <p>
                            Save interesting properties and return
                            to them whenever you want while
                            continuing your search.
                        </p>
                    </article>
                </section>
                <section className="about-mission">
                    <div className="about-mission-inner">
                        <p className="about-eyebrow">
                            OUR IDEA
                        </p>
                        <h3>
                            Your next place might already
                            be out there. We just want to
                            make it easier to find.
                        </h3>
                        <p>
                            Baytak Lebanon is an independent
                            property aggregation project built
                            around a simple idea: property
                            discovery should be straightforward,
                            organized, and accessible.
                        </p>
                    </div>
                </section>
            </main>
            <Footer />
        </>
    );
}
export default About;