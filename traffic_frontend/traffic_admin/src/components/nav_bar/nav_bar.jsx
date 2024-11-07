import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navbar.css'; 

const Navbar = ({ userName }) => {
const navigate = useNavigate(); 

  return (
    <nav className="navbar">
      <div className="navbar-left">
        <h2>SignalMaster</h2>
      </div>
      <div className="navbar-center">
      <button className="nav-button" onClick={() => navigate('/About')}>
          <h3>Home</h3>
        </button>
        <button className="nav-button" onClick={() => navigate('/control-panel')}>
          <h3>Control Panel</h3>
        </button>
        <button className="nav-button" onClick={() => navigate('/analytics')}>
          <h3>Analytics</h3>
        </button>
      </div>
      <div className="navbar-right">
        <span className="user-name">Welcome, {userName}</span>
        <button className="nav-button logout">Logout</button>
      </div>
    </nav>
  );
};

export default Navbar;