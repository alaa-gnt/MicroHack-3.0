import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
    startOnLoad: true,
    theme: 'neutral',
    securityLevel: 'loose',
    flowchart: {
        useMaxWidth: true,
        htmlLabels: true,
        curve: 'basis'
    }
});

const Mermaid = ({ chart }) => {
    const mermaidRef = useRef(null);

    useEffect(() => {
        if (mermaidRef.current && chart) {
            mermaidRef.current.removeAttribute('data-processed');
            mermaid.contentLoaded();
        }
    }, [chart]);

    return (
        <div
            className="mermaid"
            ref={mermaidRef}
            style={{
                width: '100%',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                minHeight: '100%'
            }}
        >
            {chart}
        </div>
    );
};

export default Mermaid;
