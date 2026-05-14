import { motion } from "framer-motion";

export default function ConfidenceBar({ digit, probability, isTop }) {
  const percent = Math.round(probability * 100);

  return (
    <div className="flex items-center gap-3 w-full">
      <span className={`text-sm font-mono w-4 text-right
                        ${isTop ? "text-violet-400 font-bold" 
                                : "text-slate-400"}`}>
        {digit}
      </span>
      <div className="flex-1 bg-slate-700 rounded-full h-2 overflow-hidden">
        <motion.div
          className={`h-full rounded-full
                      ${isTop 
                        ? "bg-gradient-to-r from-violet-500 to-indigo-500" 
                        : "bg-slate-500"}`}
          initial={{ width: 0 }}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.5, ease: "easeOut" }}
        />
      </div>
      <span className={`text-xs w-9 text-right
                        ${isTop ? "text-violet-400 font-bold" 
                                : "text-slate-500"}`}>
        {percent}%
      </span>
    </div>
  );
}

