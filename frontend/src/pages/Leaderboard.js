import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Leaderboard() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('all');

  useEffect(() => {
    fetchLeaderboard();
  }, [period]);

  const fetchLeaderboard = async () => {
    setLoading(true);
    try {
      const data = await api.getLeaderboard(period);
      setUsers(data);
    } catch (error) {
      console.error('Failed to fetch leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getRankBadge = (rank) => {
    if (rank === 1) return '🥇';
    if (rank === 2) return '🥈';
    if (rank === 3) return '🥉';
    return rank;
  };

  const getBadgeStyle = (badge) => {
    const badges = {
      'Gold': '#FFD700',
      'Silver': '#C0C0C0',
      'Bronze': '#CD7F32',
      'Platinum': '#E5E4E2'
    };
    return badges[badge] || '#888';
  };

  return (
    <div className="leaderboard">
      <h2>Community Leaderboard</h2>
      <div className="period-filter">
        <button 
          className={period === 'week' ? 'active' : ''}
          onClick={() => setPeriod('week')}
        >
          This Week
        </button>
        <button 
          className={period === 'month' ? 'active' : ''}
          onClick={() => setPeriod('month')}
        >
          This Month
        </button>
        <button 
          className={period === 'all' ? 'active' : ''}
          onClick={() => setPeriod('all')}
        >
          All Time
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading leaderboard...</div>
      ) : (
        <div className="leaderboard-list">
          {users.map((user, index) => (
            <div key={user.id} className={`leaderboard-item rank-${index + 1}`}>
              <div className="rank">{getRankBadge(index + 1)}</div>
              <div className="user-info">
                <h3>{user.username}</h3>
                <p className="score">{user.points} points</p>
              </div>
              <div className="stats">
                <span className="reports">📝 {user.total_reports} reports</span>
                <span 
                  className="badge"
                  style={{ backgroundColor: getBadgeStyle(user.current_badge) }}
                >
                  {user.current_badge}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="leaderboard-info">
        <h3>How Points Work</h3>
        <ul>
          <li>✅ Verified report: +10 points</li>
          <li>📸 Photo evidence: +5 bonus points</li>
          <li>🎖️ Consistent reporting: Badge rewards</li>
          <li>🏆 Top contributors: Monthly recognition</li>
        </ul>
      </div>
    </div>
  );
}

export default Leaderboard;
