import React from 'react';
import '../styles/Header.css';
import logo from '../assets/icon/logo.png'
const Header = () => {
  return (<>    <header>
      <div className="icon">
      <img  src={logo} height="32px" width="32px" alt="logo" />
      <h1>MarketMate</h1>
        </div>  
      <nav>
        <a href="#home">Compare</a>
        <a href="#about">Trends</a>
        <a href="#contact">FAQ</a>
        <a href="#account">Register</a>
      </nav>
    </header>
      <div className="search-bar">
        <input type="text" placeholder="Search Component..." />
      </div>
      </>

  );
};

export default Header;
