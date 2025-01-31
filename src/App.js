import React, { useEffect } from "react";
import { Routes, Route, useNavigationType, useLocation } from "react-router-dom";
import HOMEPAGE1 from "./pages/HomePage1";
import SIGNUP from "./pages/SIGNUP";
import LOGIN from "./pages/LOGIN";
import Profile from "./pages/Profile";
import Navbar from "./pages/Navbar";
import Footer from "./pages/Footer";
import StepController from "./pages/StepController";
import INTERVIEW from "./pages/INTERVIEW";
import EditProfile from "./pages/EditProfile";
import './App.css';
import UserReports from "./pages/UserReports";
import RecruiterTable from "./pages/RecruitersTable";

function App() {
  const action = useNavigationType();
  const location = useLocation();
  const pathname = location.pathname;

  useEffect(() => {
    const handleBeforeUnload = (event) => {
      event.preventDefault();
      event.returnValue = ''; // Required for showing the confirmation dialog
    };

    window.addEventListener('beforeunload', handleBeforeUnload);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
    };
  }, []);

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
        title = "Home";
        metaDescription = "Welcome to the home page.";
        break;
      case "/sign-up":
        title = "Sign Up";
        metaDescription = "Create an account.";
        break;
      case "/login":
        title = "Login";
        metaDescription = "Log in to your account.";
        break;
      case "/profile":
        title = "Profile";
        metaDescription = "View your profile.";
        break;
      case "/steps":
        title = "Steps";
        metaDescription = "Follow the steps for the interview process.";
        break;
      case "/interview":
        title = "Interview";
        metaDescription = "Prepare for your interview.";
        break;
      case "/editprofile":
        title = "Edit Profile";
        metaDescription = "Edit your profile.";
        break;
      default:
        title = "App";
        metaDescription = "App description.";
    }

    if (title) {
      document.title = title;
    }

    if (metaDescription) {
      const metaDescriptionTag = document.querySelector('head > meta[name="description"]');
      if (metaDescriptionTag) {
        metaDescriptionTag.content = metaDescription;
      }
    }
  }, [pathname]);

  return (
    <div className="app-container">
    <div className="abc">
      <Navbar />
      </div>
      <div className="content-wrap">
        <Routes>
          <Route path="/" element={<HOMEPAGE1 />} />
          <Route path="/login" element={<LOGIN />} />
          <Route path="/sign-up" element={<SIGNUP />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/steps" element={<StepController />} />
          <Route path="/interview" element={<INTERVIEW />} />
          <Route path="/editprofile" element={<EditProfile />} />
          <Route path="/userreports" element={<UserReports/>} />
          <Route path="/recruiterslist" element={<RecruiterTable/>} />
        </Routes>
        {/* <UserReports/> */}
        {/* <RecruiterTable/> */}
      </div>
      <Footer />
    </div>
  );
}

export default App;