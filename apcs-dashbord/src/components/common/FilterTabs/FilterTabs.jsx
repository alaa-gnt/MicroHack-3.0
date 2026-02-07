import React from "react";
import "./FilterTabs.css";

const FilterTabs = ({ tabs, activeTab, onTabChange }) => {
  return (
    <div className="filter-tabs-bar">
      {tabs.map((tab) => (
        <button
          key={tab}
          className={`filter-tab ${activeTab === tab ? "active" : ""}`}
          onClick={() => onTabChange(tab)}
        >
          {tab}
        </button>
      ))}
    </div>
  );
};

export default FilterTabs;
