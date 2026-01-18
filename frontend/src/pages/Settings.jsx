import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import api from '../services/api';
import './Settings.css';

function Settings() {
  const { user } = useAuth();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  
  // Settings state
  const [alternateEmail, setAlternateEmail] = useState('');
  const [notifyEmail, setNotifyEmail] = useState('Y');
  const [notifySms, setNotifySms] = useState('N');
  const [reminderIntervals, setReminderIntervals] = useState({
    '6_months': true,
    '3_months': true,
    '1_month': true,
    '7_days': true
  });

  useEffect(() => {
    loadSettings();
  }, []);

  const loadSettings = async () => {
    try {
      const response = await api.get('/api/auth/settings');
      const settings = response.data;
      
      setAlternateEmail(settings.alternate_email || '');
      setNotifyEmail(settings.notify_email || 'Y');
      setNotifySms(settings.notify_sms || 'N');
      setReminderIntervals(settings.reminder_intervals || {
        '6_months': true,
        '3_months': true,
        '1_month': true,
        '7_days': true
      });
    } catch (error) {
      console.error('Failed to load settings:', error);
      toast.error('Failed to load settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.put('/api/auth/settings', {
        alternate_email: alternateEmail || null,
        notify_email: notifyEmail,
        notify_sms: notifySms,
        reminder_intervals: reminderIntervals
      });
      
      toast.success('✅ Settings saved successfully!');
    } catch (error) {
      console.error('Failed to save settings:', error);
      toast.error('Failed to save settings: ' + (error.response?.data?.detail || error.message));
    } finally {
      setSaving(false);
    }
  };

  const toggleInterval = (interval) => {
    setReminderIntervals(prev => ({
      ...prev,
      [interval]: !prev[interval]
    }));
  };

  const getIntervalLabel = (interval) => {
    const labels = {
      '6_months': '6 Months Before (180 days)',
      '3_months': '3 Months Before (90 days)',
      '1_month': '1 Month Before (30 days)',
      '7_days': '7 Days Before'
    };
    return labels[interval] || interval;
  };

  const getIntervalEmoji = (interval) => {
    const emojis = {
      '6_months': '📅',
      '3_months': '⏰',
      '1_month': '⚠️',
      '7_days': '🚨'
    };
    return emojis[interval] || '📄';
  };

  if (loading) {
    return (
      <div className="settings-loading">
        <div className="spinner">⏳</div>
        <p>Loading settings...</p>
      </div>
    );
  }

  return (
    <div className="settings-container">
      <div className="settings-header">
        <h1>⚙️ Reminder Settings</h1>
        <p>Customize when and how you receive document expiry reminders</p>
      </div>

      <div className="settings-content">
        {/* Email Settings */}
        <section className="settings-section">
          <div className="section-header">
            <h2>📧 Email Settings</h2>
            <p>Configure where reminders are sent</p>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label>Primary Email</label>
              <p className="setting-description">
                Your login email: <strong>{user?.email}</strong>
              </p>
            </div>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label htmlFor="alternateEmail">Alternate Email (Optional)</label>
              <p className="setting-description">
                Send reminders to a different email address
              </p>
            </div>
            <input
              type="email"
              id="alternateEmail"
              value={alternateEmail}
              onChange={(e) => setAlternateEmail(e.target.value)}
              placeholder="alternate@example.com"
              className="setting-input"
            />
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label>Email Notifications</label>
              <p className="setting-description">
                Receive reminder emails
              </p>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={notifyEmail === 'Y'}
                onChange={(e) => setNotifyEmail(e.target.checked ? 'Y' : 'N')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </section>

        {/* Reminder Intervals */}
        <section className="settings-section">
          <div className="section-header">
            <h2>🔔 Reminder Intervals</h2>
            <p>Choose when to receive reminders before documents expire</p>
          </div>

          <div className="intervals-grid">
            {Object.keys(reminderIntervals).map((interval) => (
              <div
                key={interval}
                className={`interval-card ${reminderIntervals[interval] ? 'active' : 'inactive'}`}
                onClick={() => toggleInterval(interval)}
              >
                <div className="interval-icon">{getIntervalEmoji(interval)}</div>
                <div className="interval-label">{getIntervalLabel(interval)}</div>
                <div className="interval-toggle">
                  <label className="toggle-switch">
                    <input
                      type="checkbox"
                      checked={reminderIntervals[interval]}
                      onChange={() => toggleInterval(interval)}
                      onClick={(e) => e.stopPropagation()}
                    />
                    <span className="toggle-slider"></span>
                  </label>
                </div>
              </div>
            ))}
          </div>

          <div className="intervals-info">
            <p>
              ℹ️ <strong>How it works:</strong> You'll receive reminders at the selected intervals before your documents expire.
              For example, if a document expires on July 17, 2026, and you have "6 Months Before" enabled,
              you'll get a reminder on January 17, 2026.
            </p>
          </div>
        </section>

        {/* SMS Settings */}
        <section className="settings-section">
          <div className="section-header">
            <h2>📱 SMS Settings</h2>
            <p>Configure SMS notifications (optional)</p>
          </div>

          <div className="setting-item">
            <div className="setting-info">
              <label>SMS Notifications</label>
              <p className="setting-description">
                Receive reminder via SMS (requires phone number)
              </p>
            </div>
            <label className="toggle-switch">
              <input
                type="checkbox"
                checked={notifySms === 'Y'}
                onChange={(e) => setNotifySms(e.target.checked ? 'Y' : 'N')}
              />
              <span className="toggle-slider"></span>
            </label>
          </div>
        </section>

        {/* Save Button */}
        <div className="settings-actions">
          <button
            className="btn-save-settings"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? (
              <>
                <span className="spinner">⏳</span>
                Saving...
              </>
            ) : (
              <>
                <span className="icon">💾</span>
                Save Settings
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default Settings;
