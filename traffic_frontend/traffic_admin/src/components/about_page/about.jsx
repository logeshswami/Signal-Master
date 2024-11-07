import React from 'react';
import './About.css'; 

const About = () => {
    return (
        <div className="about-container">
            <div className="about-content">
                <h2> Intelligent Traffic Signal Management</h2>
                <p>
                    Welcome to <strong>Signal Master</strong>, the ultimate solution for managing traffic signals with efficiency and precision. Designed for administrators and traffic management professionals, Signal Master utilizes advanced density-based timing allocation to optimize traffic flow and enhance road safety.
                </p>
                <h3>Our Mission</h3>
                <p>
                    At Signal Master, our mission is to provide a smart traffic management system that adapts to real-time traffic conditions, ensuring smoother and safer journeys for all road users.
                </p>
                <h3>Key Features</h3>
                <ul>
                    <li>Real-time traffic density analysis</li>
                    <li>Adaptive signal timing based on traffic conditions</li>
                    <li>User-friendly interface for efficient control</li>
                    <li>Comprehensive analytics for decision-making</li>
                </ul>
                <p>
                    Join us in revolutionizing traffic management and making our roads safer and more efficient. Thank you for choosing Signal Master!
                </p>
            </div>
        </div>
    );
};

export default About;
