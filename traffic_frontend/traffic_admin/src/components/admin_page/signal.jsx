import React from "react";
import './Traffic_light.css';

const Traffic_light = ({ signals, keyIndex }) => {  
  console.log(signals);
  console.log(keyIndex);
  const active = signals[keyIndex] ? signals[keyIndex].active_signal : null;
  
  return (
    active && signals[keyIndex] ? (
      <div key={keyIndex} className="traffic-light-container">
        <div className="traffic-light">
          <div className={`light ${active === 'red' ? 'active' : ''}`}></div>
          <div className={`light ${active === 'yellow' ? 'active' : ''}`}></div>
          <div className={`light ${active === 'green' ? 'active' : ''}`}></div>
        </div>
        <div className="pole"></div>
        <div className="timer">
          {signals[keyIndex].timing[active]}s
        </div>
        <h5 style ={{color:'black',fontWeight:'bolder',fontFamily:'monospace'}}>SIGNAL {parseInt(keyIndex) + 1}</h5>
      </div>
    ) : null
  );
};

export default Traffic_light;
