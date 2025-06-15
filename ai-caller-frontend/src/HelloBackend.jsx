import React, { useEffect, useState } from 'react';

export default function HelloBackend() {
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch(`${process.env.REACT_APP_BACKEND_URL}/api/hello`)
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
