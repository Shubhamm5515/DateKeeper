import { useState, useEffect } from 'react';
import { getDocuments, deleteDocument, getDocumentStats } from '../services/api';
import { toast } from 'react-toastify';
import './DocumentList.css';

function DocumentList({ refreshTrigger }) {
  const [documents, setDocuments] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDocuments();
    fetchStats();
  }, [refreshTrigger]);

  const fetchDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
      toast.error('Failed to load documents');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const data = await getDocumentStats();
      setStats(data);
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleDelete = async (documentId, documentName) => {
    if (!window.confirm(`Are you sure you want to delete "${documentName}"?`)) {
      return;
    }

    try {
      await deleteDocument(documentId);
      toast.success('Document deleted successfully');
      fetchDocuments();
      fetchStats();
    } catch (error) {
      console.error('Failed to delete document:', error);
      toast.error('Failed to delete document');
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      valid: { emoji: '🟢', text: 'Valid', class: 'status-valid' },
      expiring_this_month: { emoji: '🟡', text: 'Expiring Soon', class: 'status-warning' },
      expiring_soon: { emoji: '🟠', text: 'Expiring Very Soon', class: 'status-urgent' },
      expired: { emoji: '🔴', text: 'Expired', class: 'status-expired' }
    };
    return badges[status] || badges.valid;
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  const getDaysUntilExpiry = (expiryDate) => {
    const today = new Date();
    const expiry = new Date(expiryDate);
    const diffTime = expiry - today;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
  };

  if (loading) {
    return <div className="loading">Loading documents...</div>;
  }

  return (
    <div className="document-list-container">
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-value">{stats.total}</div>
            <div className="stat-label">Total Documents</div>
          </div>
          <div className="stat-card valid">
            <div className="stat-value">{stats.valid}</div>
            <div className="stat-label">🟢 Valid</div>
          </div>
          <div className="stat-card warning">
            <div className="stat-value">{stats.expiring_soon}</div>
            <div className="stat-label">🟡 Expiring Soon</div>
          </div>
          <div className="stat-card expired">
            <div className="stat-value">{stats.expired}</div>
            <div className="stat-label">🔴 Expired</div>
          </div>
        </div>
      )}

      <div className="document-list">
        <h2>📋 My Documents</h2>
        
        {documents.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">📄</div>
            <p>No documents yet</p>
            <small>Add your first document using the form above</small>
          </div>
        ) : (
          <div className="documents-grid">
            {documents.map((doc) => {
              const statusBadge = getStatusBadge(doc.status);
              const daysUntilExpiry = getDaysUntilExpiry(doc.expiry_date);
              
              return (
                <div key={doc.id} className={`document-card ${statusBadge.class}`}>
                  <div className="document-header">
                    <h3>{doc.document_name}</h3>
                    <span className={`status-badge ${statusBadge.class}`}>
                      {statusBadge.emoji} {statusBadge.text}
                    </span>
                  </div>
                  
                  <div className="document-body">
                    <div className="document-info">
                      <span className="info-label">Type:</span>
                      <span className="info-value">{doc.document_type.replace('_', ' ')}</span>
                    </div>
                    
                    <div className="document-info">
                      <span className="info-label">Expires:</span>
                      <span className="info-value">{formatDate(doc.expiry_date)}</span>
                    </div>
                    
                    <div className="document-info">
                      <span className="info-label">Days Left:</span>
                      <span className={`info-value ${daysUntilExpiry < 0 ? 'expired-text' : ''}`}>
                        {daysUntilExpiry < 0 ? 'Expired' : `${daysUntilExpiry} days`}
                      </span>
                    </div>
                  </div>
                  
                  <div className="document-actions">
                    <button 
                      onClick={() => handleDelete(doc.id, doc.document_name)}
                      className="btn-delete"
                    >
                      🗑️ Delete
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default DocumentList;
