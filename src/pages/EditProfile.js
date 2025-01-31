import React, { useState, useEffect, useContext } from 'react';
import axios from 'axios';
import './EditProfile.css';
import { logincontext } from "../contexts/Logincontext";

const EditProfile = () => {
    const [formData, setFormData] = useState({
        photo: null,
        gender: '',
        dob: '',
        contact: '',
        institute: '',
        department: '',
        leetcodeUsername: '',
        codechefUsername: '',
        codeforcesUsername: '',
        address: '',
    });
    const [currentuser,loginerror,UserloginStatus,Loginuser,Logoutuser,isUser,isRecruiter,isAdmin] = useContext(logincontext);

    useEffect(() => {
        // Fetch user profile data when component mounts
        const fetchProfile = async () => {
            try {
                const response = await axios.get('http://127.0.0.1:5000/profile', {
                    params: { email: currentuser.email }
                });
                const profileData = response.data;
                setFormData(profileData);
            } catch (error) {
                console.error('Error fetching profile:', error);
                // Handle error fetching profile data
            }
        };
        if (UserloginStatus) {
            fetchProfile();
        }
    }, [UserloginStatus, currentuser.email]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleFileChange = (e) => {
        setFormData({ ...formData, photo: e.target.files[0] });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            console.log(formData);
            const filteredData = Object.keys(formData)
            .filter(key => formData[key] !== null && formData[key] !== '')
            .reduce((obj, key) => {
                obj[key] = formData[key];
                return obj;
            }, {});
            const response = await axios.post('http://127.0.0.1:5000/editprofile', {
                email: currentuser.email,
                data: filteredData
            });
            console.log('Profile updated successfully:', response.data);
            } catch (error) {
            console.error('Error updating profile:', error);
            // Handle error updating profile
        }
    };

    return (
        <div className="edit-profile-page">
            <h1>Edit Profile</h1>
            <form onSubmit={handleSubmit} className="edit-profile-form">
                <div className="form-row">
                    <label>
                        Profile Photo:
                        <input type="file" name="photo" onChange={handleFileChange} />
                    </label>
                    <label>
                        Name:
                        <p>{currentuser.first_name}</p>
                    </label>
                </div>
                <div className="form-row">
                    <label>
                        Gender:
                        <select name="gender" value={formData.gender} onChange={handleChange} required>
                            <option value="">Select Gender</option>
                            <option value="male">Male</option>
                            <option value="female">Female</option>
                            <option value="other">Other</option>
                        </select>
                    </label>
                    <label>
                        DOB:
                        <input type="date" name="dob" value={formData.dob} onChange={handleChange} required />
                    </label>
                </div>
                <div className="form-row">
                    <label>
                        Institute:
                        <input type="text" name="institute" value={formData.institute} onChange={handleChange} required />
                    </label>
                    <label>
                        Department:
                        <input type="text" name="department" value={formData.department} onChange={handleChange} required />
                    </label>
                </div>
                <div className="form-row">
                    <label>
                        Leetcode Username:
                        <input type="text" name="leetcodeUsername" value={formData.leetcodeUsername} onChange={handleChange} />
                    </label>
                    <label>
                        Codechef Username:
                        <input type="text" name="codechefUsername" value={formData.codechefUsername} onChange={handleChange} />
                    </label>
                </div>
                <div className="form-row">
                    <label>
                        Codeforces Username:
                        <input type="text" name="codeforcesUsername" value={formData.codeforcesUsername} onChange={handleChange} />
                    </label>
                    <label>
                        Email ID:
                        <p>{currentuser.email}</p>
                    </label>
                </div>
                <div className="form-row">
                    <label>
                        Contact No:
                        <input type="tel" name="contact" value={formData.contact} onChange={handleChange} required />
                    </label>
                    <label>
                        Address:
                        <textarea name="address" value={formData.address} onChange={handleChange} />
                    </label>
                </div>
                <button type="submit" className="save-button">Save</button>
            </form>
        </div>
    );
};

export default EditProfile;
