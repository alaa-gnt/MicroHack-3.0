import React from "react";
import "./NotificationCard.css";

const NotificationCard = ({ notification, onClick }) => {
  return (
    <div
      className="notification-card"
      onClick={() => onClick && onClick(notification.id)}
      role="button"
      tabIndex={0}
      aria-label={notification.title}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          onClick && onClick(notification.id);
        }
      }}
    >
      <h3 className="notification-card__title">{notification.title}</h3>
      <ul className="notification-card__list">
        {notification.items.map((item, idx) => (
          <li key={idx} className="notification-card__item">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default NotificationCard;
