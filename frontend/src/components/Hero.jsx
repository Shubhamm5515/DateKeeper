import './Hero.css';

function Hero({ onGetStarted }) {
  const handleViewDemo = () => {
    // Scroll to documents section to show demo
    const element = document.getElementById('how-it-works');
    if (element) {
      const offset = 80;
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      
      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
    }
  };

  return (
    <section className="hero">
      <div className="hero-content">
        <div className="hero-badge">
          <span className="badge-icon">✨</span>
          <span>AI-Powered OCR</span>
        </div>
        
        <h1 className="hero-title">
          Never miss a document
          <br />
          <span className="gradient-text">renewal again</span>
        </h1>
        
        <p className="hero-description">
          Smart document management with AI-powered expiry date extraction.
          <strong style={{ color: '#34d399' }}> Your documents are never stored</strong> - we only save expiry dates for reminders.
        </p>
        
        <div className="hero-cta">
          <button className="btn-primary" onClick={onGetStarted}>
            Get Started Free
            <span className="btn-arrow">→</span>
          </button>
          <button className="btn-secondary" onClick={handleViewDemo}>
            View Demo
          </button>
        </div>
        
        <div className="hero-stats">
          <div className="stat">
            <div className="stat-value">25K+</div>
            <div className="stat-label">OCR Requests/Month</div>
          </div>
          <div className="stat">
            <div className="stat-value">95%+</div>
            <div className="stat-label">Accuracy Rate</div>
          </div>
          <div className="stat">
            <div className="stat-value">$0</div>
            <div className="stat-label">Forever Free</div>
          </div>
        </div>
      </div>
      
      <div className="hero-visual">
        <div className="floating-card card-1">
          <div className="card-icon">🛂</div>
          <div className="card-text">Passport</div>
          <div className="card-status valid">Valid</div>
        </div>
        <div className="floating-card card-2">
          <div className="card-icon">🚗</div>
          <div className="card-text">License</div>
          <div className="card-status warning">Expiring Soon</div>
        </div>
        <div className="floating-card card-3">
          <div className="card-icon">🪪</div>
          <div className="card-text">ID Card</div>
          <div className="card-status expired">Expired</div>
        </div>
        <div className="floating-card card-4">
          <div className="card-icon">🏥</div>
          <div className="card-text">Insurance</div>
          <div className="card-status valid">Valid</div>
        </div>
        <div className="floating-card card-5">
          <div className="card-icon">🌿</div>
          <div className="card-text">Pollution</div>
          <div className="card-status warning">Expiring Soon</div>
        </div>
      </div>
    </section>
  );
}

export default Hero;
