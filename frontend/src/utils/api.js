const BASE_URL = import.meta.env.VITE_API_URL || 
                 "http://localhost:8000";

export async function predictDigit(pixels) {
  const response = await fetch(`${BASE_URL}/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pixels }),
  });

  if (!response.ok) {
    throw new Error("Prediction failed. Is the backend running?");
  }

  return response.json();
}

