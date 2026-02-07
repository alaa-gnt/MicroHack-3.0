import React, { useState, useEffect, useCallback } from "react";
import { X } from "lucide-react";
import "./InnovationPipeline.css";
import usePipelineData from "../../hooks/usePipelineData";
import PipelineStageCard from "../../components/pipeline/PipelineStageCard/PipelineStageCard";
import PipelineProjectCard from "../../components/pipeline/PipelineProjectCard/PipelineProjectCard";

const InnovationPipeline = () => {
  const { stages, recentProjects, loading, error, fetchStageProjects } =
    usePipelineData();

  // Modal state
  const [modalStage, setModalStage] = useState(null);
  const [modalProjects, setModalProjects] = useState([]);
  const [modalLoading, setModalLoading] = useState(false);

  const handleStageClick = useCallback(
    async (stage) => {
      setModalStage(stage);
      setModalLoading(true);
      const projects = await fetchStageProjects(stage.id);
      setModalProjects(projects);
      setModalLoading(false);
    },
    [fetchStageProjects],
  );

  const closeModal = () => setModalStage(null);

  // ESC to close modal
  useEffect(() => {
    const onKey = (e) => {
      if (e.key === "Escape") closeModal();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  return (
    <div className="pipeline-page">
      {/* Header */}
      <h1 className="pipeline-page__title">Innovation Pipeline</h1>
      <p className="pipeline-page__subtitle">
        Tracking innovation from signal detection to deployment
      </p>

      {/* Loading skeleton for stages */}
      {loading && (
        <div className="pipeline-stages-grid">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="stage-card-skeleton">
              <div className="skel-bar w60" />
              <div className="skel-blue" />
              <div className="skel-bar w40 skel-btn" />
            </div>
          ))}
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="pipeline-error">
          <p>{error}</p>
        </div>
      )}

      {/* Stage cards */}
      {!loading && !error && (
        <div className="pipeline-stages-grid">
          {stages.map((stage) => (
            <PipelineStageCard
              key={stage.id}
              stage={stage}
              onClick={handleStageClick}
            />
          ))}
        </div>
      )}

      {/* Recent Projects */}
      {!loading && !error && recentProjects.length > 0 && (
        <div className="pipeline-projects-section">
          {recentProjects.map((proj) => (
            <PipelineProjectCard
              key={proj.id}
              project={proj}
              onAction={(p) => console.log("Action:", p.id)}
            />
          ))}
        </div>
      )}

      {/* ── Stage Projects Modal ── */}
      {modalStage && (
        <div
          className="pipeline-modal-overlay"
          onClick={(e) => {
            if (e.target === e.currentTarget) closeModal();
          }}
        >
          <div className="pipeline-modal" role="dialog" aria-modal="true">
            <button
              className="pipeline-modal__close"
              onClick={closeModal}
              aria-label="Close"
            >
              <X size={18} strokeWidth={3} />
            </button>
            <h2 className="pipeline-modal__title">
              {modalStage.name} Projects
              <span className="pipeline-modal__count">
                {" "}
                — {modalStage.count} total
              </span>
            </h2>

            <div className="pipeline-modal__body">
              {modalLoading && (
                <p className="pipeline-modal__loading">Loading…</p>
              )}
              {!modalLoading && modalProjects.length === 0 && (
                <p className="pipeline-modal__empty">
                  No projects in this stage yet.
                </p>
              )}
              {!modalLoading &&
                modalProjects.map((proj) => (
                  <PipelineProjectCard
                    key={proj.id}
                    project={{
                      ...proj,
                      stageName: modalStage.name,
                    }}
                    onAction={(p) => console.log("Action:", p.id)}
                  />
                ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default InnovationPipeline;
