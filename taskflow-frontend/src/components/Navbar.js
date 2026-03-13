import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          TaskFlow
        </Link>
        <ul className="nav-menu">
          <li className="nav-item">
            <Link 
              to="/" 
              className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
            >
              Tareas
            </Link>
          </li>
          <li className="nav-item">
            <Link 
              to="/etiquetas" 
              className={`nav-link ${location.pathname === '/etiquetas' ? 'active' : ''}`}
            >
              Etiquetas
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;