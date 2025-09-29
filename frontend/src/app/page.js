'use client';

import { useState, useEffect } from 'react';
import SentimentChart from '../components/SentimentChart';
import KeywordCloud from '../components/KeywordCloud';
import QuestionsList from '../components/QuestionList';
import styles from './page.module.css';
const processResults = (results)=>{
  if(!results || results.length === 0){
    return {positive:0, negative:0,total:0};
  }
  const positiveCount = results.filter(r=>r.sentiment_label === 'POSITIVE').length;
  const total = results.length;
  const positivePercentage = ((positiveCount / total) * 100).toFixed(1);
  const negativePercentage = (100 - positivePercentage).toFixed(1);
  return{
    positive: positivePercentage,
    negative: negativePercentage,
    total: total
  };
};
export default function HomePage() {
  const [url, setUrl] = useState('');
  const [jobId, setJobId] = useState(null);
  const [results, setResults] = useState(null);
  const [status, setStatus] = useState('idle'); 

  const [activeTab, setActiveTab] = useState('dashboard');

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
  const sentimentStats = processResults(results);
  return (
    <main>
      <h1>Social Media Analytics Dashboard</h1>

      {/* 2. APPLY THE NEW STYLES */}
      <div className={styles.formContainer}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter YouTube URL here"
          className={styles.urlInput}
          disabled={status === 'loading'}
        />
        <button
          onClick={handleAnalyzeClick}
          className={styles.analyzeButton}
          disabled={status === 'loading'}
        >
          {status === 'loading' ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>

      {status === 'loading' && <p>Analysis in progress...</p>}
      {status === 'error' && <p style={{ color: '#F44336' }}>An error occurred.</p>}

      {status === 'success' && (
        <div style={{ marginTop: '40px' }}>
          <h2>Analysis Complete!</h2>
          
          <div className={styles.tabsContainer}>
            <button 
              onClick={() => setActiveTab('dashboard')}
              className={activeTab === 'dashboard' ? styles.tabButtonActive : styles.tabButton}
            >
              Dashboard
            </button>
            <button 
              onClick={() => setActiveTab('questions')}
              className={activeTab === 'questions' ? styles.tabButtonActive : styles.tabButton}
            >
              Questions
            </button>
          </div>

          {activeTab === 'dashboard' && (
            <div>
              <SentimentChart data={results} />
              <hr />
              <KeywordCloud data={results} />
            </div>
          )}

          {activeTab === 'questions' && (
            <div>
              <QuestionsList data={results} />
            </div>
          )}
        </div>
      )}
    </main>
  );
}