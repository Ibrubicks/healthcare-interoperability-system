/**
 * API Service
 * Handles all patient data and healthcare-related API calls
 */
import { apiClient } from './authService';

const apiService = {
  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/api/health');
    return response.data;
  },

  // Emergency patient search
  emergencySearch: async (firstName, lastName, dob = null) => {
    const params = {
      first_name: firstName,
      last_name: lastName,
    };
    if (dob) {
      params.dob = dob;
    }
    const response = await apiClient.get('/api/emergency-search', { params });
    return response.data;
  },

  // Get all patients
  getAllPatients: async () => {
    const response = await apiClient.get('/api/patients');
    return response.data;
  },

  // Get matching scores
  getMatchingScores: async (patientId) => {
    const response = await apiClient.get('/api/matching-scores', {
      params: { patient_id: patientId },
    });
    return response.data;
  },

  // Get drug interactions
  getDrugInteractions: async () => {
    const response = await apiClient.get('/api/drug-interactions');
    return response.data;
  },

  // Log access (for HIPAA compliance)
  logAccess: async (userId, patientId, purpose, ipAddress) => {
    const response = await apiClient.post('/api/log-access', {
      user_id: userId,
      patient_id: patientId,
      purpose,
      ip_address: ipAddress,
    });
    return response.data;
  },

  // Get audit logs
  getAuditLogs: async (params = {}) => {
    const response = await apiClient.get('/api/audit-logs', { params });
    return response.data;
  },

  // Get patient audit logs
  getPatientAuditLogs: async (patientId) => {
    const response = await apiClient.get(`/api/audit-logs/patient/${patientId}`);
    return response.data;
  },

  // Break-glass emergency access
  breakGlassAccess: async (patientId, justification, emergencyType) => {
    const response = await apiClient.post('/api/emergency-access', {
      patient_id: patientId,
      justification,
      emergency_type: emergencyType,
    });
    return response.data;
  },

  // Get active sessions
  getActiveSessions: async () => {
    const response = await apiClient.get('/api/sessions');
    return response.data;
  },

  // Revoke session
  revokeSession: async (sessionId) => {
    const response = await apiClient.delete(`/api/sessions/${sessionId}`);
    return response.data;
  },

  // Get system stats (admin only)
  getSystemStats: async () => {
    const response = await apiClient.get('/api/stats');
    return response.data;
  },

  // Get security events (admin only)
  getSecurityEvents: async (limit = 100) => {
    const response = await apiClient.get('/api/security-events', {
      params: { limit },
    });
    return response.data;
  },
};

export default apiService;
