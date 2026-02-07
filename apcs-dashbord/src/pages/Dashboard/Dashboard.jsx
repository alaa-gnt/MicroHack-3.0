import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./Dashboard.css";
import StatCard from "../../components/dashboard/StatCard/StatCard";
import TechnologySignal from "../../components/dashboard/TechnologySignal/TechnologySignal";
import { Bot, Link2, ArrowRight, Activity, AlertTriangle, Layers } from "lucide-react";
import { api } from "../../services/api";

const Dashboard = () => {
  const [stats, setStats] = useState([
    {
      title: "Total Signals",
      value: "...",
      subtitle: "how many signals entered the pipeline",
      trend: "Loading...",
      type: "signals",
      icon: Activity
    },
    {
      title: "Projects Active",
      value: "...",
      subtitle: "How many projects are currently alive",
      type: "projects",
      icon: Layers
    },
    {
      title: "POC's Running",
      value: "...",
      subtitle: "Experiments in progress",
      trend: "Loading...",
      type: "poc",
      icon: Bot
    },
    {
      title: "Alerts Today",
      value: "...",
      subtitle: "Problems that need attention",
      type: "alerts",
      icon: AlertTriangle
    },
  ]);

  const [signals, setSignals] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // 1. Fetch Signals
        const signalsData = await api.get('/signals?limit=5');

        // Transform backend signal data to frontend format
        const formattedSignals = signalsData.map(signal => ({
          id: signal.id,
          title: signal.title,
          titleHighlight: signal.title.split(' ').slice(0, 1).join(' '),
          source: signal.source_name,
          time: new Date(signal.date).toLocaleDateString(),
          urgency: signal.analysis?.urgency_score?.toString() || "0",
          impact: signal.analysis?.impact_score?.toString() || "0",
          tags: signal.analysis?.primary_domain ? [signal.analysis.primary_domain] : ["Research"],
          icon: Bot,
        }));
        setSignals(formattedSignals);

        // 2. Fetch Analytics/Dashboard Stats
        const dashboardData = await api.get('/analytics/dashboard');

        // Update Stats with real metrics
        setStats([
          {
            title: "Total Signals",
            value: dashboardData.metrics?.total_signals?.toString().padStart(2, '0') || "00",
            subtitle: "how many signals entered the pipeline",
            trend: "+12% from last week",
            type: "signals",
            icon: Activity
          },
          {
            title: "Projects Active",
            value: dashboardData.metrics?.active_projects?.toString().padStart(2, '0') || "00",
            subtitle: "How many projects are currently alive",
            type: "projects",
            icon: Layers
          },
          {
            title: "POC's Running",
            value: dashboardData.metrics?.running_pocs?.toString().padStart(2, '0') || "00",
            subtitle: "Experiments in progress",
            trend: "2 nearing completion",
            type: "poc",
            icon: Bot
          },
          {
            title: "Alerts Today",
            value: dashboardData.metrics?.alerts_today?.toString().padStart(2, '0') || "00",
            subtitle: "Problems that need attention",
            type: "alerts",
            icon: AlertTriangle
          },
        ]);

      } catch (error) {
        console.error("Failed to fetch dashboard data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1 className="dashboard-title">Dashboard</h1>
        <p className="dashboard-description">
          This dashboard provides a real-time overview of the transportation
          pipeline, tracking each stage from signal detection to deployment,
          enabling faster decisions, better coordination, and improved
          operational efficiency
        </p>
      </header>

      <section className="stats-grid">
        {stats.map((stat, index) => (
          <StatCard key={index} {...stat} />
        ))}
      </section>

      <section className="signals-section">
        <div className="signals-header">
          <h2 className="signals-section-title">Recent Technology Signals</h2>
          <button className="view-all-btn">View all</button>
        </div>

        <div className="signals-list">
          {loading ? (
            <p>Loading signals...</p>
          ) : (
            signals.map((signal) => (
              <TechnologySignal key={signal.id} {...signal} />
            ))
          )}
          {!loading && signals.length === 0 && <p>No signals found.</p>}
        </div>

        <div className="fab-container">
          <Link to="/technology-trends" className="fab-btn">
            <ArrowRight size={20} />
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
