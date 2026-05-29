const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function fetchCompanies() {
  const response = await fetch(`${BASE_URL}/companies/`);
  if (!response.ok) {
    throw new Error("Failed to fetch companies");
  }
  return response.json();
}

export async function fetchCompanyDetail(symbol) {
  const response = await fetch(`${BASE_URL}/companies/${symbol}/`);
  if (!response.ok) {
    throw new Error("Failed to fetch company detail");
  }
  return response.json();
}