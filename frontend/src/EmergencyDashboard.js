import React, { useState } from 'react';
import { useAuth } from './contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import apiService from './services/apiService';
import './EmergencyDashboard.css';

const EmergencyDashboard = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [dob, setDob] = useState('');
    const [patientData, setPatientData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    
    const { user, logout } = useAuth();
    const navigate = useNavigate();

    const handleSearch = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            const response = await apiService.emergencySearch(firstName, lastName, dob || null);
            setPatientData(response);
        } catch (err) {
            setError(err.response?.data?.detail || 'Patient not found');
            setPatientData(null);
        } finally {
            setLoading(false);
        }
    };

    const handleLogout = async () => {
        await logout();
        navigate('/login');
    };

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <div>
                    <h1>🚨 EMERGENCY PATIENT LOOKUP</h1>
                    <p>Unified Medical Records - Multiple Hospital Systems</p>
                </div>
                <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
                    <span style={{ color: 'white' }}>
                        Logged in as: <strong>{user?.full_name}</strong> ({user?.role})
                    </span>
                    <button 
                        onClick={() => navigate('/dashboard')} 
                        style={{
                            padding: '8px 16px',
                            background: 'rgba(255,255,255,0.2)',
                            color: 'white',
                            border: '1px solid white',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        Dashboard
                    </button>
                    <button 
                        onClick={handleLogout}
                        style={{
                            padding: '8px 16px',
                            background: 'rgba(255,255,255,0.2)',
                            color: 'white',
                            border: '1px solid white',
                            borderRadius: '4px',
                            cursor: 'pointer'
                        }}
                    >
                        Logout
                    </button>
                </div>
            </header>

            <div className="search-box">
                <form onSubmit={handleSearch}>
                    <input
                        type="text"
                        placeholder="First Name"
                        value={firstName}
                        onChange={(e) => setFirstName(e.target.value)}
                        required
                    />
                    <input
                        type="text"
                        placeholder="Last Name"
                        value={lastName}
                        onChange={(e) => setLastName(e.target.value)}
                        required
                    />
                    <input
                        type="date"
                        value={dob}
                        onChange={(e) => setDob(e.target.value)}
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Searching...' : 'SEARCH'}
                    </button>
                </form>
            </div>

            {error && <div className="error-box">{error}</div>}

            {patientData && (
                <div className="patient-results">
                    
                    {/* PATIENT INFO CARD */}
                    <div className="card patient-info">
                        <h2>👤 PATIENT INFORMATION</h2>
                        <p><strong>ID:</strong> {patientData.patient.patient_id}</p>
                        <p><strong>Name:</strong> {patientData.patient.first_name} {patientData.patient.last_name}</p>
                        <p><strong>DOB:</strong> {patientData.patient.date_of_birth}</p>
                        <p><strong>Gender:</strong> {patientData.patient.gender}</p>
                        <p><strong>Phone:</strong> {patientData.patient.phone}</p>
                        <p><strong>Emergency Contact:</strong> {patientData.patient.emergency_contact}</p>
                        <p><strong>Records in:</strong> {patientData.patient.num_hospitals} Hospitals</p>
                    </div>

                    {/* CRITICAL ALERTS - HIGHEST PRIORITY */}
                    {patientData.alerts.length > 0 && (
                        <div className="card critical-alerts">
                            <h2>⚠️ CRITICAL ALERTS</h2>
                            {patientData.alerts.map((alert) => (
                                <div key={alert.alert_id} className={`alert alert-${alert.severity.toLowerCase()}`}>
                                    <span className="severity-badge">{alert.severity}</span>
                                    <strong>{alert.type}:</strong> {alert.description}
                                </div>
                            ))}
                        </div>
                    )}

                    {/* HOSPITAL RECORDS */}
                    <div className="card hospital-records">
                        <h2>🏥 HOSPITAL RECORDS</h2>
                        {patientData.hospital_records.map((record, idx) => (
                            <div key={idx} className="hospital-record">
                                <h3>{record.hospital}</h3>
                                <p><strong>MRN:</strong> {record.mrn}</p>
                                <p><strong>Last Visit:</strong> {record.last_visit}</p>
                                
                                {record.medications && (
                                    <div>
                                        <strong>Medications:</strong>
                                        <pre className="json-display">{record.medications}</pre>
                                    </div>
                                )}
                                
                                {record.allergies && (
                                    <div>
                                        <strong>Allergies:</strong>
                                        <pre className="json-display">{record.allergies}</pre>
                                    </div>
                                )}
                                
                                {record.chronic_conditions && (
                                    <div>
                                        <strong>Chronic Conditions:</strong>
                                        <pre className="json-display">{record.chronic_conditions}</pre>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default EmergencyDashboard;
