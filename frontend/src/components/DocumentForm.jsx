import { useState } from 'react';
import { createDocument } from '../services/api';
import { toast } from 'react-toastify';
import { useAuth } from '../context/AuthContext';
import DocumentScanner from './DocumentScanner';
import PrivacyNotice from './PrivacyNotice';
import './DocumentForm.css';

function DocumentForm({ onDocumentAdded }) {
  const { user } = useAuth();
  const [formData, setFormData] = useState({
    document_name: '',
    document_type: '',
    expiry_date: ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleDocumentScanned = (scannedData) => {
    setFormData({
      ...formData,
      expiry_date: scannedData.expiryDate,
      document_type: scannedData.documentType
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.document_name || !formData.document_type || !formData.expiry_date) {
      toast.error('Please fill in all fields');
      return;
    }

    setLoading(true);

    try {
      const document = await createDocument(formData);
      toast.success('✅ Document added successfully!');
      
      // Reset form
      setFormData({
        document_name: '',
        document_type: '',
        expiry_date: ''
      });
      
      // Notify parent component
      if (onDocumentAdded) {
        onDocumentAdded(document);
      }
    } catch (error) {
      console.error('Failed to add document:', error);
      toast.error('❌ Failed to add document. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="document-form-container">
      <PrivacyNotice />
      <DocumentScanner onDocumentScanned={handleDocumentScanned} />
      
      <form onSubmit={handleSubmit} className="document-form">
        <h3>📝 Document Details</h3>
        
        <div className="form-group">
          <label htmlFor="document_name">Document Name *</label>
          <input 
            type="text"
            id="document_name"
            name="document_name"
            value={formData.document_name}
            onChange={handleChange}
            placeholder="e.g., My Passport"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="document_type">Document Type *</label>
          <select 
            id="document_type"
            name="document_type"
            value={formData.document_type}
            onChange={handleChange}
            required
          >
            <option value="">Select Type</option>
            <option value="passport">🛂 Passport</option>
            <option value="driving_license">🚗 Driving License</option>
            <option value="national_id">🪪 National ID</option>
            <option value="vehicle_insurance">🏥 Vehicle Insurance</option>
            <option value="pollution_certificate">🌿 Pollution Certificate</option>
            <option value="health_insurance">💊 Health Insurance</option>
            <option value="visa">✈️ Visa</option>
            <option value="other">📄 Other</option>
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="expiry_date">Expiry Date *</label>
          <input 
            type="date"
            id="expiry_date"
            name="expiry_date"
            value={formData.expiry_date}
            onChange={handleChange}
            required
          />
          <small>Auto-filled from scan or enter manually</small>
        </div>

        <button type="submit" className="btn-submit" disabled={loading}>
          {loading ? '💾 Saving...' : '💾 Save Document'}
        </button>
      </form>
    </div>
  );
}

export default DocumentForm;
