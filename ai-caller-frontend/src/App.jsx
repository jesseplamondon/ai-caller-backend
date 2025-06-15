import React, { useState } from 'react';
import './App.css';

function App() {
  const [filename, setFilename] = useState('');
  const [transcript, setTranscript] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleTranscribe = async () => {
    if (!filename) {
      setError('Please enter a filename.');
      return;
    }

    setLoading(true);
    setError('');
    setTranscript('');
    setSummary('');

    try {
      const response = await fetch(`http://localhost:8000/process-audio/?filename=${encodeURIComponent(filename)}`);
      if (!response.ok) throw new Error(`Server error: ${response.statusText}`);
      const data = await response.json();

      setTranscript(data.transcript);
      setSummary(data.summary);
    } catch (err) {
      setError(`Transcription failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <h1>🎙️ AI Call Transcriber</h1>
      <input
        type="text"
        placeholder="Enter filename (e.g., Audio1.mp3)"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
        className="filename-input"
      />
      <button onClick={handleTranscribe} disabled={loading}>
        {loading ? 'Processing...' : 'Transcribe'}
      </button>

      {error && <p className="error">{error}</p>}

      {transcript && (
        <>
          <h2>📝 Transcript</h2>
          <pre>{transcript}</pre>
        </>
      )}

      {summary && (
        <>
          <h2>🧠 Summary</h2>
          <pre>{summary}</pre>
        </>
      )}
    </div>
  );
}

export default App;
