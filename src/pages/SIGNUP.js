import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import "./SIGNUP.css";

const SIGNUP = () => {
  const navigate = useNavigate();

  const onRectangleClick = useCallback(() => {
    navigate("/login");
  }, [navigate]);

  return (
    <div className="sign-up">
      <div className="sign-up-child" />
      <div className="navbar1">
        <div className="navbar-child1" />
        <div className="ai-interviews1">AI INTERVIEWS</div>
        <div className="login1">Login</div>
        <div className="products1">Products</div>
        <div className="solutions1">Solutions</div>
        <div className="navbar-child2" />
        <div className="navbar-child3" />
        <div className="demo1">Demo</div>
        <img className="navbar-child4" alt="" />
      </div>
      <div className="sign-up-item" />
      <img className="sign-up-inner" alt="" src="/rectangle-30@2x.png" />
      <div className="rectangle-parent">
        <div className="group-child" />
        <div className="sign-up-container">
          <div className="first-name">FIRST NAME</div>
          <div className="last-name">LAST NAME</div>
          <div className="email">EMAIL</div>
          <div className="confirm-password">CONFIRM PASSWORD</div>
          <div className="password">PASSWORD</div>
          <div className="sign-up-container-child" />
          <div className="sign-up-container-item" />
          <div className="sign-up-container-inner" />
          <div className="sign-up-container-child1" />
          <div className="password1">PASSWORD</div>
          <div className="password2">PASSWORD</div>
          <div className="email1">EMAIL</div>
          <div className="last-name1">LAST NAME</div>
          <div className="sign-up-container-child2" />
          <div className="sign-up1">SIGN UP</div>
          <div className="sign-up2">SIGN UP</div>
          <div className="sign-up-container-child3" />
          <div className="first-name1">
            <span className="first-name-txt-container">
              <span className="first">FIRST</span>
              <span className="span">{` `}</span>
              <span className="name">NAME</span>
            </span>
          </div>
        </div>
        <div className="group-item" />
        <img className="group-inner" alt="" src="/polygon-1.svg" />
        <img className="polygon-icon" alt="" src="/polygon-3.svg" />
        <img className="group-child1" alt="" src="/polygon-2.svg" />
        <img className="group-child2" alt="" src="/polygon-4.svg" />
        <img className="group-child3" alt="" src="/polygon-7.svg" />
        <img className="group-child4" alt="" src="/polygon-6.svg" />
        <img className="group-child5" alt="" src="/polygon-5.svg" />
        <div className="group-child6" onClick={onRectangleClick} />
        <div className="login2">Login</div>
        <img className="arrow-icon" alt="" src="/arrow-2.svg" />
      </div>
      <img className="rectangle-icon" alt="" src="/rectangle-51@2x.png" />
      <div className="or-">--- or ---</div>
    </div>
  );
};

export default SIGNUP;
