import React, { useState, useEffect } from "react";
import { Bell, Zap, SquarePen, Trash2, ShieldCheck, ListFilter } from "lucide-react";
import "./Alerts.css";
import useNotifications from "../../hooks/useNotifications";
import NotificationCard from "../../components/notifications/NotificationCard/NotificationCard";
import CreateAlertRuleModal from "../../components/modals/CreateAlertRuleModal/CreateAlertRuleModal";
import { getAlertRules, deleteAlertRule } from "../../services/alertRulesService";

const Alerts = () => {
  const { grouped, loading: notificationsLoading, error: notificationsError, markAsRead, refetch: refetchNotifications } = useNotifications();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [rules, setRules] = useState([]);
  const [rulesLoading, setRulesLoading] = useState(false);
  const [view, setView] = useState("notifications"); // "notifications" or "rules"

  const fetchRules = async () => {
    setRulesLoading(true);
    try {
      const data = await getAlertRules();
      setRules(data);
    } catch (err) {
      console.error("Failed to fetch rules:", err);
    } finally {
      setRulesLoading(false);
    }
  };

  useEffect(() => {
    if (view === "rules") {
      fetchRules();
    }
  }, [view]);

  const handleCardClick = (id) => {
    markAsRead(id);
  };

  const handleDeleteRule = async (id) => {
    if (window.confirm("Are you sure you want to delete this alert rule?")) {
      await deleteAlertRule(id);
      fetchRules();
    }
  };

  const handleAlertCreated = () => {
    fetchRules();
    setView("rules");
  };

  return (
    <div className="alerts-page">
      {/* ── Page header ── */}
      <div className="alerts-header">
        <div className="alerts-header__left">
          <Bell size={30} strokeWidth={2.2} />
          <h1 className="alerts-header__title">Alerts &amp; Rules</h1>
        </div>
        <div className="alerts-header__actions">
          <div className="view-toggle">
            <button
              className={`toggle-btn ${view === 'notifications' ? 'active' : ''}`}
              onClick={() => setView('notifications')}
            >
              <Zap size={16} />
              <span>Activity</span>
            </button>
            <button
              className={`toggle-btn ${view === 'rules' ? 'active' : ''}`}
              onClick={() => setView('rules')}
            >
              <ListFilter size={16} />
              <span>Rules</span>
            </button>
          </div>
          <button className="alerts-header__btn" onClick={() => setIsModalOpen(true)}>
            <SquarePen size={20} />
            <span>New Rule</span>
          </button>
        </div>
      </div>

      {view === "notifications" ? (
        <>
          <h2 className="alerts-section-title">Recent Notifications</h2>
          {notificationsLoading && <div className="alerts-loading">Loading notifications...</div>}
          {!notificationsLoading && grouped.length === 0 && (
            <div className="alerts-empty">
              <ShieldCheck size={48} color="#10B981" />
              <p>Your system is quiet. No new alerts detected.</p>
            </div>
          )}
          {!notificationsLoading && grouped.map((group, gi) => (
            <div className="notification-group" key={gi}>
              <div className="notification-group__header">
                <Zap size={20} strokeWidth={2.4} />
                <span className="notification-group__time">{group.label}</span>
              </div>
              {group.notifications.map((n) => (
                <NotificationCard key={n.id} notification={n} onClick={handleCardClick} />
              ))}
            </div>
          ))}
        </>
      ) : (
        <>
          <h2 className="alerts-section-title">Active Alert Rules</h2>
          {rulesLoading && <div className="alerts-loading">Loading rules...</div>}
          {!rulesLoading && rules.length === 0 && (
            <div className="alerts-empty">
              <p>No alert rules created yet.</p>
            </div>
          )}
          <div className="rules-grid">
            {rules.map((rule) => (
              <div key={rule.id} className="rule-card">
                <div className="rule-card__info">
                  <h3 className="rule-card__name">{rule.name}</h3>
                  <div className="rule-card__details">
                    <span>Min Impact: {rule.minimum_impact_score}%</span>
                    <span>Min Urgency: {rule.minimum_urgency_score}%</span>
                  </div>
                </div>
                <button
                  className="rule-delete-btn"
                  onClick={() => handleDeleteRule(rule.id)}
                  title="Delete rule"
                >
                  <Trash2 size={18} />
                </button>
              </div>
            ))}
          </div>
        </>
      )}

      <CreateAlertRuleModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSuccess={handleAlertCreated}
      />
    </div>
  );
};

export default Alerts;
