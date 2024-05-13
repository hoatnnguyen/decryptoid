import React, { useState } from 'react'
import axios from 'axios'
import { Link, useNavigate } from 'react-router-dom'

const SignUp = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [usernameError, setUsernameError] = useState('');
    const [emailError, setEmailError] = useState('');
    const [passwordError, setPasswordError] = useState('');
    const [responseError, setResponseError] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        const usernamePattern = /^[a-zA-Z0-9_-]+$/;
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!username.trim()) {
            setUsernameError("Please enter a username.");
            return;
        }
        if (!usernamePattern.test(username.trim())) {
            setUsernameError('Username can only contain English letters (capitalized or not), digits, "_" (underscore), and "-" (dash).');
            return;
        }
        if (username.trim().length < 3) {
            setUsernameError('Username must be at least 3 characters.');
            return;
        }
        if (!email.trim()) {
            setEmailError("Please enter an email address.");
            return;
        }
        if (!emailPattern.test(email)) {
            setEmailError('Please enter a valid email address.');
            return;
        }
        if (!password.trim()) {
            setPasswordError('Please enter a password.');
            return;
        }
        if (password.length < 8) {
            setPasswordError('Password must be at least 8 characters.');
            return;
        }

        const formData = {
            username,
            email,
            password
        };

        console.log(formData);
        try {
            const response = await axios.post("http://127.0.0.1:8000/signup", formData);
            console.log('Response from the backend:', response.data);
            navigate("/login");
        } catch (error) {
            setResponseError(error.response.data.detail);
            console.error('Error: ', error);
        }
    }

    return (
        <div className="min-vh-100 d-flex justify-content-center align-items-center">
            <div className="container">
                <div className="row">
                    <div className="col-sm-9 col-md-7 col-lg-5 mx-auto">
                        <div className="card border-0 shadow rounded-3 my-5">
                            <div className="card-body p-4 p-sm-5">
                                <h2 className="card-title text-center mb-5">Sign Up</h2>
                                <form onSubmit={handleSubmit}>
                                    {responseError && <div className="text-danger mb-2">{responseError}</div>}
                                    <div className="form-floating mb-4">
                                        <input type="text" className={`form-control ${usernameError && 'is-invalid'}`} id="username" placeholder="username"
                                            value={username}
                                            onChange={(e) => {
                                                setUsername(e.target.value);
                                                setUsernameError('');
                                            }}
                                        />
                                        <label htmlFor="username">Username</label>
                                        {usernameError && <div className="invalid-feedback">{usernameError}</div>}
                                    </div>
                                    <div className="form-floating mb-4">
                                        <input type="email" className={`form-control ${emailError && 'is-invalid'}`} id="email" placeholder="name@example.com"
                                            value={email}
                                            onChange={(e) => {
                                                setEmail(e.target.value);
                                                setEmailError('');
                                            }}
                                        />
                                        <label htmlFor="email">Email Address</label>
                                        {emailError && <div className="invalid-feedback">{emailError}</div>}
                                    </div>
                                    <div className="form-floating mb-4">
                                        <input type="password" className={`form-control ${passwordError && 'is-invalid'}`} id="password" placeholder="Password"
                                            value={password}
                                            onChange={(e) => {
                                                setPassword(e.target.value);
                                                setPasswordError('');
                                            }}
                                        />
                                        <label htmlFor="password">Password</label>
                                        {passwordError && <div className="invalid-feedback">{passwordError}</div>}
                                    </div>
                                    <div className="d-grid">
                                        <button className="btn btn-primary btn-login text-uppercase fw-bold" type="submit">Sign
                                            Up</button>
                                    </div>
                                    <div className="pt-3">
                                        Have an account?
                                        <Link to="/login"> Sign in </Link> now
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default SignUp
