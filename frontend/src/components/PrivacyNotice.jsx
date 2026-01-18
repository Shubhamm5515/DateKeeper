import './PrivacyNotice.css';

function PrivacyNotice() {
  return (
    <div className="privacy-notice">
      <div className="privacy-icon">🔒</div>
      <div className="privacy-content">
        <h4>Your Privacy is Protected</h4>
        <ul>
          <li>✓ Document images are <strong>never stored</strong> on our servers</li>
          <li>✓ Images are <strong>deleted immediately</strong> after OCR processing</li>
          <li>✓ Only expiry date and document type are saved</li>
          <li>✓ No personal information is retained</li>
        </ul>
      </div>
    </div>
  );
}

export default PrivacyNotice;
