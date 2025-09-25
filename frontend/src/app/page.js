'use client';

import { useState, useEffect } from 'react';

export default function HomePage() {
  const [url, setUrl] = useState('');
  const [jobId, setJobId] = useState(null);
  const [results, setResults] = useState(null);
  const [status, setStatus] = useState('idle'); 

  const checkJobStatus = async (id) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/results/${id}`);
      const data = await response.json();

      if (data.status === 'finished') {
        setResults(data.data);
        setStatus('success');
      } else if (data.status === 'failed') {
        setStatus('error');
      }
    } catch (error) {
      console.error("Error checking job status:", error);
      setStatus('error');
    }
  };

  useEffect(() => {
    if (status === 'loading' && jobId) {
      const intervalId = setInterval(() => {
        checkJobStatus(jobId);
      }, 3000);
      return () => clearInterval(intervalId);
    }
  }, [status, jobId]);

  const handleAnalyzeClick = async () => {
    setStatus('loading'); 
    setResults(null);
    setJobId(null);

    try {
      const response = await fetch('http://127.0.0.1:8000/start-analysis', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }),
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      
      const result = await response.json();
      setJobId(result.job_id);
    } catch (error) {
      console.error("Failed to start analysis:", error);
      setStatus('error');
    }
  };

  return (
    <main style={{ fontFamily: 'sans-serif', textAlign: 'center', marginTop: '50px' }}>
      <h1>Social Media Analytics Dashboard</h1>
      <p style={{ color: '#555' }}>Paste a YouTube video URL below to analyze its comments.</p>
      <div style={{ marginTop: '30px' }}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter YouTube URL here"
          style={{ padding: '10px', width: '400px', marginRight: '10px' }}
          disabled={status === 'loading'}
        />
        <button
          onClick={handleAnalyzeClick}
          style={{ padding: '10px 15px', cursor: 'pointer' }}
          disabled={status === 'loading'}
        >
          {status === 'loading' ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {status === 'loading' && <p>Analysis in progress... Job ID: {jobId}</p>}
      {status === 'error' && <p style={{ color: 'red' }}>An error occurred during analysis.</p>}

      {status === 'success' && (
        <div style={{ marginTop: '40px', textAlign: 'left', display: 'inline-block' }}>
          <h2>Analysis Complete!</h2>
          <pre style={{ background: '#f0f0f0', padding: '10px', borderRadius: '5px', maxHeight: '400px', overflowY: 'auto' }}>
            {JSON.stringify(results, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}