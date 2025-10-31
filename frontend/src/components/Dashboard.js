/**
 * Dashboard Component
 * Main dashboard after login with role-based UI
 */
import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import apiService from '../services/apiService';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const { user, logout, hasPermission, hasRole } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Fetch system stats if user is admin
    if (hasRole('ADMIN')) {
      loadStats();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const loadStats = async () => {
    try {
      const data = await apiService.getSystemStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const getRoleBadgeClass = (role) => {
    const classes = {
      ADMIN: 'role-badge admin',
      DOCTOR: 'role-badge doctor',
      NURSE: 'role-badge nurse',
      EMERGENCY: 'role-badge emergency',
      PATIENT: 'role-badge patient',
    };
    return classes[role] || 'role-badge';
  };

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-left">
          <h1>🏥 Healthcare Interoperability System</h1>
          <p>HIPAA-Compliant Emergency Medical Data Exchange</p>
        </div>
        <div className="header-right">
          <div className="user-info">
            <div className="user-details">
              <span className="user-name">{user?.full_name}</span>
              <span className={getRoleBadgeClass(user?.role)}>{user?.role}</span>
            </div>
            <button onClick={handleLogout} className="logout-button">
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="welcome-section">
          <h2>Welcome back, {user?.full_name}!</h2>
          <p>You are logged in as <strong>{user?.role}</strong></p>
        </div>

        {/* Quick Actions */}
        <div className="quick-actions">
          <h3>Quick Actions</h3>
          <div className="action-cards">
            {hasPermission('can_view_phi') && (
              <div 
                className="action-card" 
                onClick={() => navigate('/emergency-search')}
              >
                <span className="card-icon">🚨</span>
                <h4>Emergency Search</h4>
                <p>Search patient records across hospitals</p>
              </div>
            )}

            {hasPermission('can_view_phi') && (
              <div 
                className="action-card"
                onClick={() => navigate('/patients')}
              >
                <span className="card-icon">👥</span>
                <h4>Patient List</h4>
                <p>View all registered patients</p>
              </div>
            )}

            {hasRole('ADMIN') && (
              <div 
                className="action-card"
                onClick={() => navigate('/audit-logs')}
              >
                <span className="card-icon">📋</span>
                <h4>Audit Logs</h4>
                <p>View system access logs (HIPAA)</p>
              </div>
            )}

            {hasRole('ADMIN') && (
              <div 
                className="action-card"
                onClick={() => navigate('/security')}
              >
                <span className="card-icon">🔒</span>
                <h4>Security</h4>
                <p>Security events and monitoring</p>
              </div>
            )}

            {hasRole('EMERGENCY') && (
              <div 
                className="action-card emergency-card"
                onClick={() => navigate('/break-glass')}
              >
                <span className="card-icon">⚡</span>
                <h4>Break-Glass Access</h4>
                <p>Emergency override access</p>
              </div>
            )}

            <div 
              className="action-card"
              onClick={() => navigate('/profile')}
            >
              <span className="card-icon">⚙️</span>
              <h4>Profile Settings</h4>
              <p>Manage your account</p>
            </div>
          </div>
        </div>

        {/* Admin Stats */}
        {hasRole('ADMIN') && stats && (
          <div className="stats-section">
            <h3>System Statistics</h3>
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-number">{stats.total_users}</div>
                <div className="stat-label">Total Users</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{stats.active_sessions}</div>
                <div className="stat-label">Active Sessions</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{stats.total_audit_logs}</div>
                <div className="stat-label">Audit Logs</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{stats.failed_login_attempts}</div>
                <div className="stat-label">Failed Logins (24h)</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{stats.security_events_last_24h}</div>
                <div className="stat-label">Security Events (24h)</div>
              </div>
              <div className="stat-card">
                <div className="stat-number">{stats.break_glass_accesses_last_24h}</div>
                <div className="stat-label">Break-Glass Access (24h)</div>
              </div>
            </div>
          </div>
        )}

        {/* Role-based Information */}
        <div className="info-section">
          <h3>Your Permissions</h3>
          <div className="permissions-list">
            {hasPermission('can_view_phi') && <span className="permission-badge">✅ View PHI</span>}
            {hasPermission('can_edit_phi') && <span className="permission-badge">✅ Edit PHI</span>}
            {hasPermission('can_export_data') && <span className="permission-badge">✅ Export Data</span>}
            {hasPermission('break_glass_access') && <span className="permission-badge">✅ Emergency Access</span>}
            {hasRole('ADMIN') && <span className="permission-badge admin">✅ Admin Access</span>}
          </div>
        </div>

        {/* Security Notice */}
        <div className="security-notice">
          <p>🔒 <strong>HIPAA Compliance:</strong> All access to patient health information (PHI) is logged and monitored. 
          Unauthorized access or disclosure may result in civil and criminal penalties.</p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
