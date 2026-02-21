import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import { loginAPI, verifyToken, logoutAPI } from "../services/authService";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // Check existing token on mount
  useEffect(() => {
    // 🧪 TEMPORARY TEST BYPASS
    setUser({
      id: 'user_001',
      email: 'admin@apcs.com',
      name: 'Test Admin',
      role: 'admin',
    });
    setIsAuthenticated(true);
    setLoading(false);
  }, []);

  const login = useCallback(async (credentials) => {
    const response = await loginAPI(credentials);
    localStorage.setItem("authToken", response.token);
    localStorage.setItem("authUser", JSON.stringify(response.user));
    setUser(response.user);
    setIsAuthenticated(true);
    return response;
  }, []);

  const logout = useCallback(() => {
    logoutAPI();
    setUser(null);
    setIsAuthenticated(false);
  }, []);

  return (
    <AuthContext.Provider
      value={{ user, loading, isAuthenticated, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
};
