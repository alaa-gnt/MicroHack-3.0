import React from "react";
import "./TechnologySignal.css";

const TechnologySignal = ({
  title,
  titleHighlight,
  source,
  time,
  urgency,
  impact,
  tags,
  icon: Icon,
}) => {
  const renderTitle = () => {
    if (!titleHighlight) return <span>{title}</span>;
    const parts = title.split(new RegExp(`(${titleHighlight})`, "i"));
    return parts.map((part, i) =>
      part.toLowerCase() === titleHighlight.toLowerCase() ? (
        <span key={i} className="title-highlight">
          {part}
        </span>
      ) : (
        <span key={i}>{part}</span>
      ),
    );
  };

  return (
    <div className="signal-card">
      <div className="signal-header">
        {Icon && <Icon className="signal-icon" size={20} />}
        <h4 className="signal-title">{renderTitle()}</h4>
      </div>

      <div className="signal-meta">
        <span className="meta-source">{source}</span>
        <span className="meta-sep">|</span>
        <span className="meta-time">{time}</span>
        <span className="meta-sep">|</span>
        <span className="meta-urgency">Urgency : {urgency}</span>
        <span className="meta-sep">|</span>
        <span className="meta-impact">Impact : {impact}</span>
      </div>

      <div className="signal-tags">
        <span className="tag-arrow">→</span>
        {tags.map((tag, index) => (
          <React.Fragment key={tag}>
            <span className="tag-name">{tag}</span>
            {index < tags.length - 1 && <span className="tag-sep">|</span>}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
};

export default TechnologySignal;
