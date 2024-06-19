import { useCallback } from "react";
import { useNavigate } from "react-router-dom";
import "./LOGIN.css";

const LOGIN = () => {
  const navigate = useNavigate();

  const onRectangleClick = useCallback(() => {
    navigate("/sign-up");
  }, [navigate]);

  return (
    <div className="login3">
      <img className="login-child" alt="" src="/rectangle-33@2x.png" />
      <div className="navbar2">
        <div className="navbar-child5" />
        <div className="ai-interviews2">AI INTERVIEWS</div>
        <div className="login4">Login</div>
        <div className="products2">Products</div>
        <div className="solutions2">Solutions</div>
        <div className="navbar-child6" />
        <div className="navbar-child7" />
        <div className="demo2">Demo</div>
        <img className="navbar-child8" alt="" src="/line-1.svg" />
      </div>
      <div className="login-item" />
      <div className="login-inner" />
      <div className="login5">LOGIN</div>
      <div className="username">USERNAME</div>
      <div className="password3">PASSWORD</div>
      <div className="login-child1" />
      <div className="username1">USERNAME</div>
      <div className="password4">PASSWORD</div>
      <div className="login-child2" />
      <div className="login6">LOGIN</div>
      <div className="login-child3" onClick={onRectangleClick} />
      <div className="sign-up3">Sign up</div>
      <img className="login-child4" alt="" src="/arrow-1.svg" />
      <div className="or-1">--- or ----</div>
      <img className="login-child5" alt="" src="/rectangle-51@2x.png" />
    </div>
  );
};

export default LOGIN;
