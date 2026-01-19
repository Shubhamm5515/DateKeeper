import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { GoogleLogin } from '@react-oauth/google';
import { toast } from 'react-toastify';
import api from '../services/api';
import './Auth.css';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login, setToken, updateUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!email || !password) {
      return;
    }

    setLoading(true);
    toast.info('Signing in... This may take 30-60 seconds on first request.', {
      autoClose: 5000
    });
    try {
      await login(email, password);
    } catch (error) {
      console.error('Login error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleSuccess = async (credentialResponse) => {
    try {
      setLoading(true);
      toast.info('Signing in with Google... This may take 30-60 seconds on first request.', {
        autoClose: 5000
      });
      
      // Send Google token to backend
      const response = await api.post('/api/auth/google/login', {
        token: credentialResponse.credential
      });
      
      const { access_token, user } = response.data;
      
      // Save token and user
      localStorage.setItem('token', access_token);
      localStorage.setItem('user', JSON.stringify(user));
      setToken(access_token);
      updateUser(user);
      
      toast.success(`Welcome back, ${user.full_name || user.email}!`);
      navigate('/dashboard');
    } catch (error) {
      console.error('Google login error:', error);
      toast.error(error.response?.data?.detail || 'Google login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleError = () => {
    toast.error('Google login was cancelled or failed');
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <div className="auth-header">
          <div className="auth-logo">
            <span className="logo-icon">📄</span>
            <span className="logo-text">DateKeeper</span>
          </div>
          <h1>Welcome Back</h1>
          <p>Sign in to manage your documents</p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="your-email@example.com"
              required
              autoFocus
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
          </div>

          <button type="submit" className="btn-auth" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign In'}
          </button>

          <div className="divider">
            <span>OR</span>
          </div>

          <div className="google-login-wrapper">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleError}
              useOneTap={false}
              theme="filled_black"
              size="large"
              text="continue_with"
              shape="rectangular"
              width="100%"
            />
          </div>
        </form>

        <div className="auth-footer">
          <p>
            Don't have an account?{' '}
            <Link to="/register" className="auth-link">
              Sign up
            </Link>
          </p>
        </div>

        <div className="auth-features">
          <div className="feature-item">
            <span className="feature-icon">🔒</span>
            <span>Privacy First</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">📧</span>
            <span>Email Reminders</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">🤖</span>
            <span>AI-Powered OCR</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
