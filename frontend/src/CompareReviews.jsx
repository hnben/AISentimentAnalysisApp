import { useState, useEffect } from 'react';
import './review.css'

const CompareReviews = () => {
  const [modelData, setModelData] = useState(null);
  const [actualData, setActualData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch the model data and actual data
    const fetchData = async () => {
      const modelResponse = await fetch('http://127.0.0.1:8000/api/v1/data/');
      const actualResponse = await fetch('http://127.0.0.1:8000/api/v1/actual/');

      const modelData = await modelResponse.json();
      const actualData = await actualResponse.json();

      setModelData(modelData);
      setActualData(actualData);
      setLoading(false);
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  // Function to get the label class based on the analysis
  const getLabelClass = (label) => {
    switch (label) {
      case 'Positive':
        return 'positive';
      case 'Neutral':
        return 'neutral';
      case 'Negative':
        return 'negative';
      default:
        return '';
    }
  };

  return (
    <div>
      <h1>Compare Reviews</h1>
      <div className="reviews-container">
        {modelData && actualData && modelData.map((item, index) => (
          <div key={index} className="reviews-column">
            <div className="review-card">
              <h3>{item.name}</h3>
              <p>{item.message}</p>

              {/* Analysis side by side */}
              <div className="analysis-container">
                <div className="analysis-box">
                  <h4>Model Analysis</h4>
                  {item.analysis && Object.keys(item.analysis).map((category, i) => (
                    <div key={i}>
                      <strong>{category}:</strong>
                      <p className={getLabelClass(item.analysis[category][0].label)}>
                        {item.analysis[category][0].label}
                      </p>
                    </div>
                  ))}
                </div>

                <div className="analysis-box">
                  <h4>Actual Analysis</h4>
                  {actualData[index] && actualData[index].analysis && Object.keys(actualData[index].analysis).map((category, i) => (
                    <div key={i}>
                      <strong>{category}:</strong>
                      <p className={getLabelClass(actualData[index].analysis[category][0].label)}>
                        {actualData[index].analysis[category][0].label}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CompareReviews;
