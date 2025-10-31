/**
 * Protected Route Component
 * Redirects to login if user is not authenticated
 */
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const ProtectedRoute = ({ children, requiredRoles = [], requiredPermission = null }) => {
  const { user, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (!user) {
    // Redirect to login, but save the location they were trying to go to
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Check if user has required role
  if (requiredRoles.length > 0 && !requiredRoles.includes(user.role)) {
    return (
      <div style={{ 
        padding: '20px', 
        textAlign: 'center',
        color: '#d32f2f'
      }}>
        <h2>Access Denied</h2>
        <p>You don't have permission to access this page.</p>
        <p>Required roles: {requiredRoles.join(', ')}</p>
      </div>
    );
  }

  // Check if user has required permission
  if (requiredPermission) {
    const { hasPermission } = useAuth();
    if (!hasPermission(requiredPermission)) {
      return (
        <div style={{ 
          padding: '20px', 
          textAlign: 'center',
          color: '#d32f2f'
        }}>
          <h2>Access Denied</h2>
          <p>You don't have the required permission: {requiredPermission}</p>
        </div>
      );
    }
  }

  return children;
};

export default ProtectedRoute;
