/**
 * Authentication Context
 * Provides authentication state and methods throughout the app
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import authService from '../services/authService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Check if user is already logged in on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        if (authService.isAuthenticated()) {
          const storedUser = authService.getStoredUser();
          if (storedUser) {
            setUser(storedUser);
          } else {
            // Fetch user info if token exists but user data doesn't
            const userData = await authService.getCurrentUser();
            setUser(userData);
          }
        }
      } catch (err) {
        console.error('Auth initialization error:', err);
        // Clear invalid auth data
        await authService.logout();
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const login = async (username, password) => {
    try {
      setError(null);
      setLoading(true);
      const userData = await authService.login(username, password);
      setUser(userData);
      return userData;
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Login failed. Please check your credentials.';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    try {
      setLoading(true);
      await authService.logout();
      setUser(null);
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateUser = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
      return userData;
    } catch (err) {
      console.error('Update user error:', err);
      throw err;
    }
  };

  const hasPermission = (permission) => {
    if (!user) return false;
    
    // Admin has all permissions
    if (user.role === 'ADMIN') return true;

    // Define permissions based on roles
    const rolePermissions = {
      DOCTOR: ['can_view_phi', 'can_edit_phi', 'can_export_data'],
      NURSE: ['can_view_phi', 'can_edit_phi'],
      EMERGENCY: ['can_view_phi', 'can_edit_phi', 'break_glass_access'],
      PATIENT: ['can_view_phi', 'can_export_data'],
    };

    return rolePermissions[user.role]?.includes(permission) || false;
  };

  const hasRole = (...roles) => {
    if (!user) return false;
    return roles.includes(user.role);
  };

  const value = {
    user,
    loading,
    error,
    login,
    logout,
    updateUser,
    hasPermission,
    hasRole,
    isAuthenticated: !!user,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext;
