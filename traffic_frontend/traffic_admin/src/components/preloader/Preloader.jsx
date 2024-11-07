import React from 'react';
import './preloader.css';
import traffic from '../../assets/final-traffic.gif';

function Preloader() {
  return (
    <div className='preloader-container'>
        <h1>Welcome to SignalMaster!</h1>
        <img src={traffic} alt="Welcome" />
    </div>
  )
}

export default Preloader
