import Home from "./pages/Home";
import Listings from "./pages/Listings";
import Saved from "./pages/Saved";


function App() {

    const path = window.location.pathname;


    if (path === "/listings") {
        return <Listings />;
    }


    if (path === "/saved") {
        return <Saved />;
    }


    return <Home />;
}


export default App;