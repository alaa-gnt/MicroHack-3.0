import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import "./Sidebar.css";
import {
  LayoutDashboard,
  Search,
  Lightbulb,
  Bell,
  Settings,
  LogOut,
} from "lucide-react";
import { useAuth } from "../../../context/AuthContext";

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { logout } = useAuth();

  const menuItems = [
    {
      icon: <LayoutDashboard size={20} />,
      label: "Dashboard",
      id: "dashboard",
      path: "/",
    },
    {
      icon: <Search size={20} />,
      label: "Signals Inbox",
      id: "signals",
      path: "/signals-inbox",
    },
    {
      icon: <Lightbulb size={20} />,
      label: "Innovation Pipeline",
      id: "pipeline",
      path: "/innovation-pipeline",
    },
    {
      icon: <Bell size={20} />,
      label: "Alerts",
      id: "alerts",
      path: "/alerts",
    },
  ];

  const generalItems = [
    { icon: <Settings size={20} />, label: "Settings", id: "settings" },
    { icon: <LogOut size={20} />, label: "Log out", id: "logout" },
  ];

  const isActive = (path) => {
    if (path === "/") return location.pathname === "/";
    return location.pathname.startsWith(path);
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-section">
        <p className="section-title">Menu</p>
        <ul className="menu-list">
          {menuItems.map((item) => (
            <li
              key={item.id}
              className={`menu-item ${isActive(item.path) ? "active" : ""}`}
              onClick={() => navigate(item.path)}
            >
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-label">{item.label}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="sidebar-section footer">
        <p className="section-title">General</p>
        <ul className="menu-list">
          {generalItems.map((item) => (
            <li
              key={item.id}
              className="menu-item"
              onClick={() => {
                if (item.id === "logout") {
                  logout();
                  navigate("/login");
                }
              }}
            >
              <span className="menu-icon">{item.icon}</span>
              <span className="menu-label">{item.label}</span>
            </li>
          ))}
        </ul>
      </div>
    </aside>
  );
};

export default Sidebar;
