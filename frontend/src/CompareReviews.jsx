import { useState, useEffect } from 'react';

const CompareReviews = () => {
  const [modelReviews, setModelReviews] = useState([]);
  const [actualReviews, setActualReviews] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    // Fetch model's review data
    const fetchModelData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/data/');
        if (!response.ok) {
          throw new Error('Failed to fetch model reviews');
        }
        const data = await response.json();
        setModelReviews(data);
      } catch (err) {
        setError('Error fetching model reviews');
      }
    };

    // Fetch actual reviews data
    const fetchActualData = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/v1/actual/');
        if (!response.ok) {
          throw new Error('Failed to fetch actual reviews');
        }
        const data = await response.json();
        setActualReviews(data);
      } catch (err) {
        setError('Error fetching actual reviews');
      }
    };

    fetchModelData();
    fetchActualData();
  }, []);

  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div className="comparison-container">
      {modelReviews.length > 0 && actualReviews.length > 0 ? (
        modelReviews.map((modelReview, index) => (
          <div className="review-comparison" key={index}>
            <div className="review">
              <h3>Model's Review</h3>
              <p><strong>{modelReview.name}</strong></p>
              <p>{modelReview.message}</p>
              <div>
                <h4>Analysis Scores:</h4>
                <ul>
                  {Object.keys(modelReview.analysis).map((category) => (
                    <li key={category}>
                      <strong>{category}:</strong> {modelReview.analysis[category][0].label} ({modelReview.analysis[category][0].score.toFixed(2)})
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="review">
              <h3>Actual Review</h3>
              <p><strong>{actualReviews[index]?.name}</strong></p>
              <p>{actualReviews[index]?.message}</p>
            </div>
          </div>
        ))
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default CompareReviews;
