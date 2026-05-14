import { useCanvas } from "../hooks/useCanvas";

export default function DrawingCanvas({ onPredict, onClear }) {
  const { 
    canvasRef, 
    startDraw, 
    draw, 
    stopDraw, 
    clearCanvas, 
    getPixels 
  } = useCanvas();

  const handlePredict = () => {
    const pixels = getPixels();
    onPredict(pixels);
  };

  const handleClear = () => {
    clearCanvas();
    onClear();
  };

  return (
    <div className="flex flex-col items-center gap-4">
      {/* Canvas wrapper with glow effect */}
      <div className="relative">
        <div className="absolute inset-0 rounded-2xl 
                        bg-gradient-to-br from-violet-500/20 
                        to-indigo-500/20 blur-xl" />
        <canvas
          ref={canvasRef}
          width={280}
          height={280}
          onMouseDown={startDraw}
          onMouseMove={draw}
          onMouseUp={stopDraw}
          onMouseLeave={stopDraw}
          onTouchStart={startDraw}
          onTouchMove={draw}
          onTouchEnd={stopDraw}
          className="relative rounded-2xl border-2 border-slate-600 
                     cursor-crosshair touch-none
                     hover:border-violet-500 transition-colors duration-200"
          style={{ width: "280px", height: "280px" }}
        />
      </div>

      {/* Buttons */}
      <div className="flex gap-3 w-full">
        <button
          onClick={handleClear}
          className="flex-1 py-3 rounded-xl border border-slate-600 
                     text-slate-300 text-sm font-medium
                     hover:border-slate-400 hover:text-white 
                     transition-all duration-200"
        >
          Clear
        </button>
        <button
          onClick={handlePredict}
          className="flex-1 py-3 rounded-xl 
                     bg-gradient-to-r from-violet-600 to-indigo-600
                     text-white text-sm font-semibold
                     hover:from-violet-500 hover:to-indigo-500
                     active:scale-95 transition-all duration-200
                     shadow-lg shadow-violet-500/25"
        >
          Predict →
        </button>
      </div>
      <p className="text-slate-600 text-xs">
        Draw clearly in the center of the box
      </p>
    </div>
  );
}

