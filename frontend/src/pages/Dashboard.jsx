import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import DocumentForm from '../components/DocumentForm';
import DocumentList from '../components/DocumentList';
import api from '../services/api';
import './Dashboard.css';

function Dashboard() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [testingReminders, setTestingReminders] = useState(false);
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleDocumentAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  const handleTestReminders = async () => {
    setTestingReminders(true);
    try {
      const response = await api.post('/api/scheduler/run-now');
      toast.success('✅ Reminder check completed! Check your email inbox and server logs.');
      console.log('Scheduler response:', response.data);
    } catch (error) {
      console.error('Test reminders error:', error);
      toast.error('Failed to test reminders: ' + (error.response?.data?.detail || error.message));
    } finally {
      setTestingReminders(false);
    }
  };

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-content">
          <div className="logo">
            <span className="logo-icon">📄</span>
            <span className="logo-text">DateKeeper</span>
          </div>
          <div className="nav-right">
            <button className="btn-settings" onClick={() => navigate('/settings')}>
              <span className="icon">⚙️</span>
              <span className="text">Settings</span>
            </button>
            <div className="user-info">
              <span className="user-icon">👤</span>
              <span className="user-name">{user?.full_name || user?.email}</span>
            </div>
            <button className="btn-logout" onClick={logout}>
              Logout
            </button>
          </div>
        </div>
      </nav>

      <main className="dashboard-main">
        <section className="welcome-section">
          <div className="welcome-header">
            <div>
              <h1>Welcome back, {user?.full_name || 'User'}! 👋</h1>
              <p className="welcome-subtitle">
                📧 Reminders will be sent to: <strong>{user?.email}</strong>
              </p>
            </div>
            <button 
              className="btn-test-reminders" 
              onClick={handleTestReminders}
              disabled={testingReminders}
            >
              {testingReminders ? (
                <>
                  <span className="spinner">⏳</span>
                  Testing...
                </>
              ) : (
                <>
                  <span className="icon">🔔</span>
                  Test Reminders
                </>
              )}
            </button>
          </div>
        </section>

        <section className="add-document-section">
          <div className="section-header">
            <h2>Add Your Document</h2>
            <p>Upload and scan your documents with AI-powered OCR</p>
          </div>
          <DocumentForm onDocumentAdded={handleDocumentAdded} />
        </section>

        <section className="documents-section">
          <DocumentList refreshTrigger={refreshTrigger} />
        </section>
      </main>
    </div>
  );
}

export default Dashboard;
