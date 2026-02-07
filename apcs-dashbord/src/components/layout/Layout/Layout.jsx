import React from 'react';
import './Layout.css';
import Sidebar from '../Sidebar/Sidebar';
import Header from '../Header/Header';

const Layout = ({ children }) => {
    return (
        <div className="layout-root">
            <Sidebar />
            <div className="main-wrapper">
                <Header />
                <main className="content-container">
                    {children}
                </main>
            </div>
        </div>
    );
};

export default Layout;
