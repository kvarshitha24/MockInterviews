import { useEffect } from "react";
import {
  Routes,
  Route,
  useNavigationType,
  useLocation,
} from "react-router-dom";
import Homepage from "./pages/Homepage";
import Thumbnail from "./pages/Thumbnail";
import ShoppingCart from "./pages/ShoppingCart";
import HomePage1 from "./pages/HomePage1";
import SIGNUP from "./pages/SIGNUP";
import LOGIN from "./pages/LOGIN";
import Profile from "./pages/Profile";
import RESUME from "./pages/RESUME";

function App() {
  const action = useNavigationType();
  const location = useLocation();
  const pathname = location.pathname;

  useEffect(() => {
    if (action !== "POP") {
      window.scrollTo(0, 0);
    }
  }, [action, pathname]);

  useEffect(() => {
    let title = "";
    let metaDescription = "";

    switch (pathname) {
      case "/":
        title = "";
        metaDescription = "";
        break;
      case "/thumbnail":
        title = "";
        metaDescription = "";
        break;
      case "/shopping-cart":
        title = "";
        metaDescription = "";
        break;
      case "/home-page":
        title = "";
        metaDescription = "";
        break;
      case "/sign-up":
        title = "";
        metaDescription = "";
        break;
      case "/login":
        title = "";
        metaDescription = "";
        break;
      case "/profile":
        title = "";
        metaDescription = "";
        break;
      case "/resume":
        title = "";
        metaDescription = "";
        break;
    }

    if (title) {
      document.title = title;
    }

    if (metaDescription) {
      const metaDescriptionTag = document.querySelector(
        'head > meta[name="description"]'
      );
      if (metaDescriptionTag) {
        metaDescriptionTag.content = metaDescription;
      }
    }
  }, [pathname]);

  return (
    <Routes>
      <Route path="/" element={<Homepage />} />
      <Route path="/thumbnail" element={<Thumbnail />} />
      <Route path="/shopping-cart" element={<ShoppingCart />} />
      <Route path="/home-page" element={<HomePage1 />} />
      <Route path="/sign-up" element={<SIGNUP />} />
      <Route path="/login" element={<LOGIN />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/resume" element={<RESUME />} />
    </Routes>
  );
}
export default App;
