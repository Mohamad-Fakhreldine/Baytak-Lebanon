import Home from "./pages/Home";
import Listings from "./pages/Listings";
import Saved from "./pages/Saved";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Privacy from "./pages/Privacy";


function App() {

    const path = window.location.pathname;


    if (path === "/listings") {
        return <Listings />;
    }


    if (path === "/saved") {
        return <Saved />;
    }


    if (path === "/about") {
        return <About />;
    }

    if (path === "/contact") {
        return <Contact />;
    }

    if (path === "/privacy") {
        return <Privacy />;
    }

    return <Home />;
}


export default App;