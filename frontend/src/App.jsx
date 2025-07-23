import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [moodifyResult, setMoodifyResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [moodifyLoading, setMoodifyLoading] = useState(false)
  const [error, setError] = useState(null)

  const analyzeText = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze')
      return
    }

    setLoading(true)
    setError(null)
    setMoodifyResult(null) // Clear previous moodify results

    try {
      const response = await fetch('http://localhost:8000/api/analyze-sentiment/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text.trim() })
      })

      const data = await response.json()

      if (response.ok) {
        setAnalysis(data)
      } else {
        setError(data.error || 'Failed to analyze text')
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const moodifyText = async (targetSentiment) => {
    setMoodifyLoading(true)
    setError(null)

    try {
      const response = await fetch('http://localhost:8000/api/moodify-text/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          text: text.trim(),
          target_sentiment: targetSentiment
        })
      })

      const data = await response.json()

      if (response.ok) {
        setMoodifyResult(data)
      } else {
        setError(data.error || 'Failed to moodify text')
      }
    } catch (err) {
      setError('Failed to connect to the server. Make sure the backend is running.')
    } finally {
      setMoodifyLoading(false)
    }
  }

  const useMoodifiedText = () => {
    if (moodifyResult && moodifyResult.modified_text) {
      setText(moodifyResult.modified_text)
      setMoodifyResult(null)
      setAnalysis(null)
    }
  }

  const clearAnalysis = () => {
    setText('')
    setAnalysis(null)
    setMoodifyResult(null)
    setError(null)
  }

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '#4CAF50'
      case 'negative': return '#f44336'
      case 'neutral': return '#FF9800'
      default: return '#2196F3'
    }
  }

  const getSentimentEmoji = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case 'positive': return '😊'
      case 'negative': return '😞'
      case 'neutral': return '😐'
      default: return '🤔'
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🧠 Moodify - Text Sentiment Analyzer</h1>
        <p>Analyze the emotional tone of your text using AI</p>
      </header>

      <main className="app-main">
        <div className="input-section">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter your text here to analyze its sentiment... 

Examples:
• I love this beautiful sunny day!
• I'm feeling really frustrated with this situation.
• The weather is okay today, nothing special."
            rows={6}
            className="text-input"
            maxLength={1000}
          />
          
          <div className="char-count">
            {text.length}/1000 characters
          </div>

          <div className="button-group">
            <button 
              onClick={analyzeText} 
              disabled={loading || !text.trim()}
              className="analyze-btn"
            >
              {loading ? 'Analyzing...' : 'Analyze Sentiment'}
            </button>
            
            {(analysis || error) && (
              <button onClick={clearAnalysis} className="clear-btn">
                Clear
              </button>
            )}
          </div>
        </div>

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {analysis && (
          <div className="results-section">
            <h2>Analysis Results</h2>
            
            <div className="sentiment-card">
              <div className="sentiment-header">
                <span 
                  className="sentiment-emoji"
                  style={{ color: getSentimentColor(analysis.sentiment) }}
                >
                  {getSentimentEmoji(analysis.sentiment)}
                </span>
                <span 
                  className="sentiment-label"
                  style={{ color: getSentimentColor(analysis.sentiment) }}
                >
                  {analysis.sentiment || 'Unknown'}
                </span>
              </div>

              {analysis.confidence && (
                <div className="confidence-section">
                  <div className="confidence-label">Confidence</div>
                  <div className="confidence-bar">
                    <div 
                      className="confidence-fill"
                      style={{ 
                        width: `${analysis.confidence * 100}%`,
                        backgroundColor: getSentimentColor(analysis.sentiment)
                      }}
                    ></div>
                  </div>
                  <div className="confidence-value">
                    {(analysis.confidence * 100).toFixed(1)}%
                  </div>
                </div>
              )}

              {analysis.scores && (
                <div className="scores-section">
                  <h3>Detailed Scores</h3>
                  <div className="scores-grid">
                    {Object.entries(analysis.scores).map(([sentiment, score]) => (
                      <div key={sentiment} className="score-item">
                        <span className="score-label">{sentiment}</span>
                        <span className="score-value">{(score * 100).toFixed(1)}%</span>
                        <div className="score-bar">
                          <div 
                            className="score-fill"
                            style={{ 
                              width: `${score * 100}%`,
                              backgroundColor: getSentimentColor(sentiment)
                            }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="analyzed-text">
              <h3>Analyzed Text</h3>
              <p>"{text}"</p>
            </div>

            {/* Moodify Section */}
            <div className="moodify-section">
              <h3>🎭 Moodify Your Text</h3>
              <p>Transform your text to express a different sentiment:</p>
              
              <div className="moodify-buttons">
                <button 
                  onClick={() => moodifyText('positive')}
                  disabled={moodifyLoading || analysis.sentiment === 'positive'}
                  className="moodify-btn positive"
                >
                  {moodifyLoading ? '✨ Transforming...' : '😊 Make Positive'}
                </button>
                
                <button 
                  onClick={() => moodifyText('negative')}
                  disabled={moodifyLoading || analysis.sentiment === 'negative'}
                  className="moodify-btn negative"
                >
                  {moodifyLoading ? '✨ Transforming...' : '😞 Make Negative'}
                </button>
                
                <button 
                  onClick={() => moodifyText('neutral')}
                  disabled={moodifyLoading || analysis.sentiment === 'neutral'}
                  className="moodify-btn neutral"
                >
                  {moodifyLoading ? '✨ Transforming...' : '😐 Make Neutral'}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Moodify Results */}
        {moodifyResult && (
          <div className="moodify-results">
            <h2>🎭 Moodify Results</h2>
            
            <div className="transformation-card">
              <div className="transformation-header">
                <span className="transformation-title">
                  {moodifyResult.success ? '✅ Success!' : '⚠️ Partial Success'}
                </span>
                <span className="transformation-message">
                  {moodifyResult.message}
                </span>
              </div>

              <div className="text-comparison">
                <div className="text-before">
                  <h4>Original Text ({moodifyResult.original_sentiment}):</h4>
                  <p>"{moodifyResult.original_text}"</p>
                </div>
                
                <div className="transformation-arrow">
                  ⬇️ Transformed to {moodifyResult.target_sentiment} ⬇️
                </div>
                
                <div className="text-after">
                  <h4>Moodified Text ({moodifyResult.new_sentiment}):</h4>
                  <p className={`moodified-text ${moodifyResult.new_sentiment}`}>
                    "{moodifyResult.modified_text}"
                  </p>
                </div>
              </div>

              {moodifyResult.changes_made && moodifyResult.changes_made.length > 0 && (
                <div className="changes-section">
                  <h4>Changes Made:</h4>
                  <ul className="changes-list">
                    {moodifyResult.changes_made.map((change, index) => (
                      <li key={index}>{change}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="moodify-actions">
                <button 
                  onClick={useMoodifiedText}
                  className="use-moodified-btn"
                >
                  📝 Use This Text
                </button>
                
                <button 
                  onClick={() => setMoodifyResult(null)}
                  className="dismiss-btn"
                >
                  ❌ Dismiss
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="sample-texts">
          <h3>Try these sample texts:</h3>
          <div className="sample-buttons">
            <button 
              onClick={() => setText("I absolutely love this amazing weather! It's such a beautiful and perfect day!")}
              className="sample-btn positive"
            >
              😊 Positive Sample
            </button>
            <button 
              onClick={() => setText("I'm really disappointed and frustrated with how things turned out today.")}
              className="sample-btn negative"
            >
              😞 Negative Sample
            </button>
            <button 
              onClick={() => setText("The meeting was okay. Nothing particularly exciting or disappointing happened.")}
              className="sample-btn neutral"
            >
              😐 Neutral Sample
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
