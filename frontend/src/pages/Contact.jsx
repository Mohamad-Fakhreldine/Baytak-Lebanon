import Header from "../components/Header";
import Footer from "../components/Footer";
import "../styles/contact.css";


function Contact() {

    return (
        <>

            <Header />


            <main className="contact-page">

                <section className="contact-hero">

                    <p className="contact-eyebrow">
                        CONTACT BAYTAK
                    </p>

                    <h2>
                        Have a question?
                        <span> Let’s talk.</span>
                    </h2>

                    <p className="contact-intro">
                        Whether you have a question about Baytak,
                        found something that needs attention, or
                        simply want to get in touch, we would love
                        to hear from you.
                    </p>

                </section>


                <section className="contact-content">

                    <div className="contact-info">

                        <p className="contact-eyebrow">
                            GET IN TOUCH
                        </p>

                        <h3>
                            We’re here to help.
                        </h3>

                        <p>
                            Baytak Lebanon is an independent property
                            aggregation project. If you have questions,
                            feedback, suggestions, or notice an issue
                            with the website, feel free to reach out.
                        </p>

                        <div className="contact-detail">

                            <span>
                                EMAIL
                            </span>

                            <a href="mailto:contact@baytaklebanon.com">
                                contact@baytaklebanon.com
                            </a>

                        </div>

                    </div>


                    <div className="contact-card">

                        <div className="contact-card-number">
                            01
                        </div>

                        <h3>
                            Questions & Feedback
                        </h3>

                        <p>
                            Have an idea that could make Baytak
                            better? Found something that does not
                            look right? We appreciate hearing from
                            people using the platform.
                        </p>


                        <div className="contact-card-divider" />


                        <div className="contact-card-number">
                            02
                        </div>

                        <h3>
                            Listing Issues
                        </h3>

                        <p>
                            If you notice an inaccurate, outdated,
                            or otherwise problematic listing, let
                            us know so we can look into it.
                        </p>

                    </div>

                </section>


                <section className="contact-bottom">

                    <p className="contact-eyebrow">
                        BAYTAK LEBANON
                    </p>

                    <h3>
                        Building a simpler way to
                        discover property in Lebanon.
                    </h3>

                </section>

            </main>


            <Footer />

        </>
    );

}


export default Contact;