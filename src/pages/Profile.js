import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Profile.css';
import { logincontext } from "../contexts/Logincontext";
import { Link } from'react-router-dom';
import { useContext } from "react";

const Profile = () => {
  const [currentuser,loginerror,UserloginStatus,Loginuser,Logoutuser,isUser,isRecruiter,isAdmin] = useContext(logincontext);
  const [profileData, setProfileData] = useState(currentuser);

  useEffect(() => {
    const fetchProfileData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/profile', {
          params: { email: currentuser.email ,role:currentuser.role },
        });  
        // Ensure response.data.data is properly set
        setProfileData(response.data.data);
      } catch (error) {
        console.error('Error fetching profile data:', error);
        // Handle error fetching profile data
      }
    };

    if (UserloginStatus) {
      fetchProfileData();
    }
  }, [UserloginStatus, currentuser.email]);

  // Log profileData to check its value
  console.log(profileData);

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-header-left">
          <img className="profile-avatar" alt="Profile Avatar" src="/ellipse-25@2x.png" />
          <Link to ="/editprofile">
            <button className="edit-button">Edit Profile</button>
          </Link>
        </div>
        <div className="profile-details">
          <h2 className="section-title">Profile Details</h2>
          {profileData.first_name? (  // Check if profileData.name or any other required field exists
            <>
              <div className="detail-item">
                <strong>Name:</strong> <span className="detail-value">{profileData.first_name}</span>
              </div>
              <div className="detail-item">
                <strong>Department:</strong> <span className="detail-value">{profileData.department}</span>
              </div>
              <div className="detail-item">
                <strong>DOB:</strong> <span className="detail-value">{profileData.dob}</span>
              </div>
              <div className="detail-item">
                <strong>Leetcode Username:</strong> <span className="detail-value">{profileData.leetcodeUsername}</span>
              </div>
              <div className="detail-item">
                <strong>Codechef Username:</strong> <span className="detail-value">{profileData.codechefUsername}</span>
              </div>
              <div className="detail-item">
                <strong>Address:</strong> <span className="detail-value">{profileData.address}</span>
              </div>
            </>
          ) : (
            <p>Loading profile data...</p>
          )}
        </div>
      </div>
      <div className="profile-main">
        <div className="profile-performance">
          <h2 className="section-title">Performance Analysis</h2>
          <div className="performance-stats">
            <div className="stat-item">
              <p>Attended</p>
              <h3>12</h3>
            </div>
            <div className="stat-item">
              <p>Average Duration</p>
              <h3>45 mins</h3>
            </div>
            <div className="stat-item">
              <p>Average Score</p>
              <h3>85%</h3>
            </div>
            <div className="stat-item">
              <p>Contest Rating</p>
              <h3>1716</h3>
            </div>
          </div>
          <div className="performance-graph">
            {/* Placeholder for performance graph */}
            <p>Graph Placeholder</p>
          </div>
        </div>
        <div className="recent-interviews">
          <h2 className="section-title">Recent Interviews</h2>
          <table className="interviews-table">
            <thead>
              <tr>
                <th>Interview Number</th>
                <th>Date</th>
                <th>Time</th>
                <th>Score</th>
                <th>Analysis Report</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>1</td>
                <td>2024-06-01</td>
                <td>10:00 AM</td>
                <td>85</td>
                <td><button className="report-button">View Report</button></td>
              </tr>
              <tr>
                <td>2</td>
                <td>2024-06-05</td>
                <td>11:30 AM</td>
                <td>90</td>
                <td><button className="report-button">View Report</button></td>
              </tr>
              <tr>
                <td>3</td>
                <td>2024-06-10</td>
                <td>02:00 PM</td>
                <td>78</td>
                <td><button className="report-button">View Report</button></td>
              </tr>
              <tr>
                <td>4</td>
                <td>2024-06-15</td>
                <td>09:00 AM</td>
                <td>88</td>
                <td><button className="report-button">View Report</button></td>
              </tr>
            </tbody>
          </table>
          <button className="see-more-button">See More</button>
        </div>
      </div>
    </div>
  );
};

export default Profile;
