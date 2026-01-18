import { useState } from 'react';
import { extractExpiryDate } from '../services/api';
import { toast } from 'react-toastify';
import './DocumentScanner.css';

function DocumentScanner({ onDocumentScanned }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    
    if (!selectedFile) return;
    
    // Validate file type
    if (!selectedFile.type.startsWith('image/')) {
      toast.error('Please select an image file');
      return;
    }
    
    // Validate file size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      toast.error('File size must be less than 10MB');
      return;
    }
    
    setFile(selectedFile);
    
    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(selectedFile);
    
    setResult(null);
  };

  const handleScanDocument = async () => {
    if (!file) return;

    setLoading(true);
    toast.info('🔍 Scanning document...');

    try {
      const data = await extractExpiryDate(file);
      setResult(data);
      
      if (data.success) {
        toast.success('✅ Expiry date extracted successfully!');
        
        // Pass data to parent component
        if (onDocumentScanned) {
          onDocumentScanned({
            expiryDate: data.expiry_date,
            documentType: data.document_type
          });
        }
      } else {
        toast.warning('⚠️ Could not extract expiry date. Please enter manually.');
      }
    } catch (error) {
      console.error('OCR failed:', error);
      
      let errorMessage = 'OCR processing failed. Please try again.';
      
      if (error.response) {
        // Server responded with error
        errorMessage = error.response.data?.detail || error.response.data?.message || errorMessage;
        console.error('Server error:', error.response.status, error.response.data);
      } else if (error.request) {
        // Request made but no response
        errorMessage = 'Cannot connect to server. Make sure backend is running on http://localhost:8000';
        console.error('No response from server');
      } else {
        // Something else happened
        errorMessage = error.message || errorMessage;
      }
      
      toast.error(`❌ ${errorMessage}`);
      setResult({
        success: false,
        message: errorMessage
      });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
  };

  return (
    <div className="document-scanner">
      <h3>📸 Scan Document</h3>
      <p className="scanner-subtitle">Upload your document image to auto-extract expiry date</p>
      
      <div className="upload-section">
        {!preview ? (
          <label className="file-upload-label">
            <input 
              type="file" 
              accept="image/*" 
              onChange={handleFileChange}
              className="file-input"
            />
            <div className="upload-box">
              <div className="upload-icon">📄</div>
              <p className="upload-text">Click to upload or drag and drop</p>
              <p className="upload-hint">PNG, JPG, WEBP (max 10MB)</p>
            </div>
          </label>
        ) : (
          <div className="preview-section">
            <img src={preview} alt="Preview" className="preview-image" />
            <button onClick={handleReset} className="btn-reset">
              🔄 Choose Different Image
            </button>
          </div>
        )}
      </div>

      {file && !result && (
        <button 
          onClick={handleScanDocument} 
          disabled={loading}
          className="btn-scan"
        >
          {loading ? '🔍 Scanning...' : '🔍 Scan & Extract Date'}
        </button>
      )}

      {result && (
        <div className={`result-box ${result.success ? 'success' : 'warning'}`}>
          <p className="result-message">{result.message}</p>
          {result.success && (
            <div className="result-details">
              <p>✅ <strong>Expiry Date:</strong> {result.expiry_date}</p>
              <p>📋 <strong>Document Type:</strong> {result.document_type}</p>
              <p>🎯 <strong>Confidence:</strong> {result.confidence}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default DocumentScanner;
