import { useRef, useEffect, useCallback } from "react";

export function useCanvas() {
  const canvasRef = useRef(null);
  const isDrawing = useRef(false);

  const setupCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.strokeStyle = "#FFFFFF";
    ctx.lineWidth = 18;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
  }, []);

  useEffect(() => { setupCanvas(); }, [setupCanvas]);

  const getPos = (e, canvas) => {
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    if (e.touches) {
      return {
        x: (e.touches[0].clientX - rect.left) * scaleX,
        y: (e.touches[0].clientY - rect.top) * scaleY,
      };
    }
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  };

  const startDraw = useCallback((e) => {
    e.preventDefault();
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const { x, y } = getPos(e, canvas);
    isDrawing.current = true;
    ctx.beginPath();
    ctx.moveTo(x, y);
  }, []);

  const draw = useCallback((e) => {
    e.preventDefault();
    if (!isDrawing.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const { x, y } = getPos(e, canvas);
    ctx.lineTo(x, y);
    ctx.stroke();
  }, []);

  const stopDraw = useCallback(() => {
    isDrawing.current = false;
  }, []);

  const clearCanvas = useCallback(() => {
    setupCanvas();
  }, [setupCanvas]);

  const getPixels = useCallback(() => {
    const canvas = canvasRef.current;
    // Create offscreen canvas scaled to 28x28
    const offscreen = document.createElement("canvas");
    offscreen.width = 28;
    offscreen.height = 28;
    const ctx = offscreen.getContext("2d");
    ctx.drawImage(canvas, 0, 0, 28, 28);
    const imageData = ctx.getImageData(0, 0, 28, 28);
    const pixels = [];
    for (let i = 0; i < imageData.data.length; i += 4) {
      // Use red channel (grayscale), normalize to 0-1
      pixels.push(imageData.data[i] / 255);
    }
    return pixels;
  }, []);

  return { 
    canvasRef, 
    startDraw, 
    draw, 
    stopDraw, 
    clearCanvas, 
    getPixels 
  };
}

