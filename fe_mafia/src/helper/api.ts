const BASE_URL = import.meta.env.VITE_API_URL;

function getAuthToken(): string | null {
  return localStorage.getItem("token");
}

async function getHeaders(): Promise<HeadersInit> {
  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };
  const token = getAuthToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorText = await response.text();
    try {
      const errorJson = JSON.parse(errorText);
      errorText = errorJson.message || errorText;
    } catch {}
    throw new Error(`API error ${response.status}: ${errorText}`);
  }
  if (response.status === 204) {
    return {} as T;
  }
  return response.json();
}

export async function get<T>(endpoint: string): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "GET",
    headers,
  });
  return handleResponse<T>(response);
}

export async function post<T>(endpoint: string, data: any): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  return handleResponse<T>(response);
}

export async function patch<T>(endpoint: string, data: any): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "PATCH",
    headers,
    body: JSON.stringify(data),
  });
  return handleResponse<T>(response);
}

export async function del<T>(endpoint: string): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "DELETE",
    headers,
  });
  return handleResponse<T>(response);
}
