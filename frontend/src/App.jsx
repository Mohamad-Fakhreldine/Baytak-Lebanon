import Home from "./pages/Home";
import Listings from "./pages/Listings";

function App() {
    const path = window.location.pathname;

    if (path === "/listings") {
        return <Listings />;
    }

    return <Home />;
}

export default App;