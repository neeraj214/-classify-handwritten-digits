import { useState } from "react";
import Header from "./components/Header";
import DrawingCanvas from "./components/DrawingCanvas";
import PredictionResult from "./components/PredictionResult";
import { predictDigit } from "./utils/api";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handlePredict = async (pixels) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const data = await predictDigit(pixels);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white 
                    flex flex-col items-center">
      <Header />

      <main className="w-full max-w-4xl px-4 pb-12
                       flex flex-col lg:flex-row gap-6 
                       items-start justify-center">
        
        {/* Left — Canvas */}
        <div className="w-full lg:w-auto bg-slate-800/50 
                        border border-slate-700 rounded-2xl p-6
                        backdrop-blur-sm">
          <p className="text-slate-400 text-xs uppercase tracking-wider 
                        mb-4 font-medium">
            Drawing Pad
          </p>
          <DrawingCanvas 
            onPredict={handlePredict} 
            onClear={handleClear} 
          />
        </div>

        {/* Right — Result */}
        <div className="w-full lg:flex-1 bg-slate-800/50 
                        border border-slate-700 rounded-2xl p-6
                        backdrop-blur-sm min-h-[400px]">
          <p className="text-slate-400 text-xs uppercase tracking-wider 
                        mb-4 font-medium">
            Prediction
          </p>
          <PredictionResult 
            result={result} 
            loading={loading} 
            error={error} 
          />
        </div>
      </main>
    </div>
  );
}
