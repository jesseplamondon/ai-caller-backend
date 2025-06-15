import React, { useEffect, useState } from 'react';

export default function HelloBackend() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    fetch(`${backendUrl}/api/hello`)
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1>Message from backend:</h1>
      <p>{message}</p>
    </div>
  );
}
