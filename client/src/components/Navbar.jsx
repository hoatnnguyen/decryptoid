import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

const Navbar = () => {
    const [accessToken, setAccessToken] = useState("");
    useEffect(() => {
        const storedAccessToken = sessionStorage.getItem('accessToken');
        if (storedAccessToken) {
            setAccessToken(storedAccessToken);
        }
    }, []);

    const handleLogOut = (e) => {
        e.preventDefault();

        sessionStorage.removeItem('accessToken');
        setAccessToken("");
        window.location.reload();
    }

    return (
        <nav className="navbar">
            {accessToken && <div className="container d-flex flex-row-reverse">
                <button className="signin-btn" onClick={handleLogOut}>Log Out</button>
            </div>}
            {!accessToken && <div className="container d-flex flex-row-reverse">
                <button className="signin-btn"><Link to="/login " className="signin-link">Log In</Link></button>
            </div>}
        </nav>
    )
}

export default Navbar
