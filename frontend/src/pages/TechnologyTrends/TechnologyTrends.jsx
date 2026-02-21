import React from "react";
import "./TechnologyTrends.css";
import TechnologyTrendsChart from "../../components/charts/TechnologyTrendsChart/TechnologyTrendsChart";
import TechnologyRadarChart from "../../components/charts/TechnologyRadarChart/TechnologyRadarChart";
import { useTechnologyTrends } from "../../hooks/useTechnologyTrends";
import { useRadarData } from "../../hooks/useRadarData";

const TechnologyTrends = () => {
  const { data: trendsData, loading: trendsLoading } = useTechnologyTrends();
  const { data: radarData, loading: radarLoading } = useRadarData();

  return (
    <div className="trends-container">
      <h1 className="trends-page-title">Dashboard</h1>

      {/* Section 1: Technology Trends Line Chart */}
      <section className="trends-section">
        <div className="trends-section-header">
          <h2 className="trends-section-title">Technology Trends</h2>
        </div>

        <TechnologyTrendsChart data={trendsData} loading={trendsLoading} />
      </section>

      {/* Section 2: Radar Graph */}
      <section className="radar-section">
        <div className="radar-layout">
          <div className="radar-text-block">
            <h2 className="radar-title">Radar graph</h2>
            <p className="radar-description">
              Distribution of technologies across the TRL scale (1-9). Research
              (TRL 1-3) represents basic concepts, Prototype (TRL 4-6) shows
              validated technologies, Demo (TRL 7-8) indicates field-tested
              systems, and Deployment (TRL 9) marks commercial-ready solutions.
            </p>
          </div>
          <div className="radar-chart-block">
            <TechnologyRadarChart data={radarData} loading={radarLoading} />
          </div>
        </div>
      </section>
    </div>
  );
};

export default TechnologyTrends;
