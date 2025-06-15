import React, { useEffect, useState } from 'react';

export default function HelloBackend() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/hello')
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
