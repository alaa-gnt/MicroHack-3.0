import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./Login.css";

const Login = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [formData, setFormData] = useState({ email: "", password: "" });
  const [errors, setErrors] = useState({});
  const [apiError, setApiError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [shake, setShake] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) setErrors((prev) => ({ ...prev, [name]: "" }));
    if (apiError) setApiError("");
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.email) {
      newErrors.email = "Email is required";
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = "Email is invalid";
    }
    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) {
      setShake(true);
      setTimeout(() => setShake(false), 500);
      return;
    }

    setIsLoading(true);
    setApiError("");
    try {
      await login(formData);
      navigate("/");
    } catch (err) {
      setApiError(err.message || "Login failed. Please try again.");
      setShake(true);
      setTimeout(() => setShake(false), 500);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        {/* Left welcome panel */}
        <div className="login-welcome">
          <div className="login-welcome__overlay" />
          <div className="login-welcome__content">
            <h1 className="login-welcome__title">Welcome !</h1>
            <p className="login-welcome__desc">
              Discover emerging technologies, track innovation projects, and
              drive digital transformation across port operations.
            </p>
          </div>
        </div>

        {/* Right form panel */}
        <div className="login-form-panel">
          <form
            className={`login-form${shake ? " login-form--shake" : ""}`}
            onSubmit={handleSubmit}
            noValidate
          >
            <h2 className="login-form__title">Log in</h2>

            {apiError && (
              <p className="login-form__api-error" role="alert">
                {apiError}
              </p>
            )}

            <div className="login-form__group">
              <label className="login-form__label" htmlFor="email">
                E-mail :
              </label>
              <input
                id="email"
                name="email"
                type="email"
                className={`login-form__input${errors.email ? " has-error" : ""}`}
                value={formData.email}
                onChange={handleChange}
                autoComplete="email"
                aria-invalid={!!errors.email}
                aria-describedby={errors.email ? "email-error" : undefined}
                disabled={isLoading}
              />
              {errors.email && (
                <span
                  className="login-form__error"
                  id="email-error"
                  role="alert"
                >
                  {errors.email}
                </span>
              )}
            </div>

            <div className="login-form__group">
              <label className="login-form__label" htmlFor="password">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                className={`login-form__input${errors.password ? " has-error" : ""}`}
                value={formData.password}
                onChange={handleChange}
                autoComplete="current-password"
                aria-invalid={!!errors.password}
                aria-describedby={
                  errors.password ? "password-error" : undefined
                }
                disabled={isLoading}
              />
              {errors.password && (
                <span
                  className="login-form__error"
                  id="password-error"
                  role="alert"
                >
                  {errors.password}
                </span>
              )}
            </div>

            <button
              type="submit"
              className="login-form__btn"
              disabled={isLoading}
            >
              {isLoading ? "Logging in\u2026" : "Log in"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
