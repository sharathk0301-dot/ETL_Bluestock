const API_BASE_URL = import.meta.env.DEV
  ? '/api/v1'
  : 'http://127.0.0.1:8000/api/v1';

async function fetchJson(url) {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Network error: ${response.status} ${response.statusText}`);
  }

  return response.json();
}

export async function fetchCompanies() {
  return fetchJson(`${API_BASE_URL}/companies/`);
}

export async function fetchCompanyDetail(symbol) {
  if (!symbol) {
    throw new Error('Missing company symbol');
  }

  return fetchJson(`${API_BASE_URL}/companies/${symbol}/`);
}
