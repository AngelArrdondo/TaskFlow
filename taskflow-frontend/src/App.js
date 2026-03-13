import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import TareaList from './components/TareaList';
import EtiquetaList from './components/EtiquetaList';
import './App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Navbar />
        <div className="container">
          <Routes>
            <Route path="/" element={<TareaList />} />
            <Route path="/etiquetas" element={<EtiquetaList />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;