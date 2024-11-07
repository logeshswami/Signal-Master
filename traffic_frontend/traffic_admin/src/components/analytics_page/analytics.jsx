import React from "react";
import dayTrafficData from '../../assets/data/VehicleTrendDay.json';
import weeklyTrafficData from '../../assets/data/VehicleTrendWeek.json';
import { useState } from "react";
import { 
    LineChart, 
    Line, 
    XAxis, 
    YAxis, 
    CartesianGrid, 
    Tooltip, 
    Legend, 
    ResponsiveContainer, 
    PieChart, 
    Pie,  
    Cell, 
    ScatterChart, 
    Scatter 
} from 'recharts';

const GraphContainer = {
    top: '130px',
    left: '50px',
    right: '50px',
    display: 'flex',
    position: 'absolute',
    boxSizing: 'border-box',
    backgroundColor: '#dcdcdc',
    flexDirection: 'column',
    height: 'calc(100vh - 150px)',
    borderRadius: '5px',
};

const TopContainer = {
    flex: '1',
    paddingTop: '3px',
    paddingRight: '30px',
    backgroundColor: '#dcdcdc',
    borderRadius: '5px',
};

const BottomContainer = {
    flex: '1',
    display: 'flex',
    borderRadius: '5px',
};

const SubContainer1 = {
    flex: '1',
    backgroundColor: '#dcdcdc',
    borderRadius: '5px',
    borderBottomRightRadius: '0'
};

const SubContainer2 = {
    flex: '1',
    paddingTop: '13px',
    paddingRight: '25px',
    backgroundColor: '#dcdcdc',
    borderRadius: '5px',
    borderBottomLeftRadius: '0'
};

const DropDownContainer = {
    top: '75px',
    right: '20px',
    left: '20px',
    width: '50%',
    display: 'flex',
    justifyContent: 'center',
    margin: '0 auto',
    position: 'absolute',
  };

const renderPieLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, value, index, COLORS, pieData }) => {
    const RADIAN = Math.PI / 180;
    const radius = 25 + innerRadius + (outerRadius - innerRadius);
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    return (
        <text
            x={x}
            y={y}
            fill={COLORS[index % COLORS.length]}
            textAnchor={x > cx ? "start" : "end"}
            dominantBaseline="central"
        >
            {pieData[index].name} ({value})
        </text>
    );
};

const Analytics = ()=>{

    const [selectedTime, setSelectedOption] = useState('day');

    const options = [
    { value: 'day', label: 'Today' },
    { value: 'week', label: 'This Week' },
    // { value: 'month', label: 'This Month' },
    ];

    const handleChange = (event) => {
    setSelectedOption(event.target.value);
    };

    let data = [];
    if (selectedTime === 'day') {
        data = dayTrafficData.dayTrafficData.map(item => ({
            time: item.time,
            Cars: item.counts.Cars,
            Triwheels: item.counts.Triwheels,
            Vans: item.counts.Vans,
            Bikes: item.counts.Bikes,
            Buses: item.counts.Buses,
            Trucks: item.counts.Trucks,
        }));
    } else {
        data = weeklyTrafficData.weeklyTrafficData.map(item => ({
            day: item.day,
            Cars: item.counts.Cars,
            Triwheels: item.counts.Triwheels,
            Vans: item.counts.Vans,
            Bikes: item.counts.Bikes,
            Buses: item.counts.Buses,
            Trucks: item.counts.Trucks,
        }));
    }

    const vehicleTypes = ['Cars', 'Trucks', 'Bikes', 'Buses', 'Triwheels', 'Vans'];
    const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#FF6699', '#A26A8D'];
    
    const pieData = vehicleTypes.map(type => ({
        name: type,
        value: data.reduce((acc, item) => acc + item[type], 0),
    }));
    
    const scatterData = data.map(item => ({
        time: item.time,
        totalCount: item.Cars + item.Trucks + item.Bikes + item.Buses + item.Vans + item.Triwheels,
    }));

    return (
        <>
        <div style={DropDownContainer}>
        <div style={{ width: '100%', position: 'relative' }}>
          <select
            style={{
              width: '100%',
              height: '100%',
              padding: '5px',
              appearance: 'none',
              border: '1px solid #ccc',
              borderRadius: '4px',
              backgroundColor: 'white',
            }}
            value={selectedTime}
            onChange={handleChange}
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </div>
        <div style={GraphContainer}>
            <div style={TopContainer}>
                <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <Legend />
                        <XAxis dataKey="time" />
                        <YAxis />
                        <Tooltip />
                        <Line type="linear" dataKey="Cars" stroke="#0088FE" />
                        <Line type="linear" dataKey="Trucks" stroke="#00C49F" />
                        <Line type="linear" dataKey="Bikes" stroke="#FFBB28" />
                        <Line type="linear" dataKey="Buses" stroke="#FF8042" />
                        <Line type="linear" dataKey="Triwheels" stroke="#FF6699" />
                        <Line type="linear" dataKey="Vans" stroke="#A26A8D" />
                    </LineChart>
                </ResponsiveContainer>
            </div>
            <div style={BottomContainer}>
                <div style={SubContainer1}>
                    <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                            <Pie 
                                data={pieData} 
                                cx="50%" 
                                cy="50%" 
                                labelLine={false} 
                                outerRadius={100} 
                                fill="#8884d8" 
                                dataKey="value"
                                label={(props) => renderPieLabel({ ...props, COLORS, pieData })}
                            >
                                {pieData.map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                ))}
                            </Pie>
                            <Legend />
                            <Tooltip />
                        </PieChart>
                    </ResponsiveContainer>
                </div>
                <div style={SubContainer2}>
                    <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart>
                            <CartesianGrid />
                            <XAxis dataKey="time" name="Time" />
                            <YAxis dataKey="totalCount" name="Total Count" />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                            <Legend />
                            <Scatter name="Traffic" data={scatterData} fill="#ff0000" />
                        </ScatterChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
        </>
    );
}
export default Analytics;