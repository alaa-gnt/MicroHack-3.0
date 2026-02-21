import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
    ArrowLeft,
    Settings,
    Database,
    TrendingUp,
    CheckCircle,
    AlertTriangle,
    FileText,
    Binary,
    ShieldCheck,
    Zap,
    Rocket
} from "lucide-react";
import ReactMarkdown from 'react-markdown';
import { getFeasibilityByOpportunity } from "../../services/feasibilityService";
import "./FeasibilityDetail.css";

const FeasibilityDetail = () => {
    const { opportunityId } = useParams();
    const navigate = useNavigate();
    const [study, setStudy] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchStudy = async () => {
            try {
                setLoading(true);
                const data = await getFeasibilityByOpportunity(opportunityId);
                setStudy(data);
            } catch (err) {
                setError("Technical connection to analysis vault failed.");
            } finally {
                setLoading(false);
            }
        };

        fetchStudy();
    }, [opportunityId]);

    if (loading) return (
        <div className="signals-inbox-page">
            <div className="feasibility-loading">
                <div className="spinner"></div>
                <p>Expert Agents are retrieving technical blueprints...</p>
            </div>
        </div>
    );

    if (error || !study) return (
        <div className="signals-inbox-page">
            <div className="feasibility-error-container">
                <div className="error-card">
                    <AlertTriangle size={48} color="#DC2626" />
                    <h2>Strategic Analysis Missing</h2>
                    <p>{error || "A feasibility study for this specific opportunity hasn't been finalized yet. Please check back after the next agent cycle."}</p>
                    <button onClick={() => navigate(-1)} className="back-btn-error">Return to Opportunity Sheets</button>
                </div>
            </div>
        </div>
    );

    const getStatusClass = (status) => {
        if (status === "GO") return "status-go";
        if (status === "MAYBE") return "status-maybe";
        return "status-no-go";
    };

    return (
        <div className="signals-inbox-page feasibility-detail-page">
            <header className="feasibility-header">
                <div className="header-top">
                    <button onClick={() => navigate(-1)} className="back-link">
                        <ArrowLeft size={16} /> Back
                    </button>
                    <div className={`feasibility-status-badge ${getStatusClass(study.overall_feasibility)}`}>
                        {study.overall_feasibility === "GO" ? <ShieldCheck size={14} /> : <Zap size={14} />}
                        STATUS: {study.overall_feasibility}
                    </div>
                </div>
                <h1 className="signals-inbox-title">Project Feasibility Deep-Dive</h1>
            </header>

            <div className="feasibility-sections">
                {/* Technical Assessment */}
                <section className="feasibility-section">
                    <div className="section-header">
                        <Settings className="section-icon" size={24} />
                        <h2>Technical Assessment</h2>
                    </div>
                    <div className="section-content markdown-body">
                        <ReactMarkdown>{study.technical_assessment}</ReactMarkdown>
                    </div>
                </section>

                {/* Market Analysis */}
                <section className="feasibility-section">
                    <div className="section-header">
                        <TrendingUp className="section-icon" size={24} />
                        <h2>Strategic Intelligence</h2>
                    </div>
                    <div className="section-content markdown-body">
                        <ReactMarkdown>{study.market_analysis}</ReactMarkdown>
                    </div>
                </section>

                {/* Recommendation */}
                <section className="feasibility-section recommendation-section">
                    <div className="section-header">
                        <CheckCircle className="section-icon" size={24} />
                        <h2>Executive Verdict</h2>
                    </div>
                    <div className="section-content highlighted markdown-body">
                        <ReactMarkdown>{study.final_recommendation}</ReactMarkdown>
                    </div>
                </section>
            </div>

            <section className="action-footer">
                <div className="action-container">
                    <p>Ready to move forward? Generate the architecture and diagrams.</p>
                    <button
                        onClick={() => navigate(`/blueprint/${study.opportunity_id}`)}
                        className="help-implementation-btn"
                    >
                        Help me with implementation
                        <ArrowLeft size={20} style={{ transform: 'rotate(180deg)' }} />
                    </button>
                </div>
            </section>

            <footer className="feasibility-footer">
                <div className="audit-info">
                    <FileText size={14} />
                    <span>Report ID: {study.id.substring(0, 8).toUpperCase()}</span>
                    <span className="separator">|</span>
                    <Binary size={14} />
                    <span>Opportunity Link: {study.opportunity_id.substring(0, 8)}</span>
                </div>
            </footer>
        </div>
    );
};

export default FeasibilityDetail;
