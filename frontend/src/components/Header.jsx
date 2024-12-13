import React from 'react';
import '../styles/Header.css';
const Header = () => {
  return (<>    <header>
      <h1>MarketMate</h1>
      <nav>
        <a href="#home">Compare</a>
        <a href="#about">Trends</a>
        <a href="#contact">FAQ</a>
        <a href="#account">Register</a>
      </nav>
    </header>
      <div className="search-bar">
        <input type="text" placeholder="Search products..." />
      </div>
      </>

  );
};

export default Header;
