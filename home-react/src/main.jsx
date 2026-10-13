import React from 'react';
import { createRoot, hydrateRoot } from 'react-dom/client';
import App from './App.jsx';
import './styles.css';

const root = document.getElementById('root');

if (import.meta.env.DEV || !root.hasChildNodes()) {
  createRoot(root).render(<App />);
} else {
  hydrateRoot(root, <App />);
}
