# Signal Master - Automated Traffic Signal Management System

Signal Master is an intelligent, AI-driven traffic management application that utilizes a **Flask backend** and a **React frontend**. The system is designed to optimize traffic signal timing dynamically based on real-time traffic density, leveraging computer vision and deep learning techniques such as **YOLO** for vehicle detection, **DeepSORT** for vehicle tracking, and additional utilities like **ANPR (Automatic Number Plate Recognition)**. This solution provides city authorities with a comprehensive dashboard to control and monitor traffic flow, effectively managing congestion in urban areas.

## Project Abstract

Rapid urbanization and the ever-increasing number of vehicles have made effective traffic management a critical challenge for cities globally. Traditional traffic systems rely on fixed timings, leading to inefficiencies, longer waiting times, and congestion, especially during peak hours. Signal Master addresses this by automating traffic management through real-time analysis of traffic density, vehicle types, and movement patterns using CCTV footage. The system dynamically adjusts signal timings based on these insights, enabling smoother vehicle flow and reducing congestion at intersections.

This adaptive approach uses machine learning algorithms to monitor and predict traffic patterns, providing a more responsive solution compared to static traffic lights. Additionally, the system can leverage historical data to anticipate traffic surges, adjusting signal timings proactively. By implementing Signal Master, cities can benefit from reduced travel times, lower fuel consumption, decreased emissions, and improved road safety. Scalable across various urban settings, Signal Master represents a significant step towards smarter, more efficient urban traffic management.

## Key Features

1. **Automatic Traffic Signal Management**:
   - Dynamically adjusts traffic light timings based on real-time traffic density.
   - Efficiently manages traffic flow, reducing congestion and waiting times.

2. **Density-Based Signal Timing Allocation**:
   - Uses YOLO object detection to assess vehicle density in real-time.
   - Calculates optimal green light duration for each signal based on density, improving traffic efficiency.

3. **Vehicle Tracking with DeepSORT**:
   - Continuously monitors individual vehicle trajectories to gather insights on traffic movement patterns.
   - Enables more detailed traffic data collection, which contributes to better signal timing predictions.

4. **ANPR (Automatic Number Plate Recognition)**:
   - Integrates YOLO and EasyOCR for accurate number plate recognition, assisting with vehicle identification and traffic rule enforcement.

5. **Admin Dashboard**:
   - Provides a centralized control panel to manage and monitor traffic signals dynamically.
   - Displays real-time signal status , traffic densities, signal statuses, and provides options to control and override the automatic system when necessary , vehicle tracking , ANPR  download traffic logs and view analytics.

6. **Scalability and Flexibility**:
   - Capable of deployment in small towns to large metropolitan areas, with the ability to integrate additional functionalities, such as violation detection and emergency vehicle prioritization.
