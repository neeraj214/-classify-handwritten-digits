# Frontend Setup & Development Guide

## Overview

The MNIST Digit Classifier frontend is built with **React** and **Vite**, providing an interactive drawing interface for digit classification.

## Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Backend Connection

Create a `.env` file in the frontend directory (optional):

```bash
# Default: http://localhost:8000
VITE_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
npm run dev
```

The frontend will be available at: `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── main.jsx              # Entry point
│   ├── App.jsx               # Main application component
│   ├── App.css               # Main styles
│   ├── index.css             # Global styles
│   ├── constants.js          # UI constants and config
│   ├── components/
│   │   ├── Header.jsx        # App header
│   │   ├── DrawingCanvas.jsx # Drawing interface
│   │   ├── PredictionResult.jsx  # Result display
│   │   └── ConfidenceBar.jsx # Confidence visualization
│   ├── hooks/
│   │   └── useCanvas.js      # Canvas drawing logic
│   └── utils/
│       └── api.js            # Backend API communication
├── public/                   # Static assets
├── vite.config.js           # Vite configuration
├── eslint.config.js         # ESLint rules
├── package.json             # Dependencies
└── README.md               # Project info
```

## Development

### Available Scripts

```bash
# Start development server with hot reload
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_URL` | http://localhost:8000 | Backend API URL |

## Building for Production

```bash
npm run build
```

Output: `dist/` directory

## Next Steps

- [Backend Setup Guide](../backend/README.md)
- [Model Performance Report](../MODEL_PERFORMANCE.md)
- [Frontend Integration Guide](../FRONTEND_INTEGRATION.md)
