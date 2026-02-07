import React, { useState } from "react";
import "./SignalsInbox.css";
import FilterTabs from "../../components/common/FilterTabs/FilterTabs";
import SignalCard from "../../components/signals/SignalCard/SignalCard";
import { useSignals } from "../../hooks/useSignals";

const FILTER_TABS = ["All", "Ai", "IoT", "Blockchain", "Security"];

const SignalsInbox = () => {
  const [activeTab, setActiveTab] = useState("All");
  const { signals, loading, error, acceptSignal, rejectSignal } =
    useSignals(activeTab);

  return (
    <div className="signals-inbox-page">
      {/* Filter tabs */}
      <FilterTabs
        tabs={FILTER_TABS}
        activeTab={activeTab}
        onTabChange={setActiveTab}
      />

      {/* Page title */}
      <h1 className="signals-inbox-title">Signals Inbox</h1>

      {/* Loading state */}
      {loading && (
        <div className="signals-loading">
          {[1, 2].map((i) => (
            <div key={i} className="signal-skeleton">
              <div className="skel-title" />
              <div className="skel-body">
                <div className="skel-line w60" />
                <div className="skel-line w100" />
                <div className="skel-line w80" />
                <div className="skel-line w40" />
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="signals-error">
          <p>Failed to load signals. Please try again.</p>
        </div>
      )}

      {/* Empty state */}
      {!loading && !error && signals.length === 0 && (
        <div className="signals-empty">
          <p>No signals found for "{activeTab}" category.</p>
        </div>
      )}

      {/* Signal cards */}
      {!loading && !error && signals.length > 0 && (
        <div className="signals-inbox-list">
          {signals.map((signal) => (
            <SignalCard
              key={signal.id}
              signal={signal}
              onAccept={acceptSignal}
              onReject={rejectSignal}
            />
          ))}
        </div>
      )}

      {/* View all link */}
      {!loading && signals.length > 0 && (
        <div className="signals-view-all-row">
          <button className="signals-view-all-btn">View all</button>
        </div>
      )}
    </div>
  );
};

export default SignalsInbox;
