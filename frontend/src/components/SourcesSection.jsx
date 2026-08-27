import olxLogo from "../assets/olx-logo.png";

function SourcesSection() {
    return (
        <section className="sources-section">
            <div className="sources-content">
                <h2>Rental Sources</h2>

                <div className="source-cards">
                    <div className="source-card">
                        <img src={olxLogo} alt="Source logo" />
                        <span>OLX Lebanon</span>
                    </div>

                    <div className="source-card">
                        <img src={olxLogo} alt="Source logo" />
                        <span>OLX Lebanon</span>
                    </div>

                    <div className="source-card">
                        <img src={olxLogo} alt="Source logo" />
                        <span>OLX Lebanon</span>
                    </div>

                    <div className="source-card">
                        <img src={olxLogo} alt="Source logo" />
                        <span>OLX Lebanon</span>
                    </div>

                    <div className="source-card">
                        <img src={olxLogo} alt="Source logo" />
                        <span>OLX Lebanon</span>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default SourcesSection;