import React from "react";
import { AlertTriangle } from "lucide-react";
import "./PipelineProjectCard.css";

const STATUS_COLORS = {
  orange: "#F59E0B",
  green: "#16A34A",
  blue: "#3B3FFF",
  red: "#DC2626",
};

const PipelineProjectCard = ({ project, onAction }) => {
  const dotColor = STATUS_COLORS[project.statusColor] || STATUS_COLORS.orange;

  return (
    <div className="pipeline-project-card">
      <div className="pipeline-project__left">
        {/* Stage badge */}
        <div className="pipeline-project__badge">
          <span
            className="pipeline-project__dot"
            style={{ backgroundColor: "#3B3FFF" }}
          />
          <span className="pipeline-project__stage">{project.stageName}</span>
        </div>


        <h3 className="pipeline-project__title">{project.title}</h3>


        <p className="pipeline-project__desc">{project.description}</p>


        <div className="pipeline-project__meta">
          <span className="pipeline-project__source">
            {project.source}
          </span>
          <span
            className="pipeline-project__status"
            style={{ color: dotColor }}
          >
            <AlertTriangle size={14} />
            {project.status}
          </span>
        </div>
      </div>

      <div className="pipeline-project__right">
        <span className="pipeline-project__time">{project.timestamp}</span>
        <button
          className="pipeline-project__action"
          onClick={() => onAction && onAction(project)}
        >
          {project.actionLabel}
        </button>
      </div>
    </div>
  );
};

export default PipelineProjectCard;
