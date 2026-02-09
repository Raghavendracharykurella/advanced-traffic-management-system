import React, { useState } from 'react';
import api from '../services/api';

function ReportViolation() {
  const [formData, setFormData] = useState({
    violation_type: '',
    vehicle_number: '',
    location: '',
    description: '',
    evidence_photo: null,
  });
  const [preview, setPreview] = useState(null);
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setFormData({ ...formData, evidence_photo: file });
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = new FormData();
      Object.keys(formData).forEach(key => {
        if (formData[key]) data.append(key, formData[key]);
      });
      await api.reportViolation(data);
      setSubmitted(true);
      setFormData({
        violation_type: '',
        vehicle_number: '',
        location: '',
        description: '',
        evidence_photo: null,
      });
      setPreview(null);
    } catch (error) {
      console.error('Failed to submit report:', error);
      alert('Failed to submit report. Please try again.');
    }
  };

  return (
    <div className="report-violation">
      <h2>Report a Violation</h2>
      {submitted && (
        <div className="success-message">
          Report submitted successfully! Thank you for helping keep our roads safe.
        </div>
      )}
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Violation Type:</label>
          <select name="violation_type" value={formData.violation_type} onChange={handleChange} required>
            <option value="">Select type</option>
            <option value="speeding">Speeding</option>
            <option value="red_light">Red Light Violation</option>
            <option value="wrong_lane">Wrong Lane</option>
            <option value="no_helmet">No Helmet</option>
            <option value="drunk_driving">Drunk Driving</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div className="form-group">
          <label>Vehicle Number:</label>
          <input
            type="text"
            name="vehicle_number"
            value={formData.vehicle_number}
            onChange={handleChange}
            placeholder="e.g., KA-01-AB-1234"
            required
          />
        </div>
        <div className="form-group">
          <label>Location:</label>
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={handleChange}
            placeholder="e.g., MG Road Junction"
            required
          />
        </div>
        <div className="form-group">
          <label>Description:</label>
          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Provide additional details..."
            rows="4"
          />
        </div>
        <div className="form-group">
          <label>Evidence Photo:</label>
          <input type="file" accept="image/*" onChange={handleFileChange} />
          {preview && <img src={preview} alt="Preview" className="photo-preview" />}
        </div>
        <button type="submit" className="submit-btn">Submit Report</button>
      </form>
    </div>
  );
}

export default ReportViolation;
