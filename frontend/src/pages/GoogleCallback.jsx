import { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';

function GoogleCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { setToken, setUser, updateUser } = useAuth();

  useEffect(() => {
    const token = searchParams.get('token');
    const userEmail = searchParams.get('user');
    const error = searchParams.get('error');

    if (error) {
      toast.error('Google authentication failed');
      navigate('/login');
      return;
    }

    if (token && userEmail) {
      // Save token and user info
      localStorage.setItem('token', token);
      
      // Fetch full user profile
      fetch('http://localhost:8000/api/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
        .then(res => res.json())
        .then(userData => {
          localStorage.setItem('user', JSON.stringify(userData));
          updateUser(userData);
          toast.success(`Welcome, ${userData.full_name || userData.email}!`);
          navigate('/dashboard');
        })
        .catch(error => {
          console.error('Failed to fetch user profile:', error);
          toast.error('Failed to complete login');
          navigate('/login');
        });
    } else {
      toast.error('Invalid authentication response');
      navigate('/login');
    }
  }, [searchParams, navigate, updateUser]);

  return (
    <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '100vh',
      background: '#0f172a',
      color: '#fff',
      flexDirection: 'column',
      gap: '20px'
    }}>
      <div style={{ fontSize: '48px' }}>🔄</div>
      <div>Completing Google Sign-In...</div>
    </div>
  );
}

export default GoogleCallback;
