const BASE_URL = import.meta.env.VITE_API_URL;
// TODO  Продумать и сделать обработку отправки файлов для обработки фотографий для постов и возможно аватарок

// Фукнция для получения токина авторизации
function getAuthToken(): string | null {
  return localStorage.getItem("token");
}

// Получает заголовки ответа
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

// Обрабатывает ошибки с сервера при запросе
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

// Гет запрос
export async function get<T>(endpoint: string): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "GET",
    headers,
  });
  return handleResponse<T>(response);
}

// Пост запрос
export async function post<T>(endpoint: string, data: any): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers,
    body: JSON.stringify(data),
  });
  return handleResponse<T>(response);
}

// Патч запрос
export async function patch<T>(endpoint: string, data: any): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "PATCH",
    headers,
    body: JSON.stringify(data),
  });
  return handleResponse<T>(response);
}

// Делит запрос
export async function del<T>(endpoint: string): Promise<T> {
  const headers = await getHeaders();
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "DELETE",
    headers,
  });
  return handleResponse<T>(response);
}
