import { motion, AnimatePresence } from "framer-motion";
import ConfidenceBar from "./ConfidenceBar";

export default function PredictionResult({ result, loading, error }) {
  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center 
                      h-48 gap-3">
        <div className="w-10 h-10 border-4 border-violet-500 
                        border-t-transparent rounded-full animate-spin" />
        <p className="text-slate-400 text-sm">Predicting...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-48">
        <p className="text-red-400 text-sm text-center px-4">
          ⚠ {error}
        </p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="flex flex-col items-center justify-center 
                      h-48 gap-2">
        <p className="text-4xl">🖊️</p>
        <p className="text-slate-400 text-sm">
          Draw a digit to see prediction
        </p>
      </div>
    );
  }

  const { predicted_digit, confidence, all_probabilities, model_used } 
    = result;

  return (
    <AnimatePresence mode="wait">
      <motion.div
        key={predicted_digit + confidence}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -10 }}
        transition={{ duration: 0.3 }}
        className="flex flex-col gap-4 w-full"
      >
        {/* Big predicted digit */}
        <div className="flex flex-col items-center gap-1">
          <motion.div
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 200 }}
            className="text-8xl font-black bg-gradient-to-br 
                       from-violet-400 to-indigo-400 
                       bg-clip-text text-transparent"
          >
            {predicted_digit}
          </motion.div>
          <p className="text-slate-400 text-xs">
            {Math.round(confidence * 100)}% confidence
          </p>
          <p className="text-slate-600 text-xs">
            via {model_used}
          </p>
        </div>

        {/* Confidence bars for all digits */}
        <div className="flex flex-col gap-2 w-full px-2">
          {all_probabilities.map((prob, digit) => (
            <ConfidenceBar
              key={digit}
              digit={digit}
              probability={prob}
              isTop={digit === predicted_digit}
            />
          ))}
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

