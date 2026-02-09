import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [violations, setViolations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const data = await api.getProfile();
      setProfile(data.profile);
      setViolations(data.violations);
    } catch (error) {
      console.error('Failed to fetch profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const getBadgeColor = (badge) => {
    const colors = {
      'Bronze': '#CD7F32',
      'Silver': '#C0C0C0',
      'Gold': '#FFD700',
      'Platinum': '#E5E4E2'
    };
    return colors[badge] || '#888';
  };

  if (loading) {
    return <div className="loading">Loading profile...</div>;
  }

  if (!profile) {
    return <div className="error">Failed to load profile</div>;
  }

  return (
    <div className="profile-page">
      <div className="profile-header">
        <div className="profile-avatar">
          <div className="avatar-circle">{profile.username[0].toUpperCase()}</div>
        </div>
        <div className="profile-info">
          <h2>{profile.username}</h2>
          <p className="email">{profile.email}</p>
          <div 
            className="badge"
            style={{ backgroundColor: getBadgeColor(profile.current_badge) }}
          >
            {profile.current_badge} Member
          </div>
        </div>
      </div>

      <div className="profile-stats">
        <div className="stat-card">
          <h3>{profile.points}</h3>
          <p>Total Points</p>
        </div>
        <div className="stat-card">
          <h3>{profile.total_reports}</h3>
          <p>Reports Submitted</p>
        </div>
        <div className="stat-card">
          <h3>{profile.verified_reports}</h3>
          <p>Verified Reports</p>
        </div>
        <div className="stat-card">
          <h3>{profile.accuracy_rate}%</h3>
          <p>Accuracy Rate</p>
        </div>
      </div>

      <div className="profile-violations">
        <h3>Recent Violations Reported</h3>
        {violations.length === 0 ? (
          <p className="no-violations">No violations reported yet</p>
        ) : (
          <div className="violations-list">
            {violations.map((violation) => (
              <div key={violation.id} className="violation-item">
                <div className="violation-header">
                  <span className="violation-type">{violation.violation_type}</span>
                  <span className={`status ${violation.status}`}>
                    {violation.is_verified ? '✅ Verified' : '⏳ Pending'}
                  </span>
                </div>
                <div className="violation-details">
                  <p><strong>Vehicle:</strong> {violation.vehicle_number}</p>
                  <p><strong>Location:</strong> {violation.location}</p>
                  <p><strong>Date:</strong> {new Date(violation.timestamp).toLocaleDateString()}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="profile-achievements">
        <h3>Achievements</h3>
        <div className="achievements-grid">
          {profile.total_reports >= 10 && (
            <div className="achievement">
              <span className="icon">🏆</span>
              <p>First 10 Reports</p>
            </div>
          )}
          {profile.verified_reports >= 5 && (
            <div className="achievement">
              <span className="icon">⭐</span>
              <p>5 Verified Reports</p>
            </div>
          )}
          {profile.accuracy_rate >= 80 && (
            <div className="achievement">
              <span className="icon">🎯</span>
              <p>High Accuracy</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Profile;
