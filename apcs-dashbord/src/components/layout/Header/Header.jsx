import React from "react";
import "./Header.css";
import { Search, Home, Bell } from "lucide-react";

const Header = () => {
  return (
    <header className="header">
      <div className="search-container">
        <Search className="search-icon" size={18} />
        <input type="text" placeholder="Search" className="search-input" />
      </div>

      <div className="header-actions">
        <button className="action-btn">
          <Home size={18} />
          <span>home</span>
        </button>
        <button className="action-btn">
          <Bell size={18} />
          <span>Notifications</span>
        </button>
      </div>
    </header>
  );
};

export default Header;
