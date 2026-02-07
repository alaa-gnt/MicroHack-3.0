import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";
import { AuthProvider, useAuth } from "./context/AuthContext";
import Layout from "./components/layout/Layout/Layout";
import Login from "./pages/Login/Login";
import Dashboard from "./pages/Dashboard/Dashboard";
import TechnologyTrends from "./pages/TechnologyTrends/TechnologyTrends";
import SignalsInbox from "./pages/SignalsInbox/SignalsInbox";
import Alerts from "./pages/Alerts/Alerts";
import InnovationPipeline from "./pages/InnovationPipeline/InnovationPipeline";

const PrivateRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  return isAuthenticated ? children : <Navigate to="/login" replace />;
};

const PublicRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  if (loading) return null;
  return !isAuthenticated ? children : <Navigate to="/" replace />;
};

function AppRoutes() {
  return (
    <Routes>
      <Route
        path="/login"
        element={
          <PublicRoute>
            <Login />
          </PublicRoute>
        }
      />
      <Route
        path="/*"
        element={
          <PrivateRoute>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route
                  path="/technology-trends"
                  element={<TechnologyTrends />}
                />
                <Route path="/signals-inbox" element={<SignalsInbox />} />
                <Route path="/alerts" element={<Alerts />} />
                <Route
                  path="/innovation-pipeline"
                  element={<InnovationPipeline />}
                />
              </Routes>
            </Layout>
          </PrivateRoute>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;

