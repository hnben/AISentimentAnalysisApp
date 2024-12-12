import  { useState } from 'react';
import './summary.css';

const SummaryComponent = () => {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchSummary = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://127.0.0.1:8000/api/v1/summary/');
      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error('Error fetching summary:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="summary-container">
      <button className="fetch-summary-button" onClick={fetchSummary}>
        Get Summary
      </button>
      {loading && <p className="loading">Loading...</p>}
      {summary && <div className="summary-content" dangerouslySetInnerHTML={{ __html: summary }} />}
    </div>
  );
};

export default SummaryComponent;
