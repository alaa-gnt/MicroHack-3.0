import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

mermaid.initialize({
    startOnLoad: true,
    theme: 'base',
    themeVariables: {
        primaryColor: '#1d4ed8',
        primaryTextColor: '#fff',
        primaryBorderColor: '#1e3a8a',
        lineColor: '#555',
        secondaryColor: '#00d1b2',
        tertiaryColor: '#fff',
    },
    securityLevel: 'loose',
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
                backgroundColor: '#fff',
                padding: '20px',
                borderRadius: '8px',
                border: '1px solid #e5e7eb'
            }}
        >
            {chart}
        </div>
    );
};

export default Mermaid;
