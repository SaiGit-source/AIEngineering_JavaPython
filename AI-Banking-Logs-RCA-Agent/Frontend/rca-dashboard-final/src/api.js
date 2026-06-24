const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080";

async function requestJson(url, options = {}) {
  const response = await fetch(url, options);

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export function fetchDashboardOverview() {
  return requestJson(`${API_BASE_URL}/api/dashboard/overview`);
}

export function analyzeRca(question) {
  return requestJson(`${API_BASE_URL}/api/rca/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ question })
  });
}
