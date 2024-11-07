import React, { useState, useEffect,useRef } from 'react';
import axios from 'axios';
import Traffic_light from './signal';
import './admin_panel.css'
import src1 from'../../assets/src1.mp4' 
import src2 from'../../assets/src2.mp4' 
import src3 from'../../assets/src3.mp4' 
import src4 from'../../assets/src4.mp4' 

const Admin_panel = () => {
  const [signals, setSignals] = useState({});
  const [currentGreen, setCurrentGreen] = useState(null);
  const [denistyScore,setDensityScore] = useState("NA");
  const [timerId, setTimerId] = useState(null);

  const greenSignalRef = useRef(null);
  const greenTimeRef = useRef(null);
  const videoRefs = useRef([]);

  useEffect(() => {
    fetchStatus();
  }, []);

  useEffect(() => {
    if (currentGreen !== null) {
      if (timerId) {
        clearInterval(timerId);
      }
      const id = setInterval(() => updateTiming(currentGreen), 1000); 
      setTimerId(id);
    }
  }, [currentGreen]);

  const fetchStatus = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/traffic_signal/send_timing'); 
      const data = response.data;
      console.log(data);
      setSignals(data); 
      setCurrentGreen(data["currentGreen"]); 
      setDensityScore(data["densityScore"]);
    } catch (error) {
      console.error("Error fetching status", error);
    }
  };

  const updateTiming = (greenSignal) => {
    setSignals(prevSignals => {
      const updatedSignals = { ...prevSignals }; 
     
      
      for (let i = 0; i < 4; i++) { 
        const signal = updatedSignals[i]; 

        if (i === greenSignal) {
          videoRefs.current[i].play();
          if (signal.timing.green > 0) {
            signal.timing.green -= 1; 
          } else if (signal.timing.green === 0) {
            signal.active_signal = "yellow";
            if (signal.timing.yellow > 0) {
              signal.timing.yellow -= 1; 
            } else if (signal.timing.yellow === 0) {
              fetchStatus();
            }
          }
        } else {
          videoRefs.current[i].pause();
          signal.timing.red = signal.timing.red > 0 ? signal.timing.red - 1 : 0; 
        }
      }

      return updatedSignals; 
    });
  };

  const handleStop = async () => {
    try {
      videoRefs.current[currentGreen].pause();
      await axios.post('http://127.0.0.1:5000/traffic_signal/stop'); 
      if (timerId) {
        clearInterval(timerId); 
        setTimerId(null); 
      }
    } catch (error) {
      console.error("Error stopping the signal", error);
    }
  };

  const handleResume = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/traffic_signal/resume'); 
      if (!timerId) {
        const id = setInterval(() => updateTiming(currentGreen), 1000); 
        setTimerId(id);
      }
    } catch (error) {
      console.error("Error resuming the signal", error);
    }
  };

  const handleUpdate = async ()=> {
    const new_green_signal = parseInt(greenSignalRef.current.value, 10)-1;
    const new_green_time = parseInt(greenTimeRef.current.value, 10);
    

    const new_timings = {
      "new_green_signal": new_green_signal,
      "new_green_time": new_green_time
    };
    try{
      await axios.post('http://127.0.0.1:5000/traffic_signal/update_signal',new_timings);
      fetchStatus();
      setDensityScore("NA")
    } 
    catch (error) {
      console.error("Error updating the signal", error);
    } 
  }

  const handleAnpr = async()=>{
    try{
      await axios.get('http://127.0.0.1:5000/anpr'); 
    }
    catch(error){
      console.error("Error updating the signal", error);
    }
  }

  const handleArialAnpr = async()=>{
    try{
      await axios.get('http://127.0.0.1:5000/arial_anpr'); 
    }
    catch(error){
      console.error("Error updating the signal", error);
    }
  }

  const handleTracking = async()=>{
    try{
      await axios.get('http://127.0.0.1:5000/track_vehicle'); 
    }
    catch(error){
      console.error("Error updating the signal", error);
    }
  }

  const handleLogDownload = async()=>{
    try{
      const response = await axios.get('http://127.0.0.1:5000/download_logs', {
        responseType: 'blob', 
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'traffic_logs.zip'); 
    document.body.appendChild(link);
    link.click();
    link.remove();
    window.URL.revokeObjectURL(url);
    console.log("Log downloaded");
    }
    catch(error){
      console.error("Error updating the signal", error);
    }
  }


  return (
    <div id="signal_board_container">
  <div id="signal_board">
    <div id="main">
      <div id="hor">
        <div className="arrow">
          <span>Signal 4 →</span>
        </div>
        <div className="arrow">
          <span>← Signal 2</span>
        </div>
      </div>

      <div id="ver">
        <div className="arrow">
          <span>↓ Signal 1</span>
        </div>
        <div className="arrow">
          <span>↑ Signal 3</span>
        </div>
      </div>

      {/* Cards for each signal */}
      <div id="card1" className="card">
        <div className="video-container">
          <video 
                  muted 
                  ref={ele => videoRefs.current[0] = ele}>
            <source src={src1} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="traffic-signal">
          <Traffic_light signals={signals} key={0} keyIndex={0} />
        </div>
      </div>

      <div id="card2" className="card">
        <div className="traffic-signal">
            <Traffic_light signals={signals} key={1} keyIndex={1} />
        </div>
        <div className="video-container">
          <video 
                  muted 
                  ref={ele => videoRefs.current[1] = ele}>
            <source src={src2} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        
      </div>

      <div id="card3" className="card">
        <div className="traffic-signal">
          <Traffic_light signals={signals} key={2} keyIndex={2} />
        </div>
        <div className="video-container">
          <video 
                  muted 
                  ref={ele => videoRefs.current[2] = ele}>
            <source src={src3} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        
      </div>

      <div id="card4" className="card">
        <div className="video-container">
          <video 
                  muted 
                  ref={ele => videoRefs.current[3] = ele}>
            <source src={src4} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
        </div>
        <div className="traffic-signal">
            <Traffic_light signals={signals} key={3} keyIndex={3} />
          </div>
      </div>
    </div>
  </div>

  {/* side panel control */}
  <div id="control_panel">
    <center><h2 >CONTROL PANEL</h2> </center>
    <hr className="divider" />
    <div>
        <select id="location-select">
            <option value="" disabled >Select a location</option>
            <option value="location1" selected>Sriperumbudur</option>
            <option value="location2">Tambaram</option>
            <option value="location3">Mogapair</option>
        </select>
    </div>

    <button onClick={handleStop} className="control-button" style={{"backgroundColor": "#990000"}}>Stop Signal</button>
    <button onClick={handleResume} className="control-button" style={{"backgroundColor": "#006a4e"}}>Resume Signal</button> 

    <div className="input-container">
        <input 
            type="text" 
            id="green-signal" 
            placeholder="Enter Green Signal" 
            ref={greenSignalRef}
        />
    </div>

    <div className="input-container">

        <input 
            type="number" 
            id="green-time" 
            placeholder="Enter Green Time"
            ref={greenTimeRef} 
        />
    </div>

    <button onClick={handleUpdate} className="control-button" style={{"backgroundColor": "#006666"}}>Update Signal</button>
    <button onClick={handleTracking} className="control-button util">Vehicle Tracking</button>
    <button onClick={handleAnpr} className="control-button util">ANPR</button>
    <button onClick={handleArialAnpr} className="control-button util">Arial ANPR</button>
    <button onClick={handleLogDownload} className="control-button util1">Download Logs</button>
    <center><bold><h3>Density Score :{denistyScore} </h3></bold> </center>
    
  </div>


</div>

  );
};

export default Admin_panel;


