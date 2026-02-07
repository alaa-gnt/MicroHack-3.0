import React from "react";
import "./StatCard.css";
import { ArrowRight } from "lucide-react";
import { motion } from "framer-motion";

const StatCard = ({ title, value, subtitle, trend, type }) => {
  return (
    <motion.div
      className={`stat-card ${type || ""}`}
      whileHover={{ y: -4 }}
      transition={{ type: "spring", stiffness: 300, damping: 20 }}
    >
      <div className="stat-header">
        <h3 className="stat-title">{title}</h3>
        <button className="stat-action-circle">
          <ArrowRight size={16} />
        </button>
      </div>

      <p className="stat-subtitle">{subtitle}</p>

      <div className="stat-value-row">
        <span className="stat-value">{value}</span>
      </div>

      {type === "alerts" ? (
        <div className="alert-breakdown">
          <div className="alert-item critical">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path
                d="M2 7h10M7 2l5 5-5 5M7 2L2 7l5 5"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            02 Critical
          </div>
          <div className="alert-item minors">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path
                d="M2 7h10M7 2l5 5-5 5M7 2L2 7l5 5"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
            03 Minors
          </div>
        </div>
      ) : trend ? (
        <div className="stat-trend-row">
          <span className={`stat-trend ${type}`}>{trend}</span>
        </div>
      ) : null}
    </motion.div>
  );
};

export default StatCard;
