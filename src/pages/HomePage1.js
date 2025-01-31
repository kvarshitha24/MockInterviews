import React from 'react';
import './HomePage1.css';
import { Link } from 'react-router-dom';

const Header = () => (
  <header className="header">
    <div className="header-content">
      <h1 className="header-title">Prepare & Succeed</h1>
      <p className="header-description">
        Ace your AI interviews with practice questions, expert feedback, and mock interviews.
      </p>
      <button className="get-started-btn">
        <Link to="/sign-up" className="get-started-link">
          <span className='get'>Get Started</span>
        </Link>
      </button>
    </div>
  </header>
);

const Feature = ({ imgSrc, altText, title, description }) => (
  <div className="feature">
    <img src={imgSrc} alt={altText} className="feature-icon large-icon" />
    <h3 className="feature-title">{title}</h3>
    <p className="feature-description">{description}</p>
  </div>
);

const Features = () => (
  <section className="features">
    <h2 className="section-title">Exclusive Features</h2>
    <div className="features-container">
      <Feature imgSrc="/screenshot-20240614-154026-1@2x.png" altText="Practice Questions" title="Practice Questions" description="Enhance your skills with a wide range of practice questions." />
      <Feature imgSrc="/mock-1@2x.png" altText="Mock Interviews" title="Mock Interviews" description="Experience realistic interview scenarios to prepare thoroughly." />
      <Feature imgSrc="/feedback-1@2x.png" altText="Expert Feedback" title="Expert Feedback" description="Receive detailed feedback from industry experts." />
      <Feature imgSrc="/performance-1@2x.png" altText="Performance Analytics" title="Performance Analytics" description="Track your performance with comprehensive analytics." />
    </div>
  </section>
);

const LiveInterviews = () => (
  <section className="live-interviews">
    <div className="live-interviews-content">
      <h2 className="live-interviews-title">Experience Live Interviews</h2>
      <p className="live-interviews-description">
        Our website offers live job interviews, allowing candidates to interact with employers in real-time. This feature facilitates instant connections, enabling quicker and more authentic hiring decisions. Candidates can showcase their skills and personalities directly, making a strong impression on potential employers.
      </p>
      <button className="live-interviews-btn">Explore Live Interviews</button>
    </div>
  </section>
);

const WhyChooseUs = () => (
  <section className="why-choose-us">
    <h2 className="section-title">Why Choose Us</h2>
    <div className="why-choose-us-container">
      <div className="why-choose-us-feature">Feature 1</div>
      <div className="why-choose-us-feature">Feature 2</div>
      <div className="why-choose-us-feature">Feature 3</div>
      <div className="why-choose-us-feature">Feature 4</div>
      <div className="why-choose-us-feature">Feature 5</div>
      <div className="why-choose-us-feature">Feature 6</div>
    </div>
  </section>
);

const HomePage1 = () => {
  return (
    <main className="home-page">
      <Header />
      <Features />
      <LiveInterviews />
      <WhyChooseUs />
    </main>
  );
};

export default HomePage1;
