import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { toast } from 'react-toastify';
import api from '../services/api';
import './Pricing.css';

function Pricing() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(null);

  const plans = [
    {
      name: "Free",
      price: 0,
      period: "forever",
      features: [
        "10 documents",
        "Email reminders",
        "Basic OCR",
        "Mobile responsive",
        "Privacy-first storage"
      ],
      cta: user?.subscription_tier === "free" ? "Current Plan" : "Downgrade",
      planId: null,
      popular: false,
      disabled: user?.subscription_tier === "free"
    },
    {
      name: "Pro",
      price: 999,
      period: "month",
      features: [
        "Unlimited documents",
        "SMS notifications",
        "Priority OCR",
        "Export data",
        "Priority support",
        "Custom reminder intervals"
      ],
      cta: user?.subscription_tier === "pro" ? "Current Plan" : "Upgrade to Pro",
      planId: import.meta.env.VITE_RAZORPAY_PLAN_PRO,
      popular: true,
      disabled: user?.subscription_tier === "pro"
    },
    {
      name: "Business",
      price: 2999,
      period: "month",
      features: [
        "Everything in Pro",
        "Team collaboration (10 users)",
        "API access",
        "SSO",
        "Advanced analytics",
        "Bulk upload"
      ],
      cta: user?.subscription_tier === "business" ? "Current Plan" : "Upgrade to Business",
      planId: import.meta.env.VITE_RAZORPAY_PLAN_BUSINESS,
      popular: false,
      disabled: user?.subscription_tier === "business"
    },
    {
      name: "Enterprise",
      price: "Custom",
      period: "",
      features: [
        "Everything in Business",
        "Unlimited users",
        "White-label",
        "24/7 support",
        "Custom integrations",
        "Dedicated account manager"
      ],
      cta: "Contact Sales",
      planId: null,
      popular: false,
      disabled: false
    }
  ];

  const handleUpgrade = async (plan) => {
    if (!user) {
      navigate('/login');
      return;
    }

    if (plan.name === "Enterprise") {
      window.location.href = "mailto:sales@datekeeper.com?subject=Enterprise Plan Inquiry";
      return;
    }

    if (!plan.planId || plan.disabled) return;

    setLoading(plan.name);
    
    try {
      // Create subscription
      const response = await api.post('/api/razorpay/create-subscription', {
        plan_id: plan.planId
      });

      const { subscription_id } = response.data;

      // Open Razorpay checkout
      const options = {
        key: import.meta.env.VITE_RAZORPAY_KEY_ID,
        subscription_id: subscription_id,
        name: 'DateKeeper',
        description: `${plan.name} Plan Subscription`,
        image: '/logo.png',
        handler: async function (response) {
          // Verify payment
          try {
            const verifyResponse = await api.post('/api/razorpay/verify-payment', {
              razorpay_payment_id: response.razorpay_payment_id,
              razorpay_subscription_id: response.razorpay_subscription_id,
              razorpay_signature: response.razorpay_signature
            });

            toast.success('🎉 Subscription activated successfully!');
            
            // Update user context
            if (verifyResponse.data.user) {
              updateUser(verifyResponse.data.user);
            }
            
            // Redirect to dashboard
            navigate('/dashboard');
          } catch (error) {
            console.error('Verification error:', error);
            toast.error('Payment verification failed. Please contact support.');
          }
        },
        prefill: {
          name: user.full_name || '',
          email: user.email,
          contact: user.phone || ''
        },
        theme: {
          color: '#667eea'
        },
        modal: {
          ondismiss: function() {
            setLoading(null);
            toast.info('Payment cancelled');
          }
        }
      };

      const razorpay = new window.Razorpay(options);
      razorpay.open();
    } catch (error) {
      console.error('Subscription error:', error);
      toast.error('Failed to create subscription. Please try again.');
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="pricing-page">
      <div className="pricing-header">
        <h1>Choose Your Plan</h1>
        <p>Start free, upgrade when you need more</p>
        {user && (
          <div className="current-plan-badge">
            Current Plan: <strong>{user.subscription_tier || 'free'}</strong>
          </div>
        )}
      </div>

      <div className="pricing-grid">
        {plans.map((plan) => (
          <div 
            key={plan.name} 
            className={`pricing-card ${plan.popular ? 'popular' : ''} ${plan.disabled ? 'disabled' : ''}`}
          >
            {plan.popular && <div className="popular-badge">Most Popular</div>}
            
            <h3>{plan.name}</h3>
            <div className="price">
              {typeof plan.price === 'number' ? (
                <>
                  <span className="currency">₹</span>
                  <span className="amount">{plan.price}</span>
                  {plan.period && <span className="period">/{plan.period}</span>}
                </>
              ) : (
                <span className="amount">{plan.price}</span>
              )}
            </div>

            <ul className="features">
              {plan.features.map((feature, index) => (
                <li key={index}>
                  <span className="check">✓</span>
                  {feature}
                </li>
              ))}
            </ul>

            <button
              className={`btn-upgrade ${plan.popular ? 'primary' : 'secondary'}`}
              onClick={() => handleUpgrade(plan)}
              disabled={loading === plan.name || plan.disabled}
            >
              {loading === plan.name ? 'Loading...' : plan.cta}
            </button>
          </div>
        ))}
      </div>

      <div className="payment-methods">
        <p>We accept:</p>
        <div className="methods">
          <span>💳 Cards</span>
          <span>📱 UPI</span>
          <span>🏦 Net Banking</span>
          <span>👛 Wallets</span>
        </div>
      </div>

      <div className="pricing-footer">
        <button className="btn-back" onClick={() => navigate(user ? '/dashboard' : '/')}>
          ← Back to {user ? 'Dashboard' : 'Home'}
        </button>
      </div>
    </div>
  );
}

export default Pricing;
