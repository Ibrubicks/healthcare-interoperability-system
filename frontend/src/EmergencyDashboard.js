import React, { useState } from 'react';
import axios from 'axios';
import './EmergencyDashboard.css';

const EmergencyDashboard = () => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [dob, setDob] = useState('');
  const [patientData, setPatientData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Convert MM/DD/YYYY to YYYY-MM-DD
  const convertDateFormat = (dateStr) => {
    if (!dateStr) return '';
    
    // Check if format is MM/DD/YYYY
    const mmddyyyyRegex = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/;
    const match = dateStr.match(mmddyyyyRegex);
    
    if (match) {
      const [, month, day, year] = match;
      return `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    }
    
    // If already YYYY-MM-DD, return as is
    return dateStr;
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setPatientData(null);

    try {
      // Convert date format before sending
      const formattedDob = convertDateFormat(dob);
      
      const response = await axios.get('http://localhost:8000/api/emergency-search', {
        params: {
          first_name: firstName,
          last_name: lastName,
          dob: formattedDob,
        },
      });

      setPatientData(response.data);

      // Log access
      axios.post('http://localhost:8000/api/log-access', null, {
        params: {
          user_id: 'EMERGENCY_STAFF',
          patient_id: response.data.patient.patient_id,
          purpose: 'Emergency lookup',
          ip_address: '127.0.0.1',
        },
      });
    } catch (err) {
      setError(err.response?.data?.detail || 'Patient not found');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="red-header">
        <span className="pulse-icon">📡</span>
        <h1>EMERGENCY PATIENT LOOKUP</h1>
        <p>Unified Medical Records – Multiple Hospital Systems</p>
      </header>

      <div className="content-box">
        <div className="quote-section">
          <p className="quote">"Every second counts. Fast, accurate patient data saves lives."</p>
        </div>

        <form className="search-box" onSubmit={handleSearch}>
          <div className="form-row">
            <div className="form-field">
              <label>First Name</label>
              <input
                type="text"
                placeholder="John"
                value={firstName}
                onChange={(e) => setFirstName(e.target.value)}
                required
                autoFocus
              />
            </div>

            <div className="form-field">
              <label>Last Name</label>
              <input
                type="text"
                placeholder="Smith"
                value={lastName}
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>

            <div className="form-field">
              <label>Date of Birth</label>
              <input
                type="text"
                placeholder="MM/DD/YYYY or YYYY-MM-DD"
                value={dob}
                onChange={(e) => setDob(e.target.value)}
                required
              />
            </div>
          </div>

          <button type="submit" className="search-btn" disabled={loading}>
            {loading ? <span className="spinner"></span> : '🔍'} SEARCH
          </button>
        </form>

        {error && (
          <div className="error-box">
            <span>❌</span> {error}
          </div>
        )}

        {patientData && (
          <div className="results">
            <section className="patient-section">
              <h2>👤 Patient Information</h2>
              <div className="info-grid">
                <div>
                  <strong>Patient ID</strong>
                  <p>{patientData.patient.patient_id}</p>
                </div>
                <div>
                  <strong>Name</strong>
                  <p>{patientData.patient.first_name} {patientData.patient.last_name}</p>
                </div>
                <div>
                  <strong>DOB</strong>
                  <p>{patientData.patient.date_of_birth}</p>
                </div>
                <div>
                  <strong>Gender</strong>
                  <p>{patientData.patient.gender}</p>
                </div>
                <div>
                  <strong>Phone</strong>
                  <p>{patientData.patient.phone}</p>
                </div>
                <div>
                  <strong>Emergency Contact</strong>
                  <p>{patientData.patient.emergency_contact}</p>
                </div>
              </div>

              <div className="hospital-count">
                <span className="badge">{patientData.patient.num_hospitals}</span>
                <span>Hospital Records Found</span>
              </div>
            </section>

            {patientData.alerts && patientData.alerts.length > 0 && (
              <section className="alerts-section">
                <h2>⚠️ Critical Alerts</h2>
                {patientData.alerts.map((alert) => (
                  <div key={alert.alert_id} className={`alert alert-${alert.severity.toLowerCase()}`}>
                    <div className="alert-indicator"></div>
                    <div className="alert-content">
                      <span className="alert-type">{alert.type}</span>
                      <p>{alert.description}</p>
                    </div>
                    <span className="severity-tag">{alert.severity}</span>
                  </div>
                ))}
              </section>
            )}

            <section className="hospitals-section">
              <h2>🏥 Hospital Records</h2>
              {patientData.hospital_records.map((record, i) => (
                <div key={i} className="hospital-card">
                  <div className="hospital-title">
                    <h3>{record.hospital}</h3>
                    <span className="mrn-label">{record.mrn}</span>
                    <span className="date-label">{record.last_visit}</span>
                  </div>

                  <div className="hospital-details">
                    <div className="detail-row">
                      <strong>Medications</strong>
                      <code>{record.medications}</code>
                    </div>
                    <div className="detail-row">
                      <strong>Allergies</strong>
                      <code>{record.allergies}</code>
                    </div>
                    <div className="detail-row">
                      <strong>Chronic Conditions</strong>
                      <code>{record.chronic_conditions}</code>
                    </div>
                  </div>
                </div>
              ))}
            </section>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmergencyDashboard;
