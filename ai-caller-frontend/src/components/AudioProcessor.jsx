import React, { useState } from "react";

export default function AudioProcessor() {
  const [filename, setFilename] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const backendUrl = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

  const handleFetch = async () => {
    if (!filename) return;
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch(
        `${backendUrl}/process-audio/?filename=${encodeURIComponent(filename)}`
      );
      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "auto" }}>
      <h2>Process Audio File</h2>
      <input
        type="text"
        placeholder="Enter audio filename (e.g. Audio1.mp3)"
        value={filename}
        onChange={(e) => setFilename(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleFetch();
          }
        }}
        style={{ width: "100%", padding: 8, fontSize: 16 }}
      />
      <button
        onClick={handleFetch}
        style={{ marginTop: 10, padding: "8px 16px" }}
        disabled={loading}
      >
        Process
      </button>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: 20 }}>
          <h3>Transcript</h3>
          <pre>{result.transcript || "No transcript available"}</pre>

          <h3>AI Response</h3>
          <pre>{result.response || "No response available"}</pre>

          <h3>Summary</h3>
          <pre>{result.summary || "No summary available"}</pre>
        </div>
      )}
    </div>
  );
}
