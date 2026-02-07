import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
    ArrowLeft,
    Layout,
    Code,
    Shield,
    BarChart3,
    Terminal,
    Github,
    Copy,
    CheckCircle2,
    FileCode,
    Network,
    Download,
    Loader2
} from "lucide-react";
import { getBlueprintByOpportunity, generateBlueprint } from "../../services/blueprintService";
import Mermaid from "../../components/common/Mermaid/Mermaid";
import "./BlueprintWorkspace.css";

const BlueprintWorkspace = () => {
    const { opportunityId } = useParams();
    const navigate = useNavigate();
    const [blueprint, setBlueprint] = useState(null);
    const [loading, setLoading] = useState(true);
    const [generating, setGenerating] = useState(false);
    const [error, setError] = useState(null);
    const [copied, setCopied] = useState(false);

    useEffect(() => {
        const fetchBlueprint = async () => {
            try {
                setLoading(true);
                const data = await getBlueprintByOpportunity(opportunityId);
                setBlueprint(data);
            } catch (err) {
                // If 404, we just show the generate button
                console.warn("No blueprint found, ready to generate.");
            } finally {
                setLoading(false);
            }
        };

        fetchBlueprint();
    }, [opportunityId]);

    const handleGenerate = async () => {
        try {
            setGenerating(true);
            setError(null);
            const data = await generateBlueprint(opportunityId);
            setBlueprint(data);
        } catch (err) {
            setError("Strategic generation failed. Please check your AI connection.");
        } finally {
            setGenerating(false);
        }
    };

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    if (loading) {
        return (
            <div className="signals-inbox-page">
                <div className="blueprint-loading">
                    <Loader2 className="spinner" size={48} />
                    <p>Accessing the Strategic Design Vault...</p>
                </div>
            </div>
        );
    }

    if (!blueprint && !generating) {
        return (
            <div className="signals-inbox-page">
                <div className="blueprint-empty-state">
                    <Terminal size={64} className="terminal-icon" />
                    <h1>Venture Blueprint Pending</h1>
                    <p>This opportunity is ready for high-fidelity architectural mapping.</p>
                    <button onClick={handleGenerate} className="generate-blueprint-btn">
                        Generate Day-Zero Blueprint
                    </button>
                    <button onClick={() => navigate(-1)} className="back-btn-secondary">
                        Return to Analysis
                    </button>
                </div>
            </div>
        );
    }

    if (generating) {
        return (
            <div className="signals-inbox-page">
                <div className="blueprint-loading">
                    <div className="pulse-ai"></div>
                    <h2>Architecting Your Venture...</h2>
                    <p>The AI is now generating technical specs, v0 prompts, and GitHub manifests.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="signals-inbox-page blueprint-page">
            <header className="blueprint-header">
                <div className="header-top">
                    <button onClick={() => navigate(-1)} className="back-link">
                        <ArrowLeft size={16} /> Back to Strategic Analysis
                    </button>
                    <div className="blueprint-badge">DAY-ZERO READY</div>
                </div>
                <div className="header-main">
                    <h1>Autonomous Venture Blueprint</h1>
                    <p className="subtitle">From Approved Idea to Implementation-Ready Codebase</p>
                </div>
            </header>

            <div className="blueprint-content">
                {/* Left Column: Technical Specifications */}
                <div className="blueprint-specs-column">
                    <section className="blueprint-spec-card">
                        <div className="card-header">
                            <Layout size={20} className="icon" />
                            <h2>System Architecture</h2>
                        </div>
                        <div className="card-body">
                            <p>{blueprint.system_architecture}</p>
                        </div>
                    </section>

                    <section className="blueprint-spec-card">
                        <div className="card-header">
                            <Code size={20} className="icon" />
                            <h2>Data Schema (Models)</h2>
                        </div>
                        <div className="card-body code-style">
                            <pre>{blueprint.data_schema}</pre>
                        </div>
                    </section>

                    <div className="spec-row">
                        <section className="blueprint-spec-card">
                            <div className="card-header">
                                <Shield size={20} className="icon" />
                                <h2>Security Protocols</h2>
                            </div>
                            <div className="card-body">
                                <p>{blueprint.security_protocols}</p>
                            </div>
                        </section>

                        <section className="blueprint-spec-card">
                            <div className="card-header">
                                <BarChart3 size={20} className="icon" />
                                <h2>KPI Metrics</h2>
                            </div>
                            <div className="card-body">
                                <p>{blueprint.kpi_metrics}</p>
                            </div>
                        </section>
                    </div>
                </div>

                {/* Right Column: v0, GitHub, and Logic Flow */}
                <div className="blueprint-assets-column">
                    {/* v0.dev Accelerator */}
                    <section className="blueprint-tool-card v0-card">
                        <div className="card-header">
                            <Zap size={20} className="icon" />
                            <h2>v0.dev Prompt Package</h2>
                        </div>
                        <div className="card-body">
                            <p className="tool-desc">Paste this into v0.dev or Claude Artifacts to generate the professional UI.</p>
                            <div className="prompt-container">
                                <p className="prompt-text">{blueprint.v0_prompt}</p>
                                <button
                                    className="copy-prompt-btn"
                                    onClick={() => copyToClipboard(blueprint.v0_prompt)}
                                >
                                    {copied ? <CheckCircle2 size={16} /> : <Copy size={16} />}
                                    {copied ? "Copied" : "Copy Prompt"}
                                </button>
                            </div>
                        </div>
                    </section>

                    {/* Logic Visualizer */}
                    <section className="blueprint-tool-card logic-card">
                        <div className="card-header">
                            <Network size={20} className="icon" />
                            <h2>Digital Brain (Logic Flow)</h2>
                        </div>
                        <div className="card-body">
                            <Mermaid chart={blueprint.mermaid_flow} />
                        </div>
                    </section>

                    {/* Day-Zero Repo */}
                    <section className="blueprint-tool-card github-card">
                        <div className="card-header">
                            <Github size={20} className="icon" />
                            <h2>GitHub Manifest (Day-Zero)</h2>
                        </div>
                        <div className="card-body">
                            <div className="manifest-files">
                                <div className="file-item">
                                    <FileCode size={16} />
                                    <span>package.json</span>
                                </div>
                                <div className="file-item">
                                    <FileCode size={16} />
                                    <span>README.md</span>
                                </div>
                                <div className="file-item">
                                    <FileCode size={16} />
                                    <span>.env.example</span>
                                </div>
                            </div>
                            <button className="download-manifest-btn">
                                <Download size={16} /> Download Project Package
                            </button>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default BlueprintWorkspace;

// Simple Zap icon as lucide-react might not have it or I want to ensure it works
const Zap = ({ size, className }) => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width={size}
        height={size}
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
    </svg>
);
