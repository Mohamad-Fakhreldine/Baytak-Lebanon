import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/privacy.css";


function Privacy() {

    return (
        <>

            <Header />


            <main className="privacy-page">

                <section className="privacy-hero">

                    <p className="privacy-eyebrow">
                        LEGAL
                    </p>

                    <h2>
                        Privacy Policy
                        <span> & Terms of Service</span>
                    </h2>

                    <p className="privacy-intro">
                        A straightforward overview of how Baytak
                        Lebanon works, what information the website
                        uses, and the terms that apply when using
                        the platform.
                    </p>

                </section>


                <section className="privacy-content">

                    <article className="privacy-section">

                        <p className="privacy-number">
                            01
                        </p>

                        <h3>
                            About Baytak Lebanon
                        </h3>

                        <p>
                            Baytak Lebanon is an independent property
                            aggregation project that brings publicly
                            available property listings from different
                            sources together in one place.
                        </p>

                        <p>
                            Baytak does not act as a real estate agency,
                            property owner, landlord, or intermediary
                            between users and property owners. Listings
                            displayed on the platform originate from
                            external sources.
                        </p>

                    </article>


                    <article className="privacy-section">

                        <p className="privacy-number">
                            02
                        </p>

                        <h3>
                            Information We Collect
                        </h3>

                        <p>
                            Baytak is designed to operate without
                            requiring users to create an account or
                            provide personal information simply to
                            browse listings.
                        </p>

                        <p>
                            Saved listings are stored locally in the
                            user's browser. Baytak does not require
                            users to submit their saved properties to
                            the platform.
                        </p>

                    </article>


                    <article className="privacy-section">

                        <p className="privacy-number">
                            03
                        </p>

                        <h3>
                            Property Listings
                        </h3>

                        <p>
                            Property information displayed on Baytak
                            is collected from publicly available
                            sources and presented for informational
                            and discovery purposes.
                        </p>

                        <p>
                            Listing information may become outdated,
                            unavailable, inaccurate, or change on its
                            original source. Users should always verify
                            property details directly with the original
                            listing source before making any decisions.
                        </p>

                    </article>


                    <article className="privacy-section">

                        <p className="privacy-number">
                            04
                        </p>

                        <h3>
                            External Websites
                        </h3>

                        <p>
                            Baytak may link users to external websites
                            where the original property listings are
                            hosted.
                        </p>

                        <p>
                            Baytak does not control those websites and
                            is not responsible for their content,
                            availability, privacy practices, or terms.
                            When visiting an external website, users are
                            subject to that website's own policies.
                        </p>

                    </article>


                    <article className="privacy-section">

                        <p className="privacy-number">
                            05
                        </p>

                        <h3>
                            Acceptable Use
                        </h3>

                        <p>
                            Users may use Baytak for personal property
                            discovery and research. Users should not
                            attempt to interfere with the operation of
                            the website, abuse its services, or use the
                            platform for unlawful purposes.
                        </p>

                    </article>


                    <article className="privacy-section">

                        <p className="privacy-number">
                            06
                        </p>

                        <h3>
                            Changes to This Policy
                        </h3>

                        <p>
                            These terms and policies may be updated as
                            Baytak evolves. Any changes will be reflected
                            on this page.
                        </p>

                    </article>

                </section>


                <section className="privacy-disclaimer">

                    <div className="privacy-disclaimer-inner">

                        <p className="privacy-eyebrow">
                            IMPORTANT
                        </p>

                        <h3>
                            Baytak is a property discovery
                            platform, not a real estate agency.
                        </h3>

                        <p>
                            Always verify property information,
                            availability, pricing, and other details
                            with the original listing source before
                            taking action.
                        </p>

                    </div>

                </section>

            </main>


            <Footer />

        </>
    );

}


export default Privacy;