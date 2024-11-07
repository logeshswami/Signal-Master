import './App.css'
import { BrowserRouter as Router, Route, Routes, Navigate} from 'react-router-dom';
import About from './components/about_page/about.jsx';
import Analytics from './components/analytics_page/analytics.jsx';
import Admin_panel from './components/admin_page/admin_panel.jsx'
import Navbar from './components/nav_bar/nav_bar.jsx'
import Preloader from './components/preloader/Preloader.jsx';
import { useEffect, useState } from 'react';

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setIsLoading(false), 4000);
  }, []);

  return (
    <>
      {
        isLoading? <Preloader /> : <Router>
        <div>
          <Navbar userName="Srini" /> 
          <div className="pages">
            <Routes>
              <Route path="/" element={<Navigate to="/about" />} />
              <Route path="/control-panel" element={<Admin_panel />} />
              <Route path="/analytics" element={<Analytics />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </div>
        </div>
      </Router>
      }
    </>
  );
}

export default App
