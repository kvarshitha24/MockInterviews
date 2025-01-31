import React, { useEffect, useState } from 'react';
import axios from 'axios'; // Import Axios
import './UserReports.css'; // Import the CSS file

const UserReports = () => {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/users')
      .then(response => {
        setUsers(response.data);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
      });
  }, []);

  return (
    <div className="container">
      {users.map(user => (
        <div className="card" key={user.email}>
          <h2>{user.name}</h2>
          {user.has_report ? (
            // Update the href to correctly call the backend API to serve the report
            <a href={`http://127.0.0.1:5000/report/${user.email}`} target="_blank" rel="noopener noreferrer">
              View Report
            </a>
          ) : (
            <p>No report available</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default UserReports;
