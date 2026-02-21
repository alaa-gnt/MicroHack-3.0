import React from 'react';
import './AlertBadge.css';

const AlertBadge = ({ type, count }) => {
    return (
        <div className={`alert-badge ${type}`}>
            {count}
        </div>
    );
};

export default AlertBadge;
