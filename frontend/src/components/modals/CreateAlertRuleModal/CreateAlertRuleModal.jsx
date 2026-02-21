import React, { useState, useEffect, useCallback, useRef } from "react";
import { X } from "lucide-react";
import "./CreateAlertRuleModal.css";
import { createAlertRule } from "../../../services/alertRulesService";

const INITIAL_FORM_STATE = {
  alertName: "",
  categories: {
    ai: false,
    blockchain: false,
    iot: false,
    cybersecurity: false,
    allCategories: false,
  },
  minimumScores: {
    impact: 80,
    urgency: 60,
  },
};

const CreateAlertRuleModal = ({ isOpen, onClose, onSuccess }) => {
  const [formData, setFormData] = useState(INITIAL_FORM_STATE);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const modalRef = useRef(null);
  const inputRef = useRef(null);

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen) {
      setFormData(INITIAL_FORM_STATE);
      setError(null);
      // Focus on input after animation
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // ESC key to close
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape" && isOpen) onClose();
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [isOpen, onClose]);

  // Click outside to close
  const handleBackdropClick = (e) => {
    if (e.target === e.currentTarget) onClose();
  };

  // Input change
  const handleInputChange = (e) => {
    setFormData({ ...formData, alertName: e.target.value });
  };

  // Category change with "All categories" logic
  const handleCategoryChange = useCallback((category) => {
    setFormData((prev) => {
      const newCategories = { ...prev.categories };

      if (category === "allCategories") {
        const newValue = !newCategories.allCategories;
        return {
          ...prev,
          categories: {
            ai: newValue,
            blockchain: newValue,
            iot: newValue,
            cybersecurity: newValue,
            allCategories: newValue,
          },
        };
      }

      newCategories[category] = !newCategories[category];

      // Check if all individual categories are selected
      const allSelected =
        newCategories.ai &&
        newCategories.blockchain &&
        newCategories.iot &&
        newCategories.cybersecurity;
      newCategories.allCategories = allSelected;

      return { ...prev, categories: newCategories };
    });
  }, []);

  // Slider change
  const handleSliderChange = (scoreType, value) => {
    setFormData({
      ...formData,
      minimumScores: { ...formData.minimumScores, [scoreType]: Number(value) },
    });
  };

  // Submit
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!formData.alertName.trim()) {
      setError("Alert name is required");
      return;
    }
    const hasCategory = Object.entries(formData.categories).some(
      ([key, val]) => key !== "allCategories" && val,
    );
    if (!hasCategory) {
      setError("Please select at least one category");
      return;
    }

    setIsSubmitting(true);
    try {
      const result = await createAlertRule(formData);
      onSuccess && onSuccess(result);
      onClose();
    } catch {
      setError("Failed to create alert rule. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) return null;

  const categories = [
    { key: "ai", label: "Ai" },
    { key: "blockchain", label: "Blockchain" },
    { key: "iot", label: "IoT" },
    { key: "cybersecurity", label: "Cybersecurity" },
  ];

  return (
    <div className="modal-overlay" onClick={handleBackdropClick}>
      <div
        className="modal-container"
        ref={modalRef}
        role="dialog"
        aria-modal="true"
      >
        {/* Close button */}
        <button
          className="modal-close-btn"
          onClick={onClose}
          aria-label="Close modal"
        >
          <X size={18} strokeWidth={3} />
        </button>

        {/* Title */}
        <h2 className="modal-title">Create a new Alerts Rule</h2>

        <form onSubmit={handleSubmit}>
          {/* Alert Name */}
          <label className="form-label blue">Alert name :</label>
          <input
            ref={inputRef}
            type="text"
            className="form-input"
            value={formData.alertName}
            onChange={handleInputChange}
            autoComplete="off"
          />

          {/* Category */}
          <label className="form-label blue category-label">Category :</label>
          <div className="checkbox-grid">
            {categories.map((cat) => (
              <label key={cat.key} className="checkbox-item">
                <input
                  type="checkbox"
                  checked={formData.categories[cat.key]}
                  onChange={() => handleCategoryChange(cat.key)}
                />
                <span className="checkbox-custom" />
                <span className="checkbox-label">{cat.label}</span>
              </label>
            ))}
          </div>
          <label className="checkbox-item all-categories">
            <input
              type="checkbox"
              checked={formData.categories.allCategories}
              onChange={() => handleCategoryChange("allCategories")}
            />
            <span className="checkbox-custom" />
            <span className="checkbox-label">All categories</span>
          </label>

          {/* Select the minimum */}
          <label className="form-label black slider-section-label">
            Select the minimum :
          </label>

          {/* Impact Score Slider */}
          <div className="slider-row">
            <span className="slider-label">Impact score</span>
            <input
              type="range"
              min="0"
              max="100"
              value={formData.minimumScores.impact}
              onChange={(e) => handleSliderChange("impact", e.target.value)}
              className="slider-input"
              style={{
                "--value": `${formData.minimumScores.impact}%`,
              }}
            />
            <span className="slider-value">
              {formData.minimumScores.impact}%
            </span>
          </div>

          {/* Urgency Score Slider */}
          <div className="slider-row">
            <span className="slider-label">Urgency score</span>
            <input
              type="range"
              min="0"
              max="100"
              value={formData.minimumScores.urgency}
              onChange={(e) => handleSliderChange("urgency", e.target.value)}
              className="slider-input"
              style={{
                "--value": `${formData.minimumScores.urgency}%`,
              }}
            />
            <span className="slider-value">
              {formData.minimumScores.urgency}%
            </span>
          </div>

          {/* Error */}
          {error && <p className="form-error">{error}</p>}

          {/* Submit */}
          <button type="submit" className="submit-btn" disabled={isSubmitting}>
            {isSubmitting ? "Creating..." : "Create Alert"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateAlertRuleModal;
