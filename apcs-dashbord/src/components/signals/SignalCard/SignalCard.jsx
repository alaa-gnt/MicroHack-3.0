import React from "react";
import "./SignalCard.css";

const STATUS_COLORS = {
  New: { text: "#16A34A", dot: "#16A34A" },
  "In Review": { text: "#D97706", dot: "#D97706" },
  Accepted: { text: "#1D4ED8", dot: "#1D4ED8" },
  Rejected: { text: "#DC2626", dot: "#DC2626" },
};

const SignalCard = ({ signal, onAccept, onReject }) => {
  const statusColor = STATUS_COLORS[signal.status] || STATUS_COLORS["New"];
  const isActionable =
    signal.status !== "Accepted" && signal.status !== "Rejected";

  return (
    <div className="signal-inbox-card">
      {/* Blue title above the card body */}
      <h3 className="signal-card-title">{signal.title}</h3>

      {/* Card body */}
      <div className="signal-card-body">
        {/* Header row: category | system + View more */}
        <div className="signal-card-header-row">
          <div className="signal-card-category-row">
            <span className="signal-card-category">
              Category : {signal.category}
            </span>
            <span className="signal-card-pipe">|</span>
            <span className="signal-card-system">{signal.system}</span>
          </div>
          <button className="signal-view-more">View more</button>
        </div>

        {/* Description */}
        <div className="signal-card-description">
          <span className="desc-label">Description :</span>
          <p className="desc-text">{signal.description}</p>
        </div>

        {/* Metadata row */}
        <div className="signal-card-meta">
          <span className="meta-time">{signal.timestamp}</span>
          <span className="meta-impact">
            Impact score : {signal.impactScore}
          </span>
          <span className="meta-urgency">
            Urgency score : {signal.urgencyScore}
          </span>
        </div>

        {/* Status + Actions row */}
        <div className="signal-card-footer">
          <div className="signal-status-badge">
            <span className="status-label">Status : </span>
            <span className="status-value" style={{ color: statusColor.text }}>
              {signal.status}
            </span>
            <span
              className="status-dot"
              style={{ backgroundColor: statusColor.dot }}
            />
          </div>

          {isActionable && (
            <div className="signal-card-actions">
              <button
                className="signal-action-btn accept-btn"
                onClick={() => onAccept(signal.id)}
              >
                Accept
              </button>
              <button
                className="signal-action-btn reject-btn"
                onClick={() => onReject(signal.id)}
              >
                Reject
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SignalCard;
