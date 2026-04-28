import axios from "axios";

const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const access = localStorage.getItem("access_token");
  const session = localStorage.getItem("session_token");
  if (access) config.headers.Authorization = `Bearer ${access}`;
  if (session && !access) config.headers["X-Session-Token"] = session;
  return config;
});

api.interceptors.response.use(
  (response) => {
    const sessionToken = response.headers["x-session-token"];
    if (sessionToken) localStorage.setItem("session_token", sessionToken);
    return response;
  },
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem("refresh_token");
      if (refresh) {
        try {
          const { data } = await axios.post("/api/users/token/refresh/", { refresh });
          localStorage.setItem("access_token", data.access);
          original.headers.Authorization = `Bearer ${data.access}`;
          return api(original);
        } catch {
          localStorage.removeItem("access_token");
          localStorage.removeItem("refresh_token");
          window.location.href = "/login";
        }
      }
    }
    return Promise.reject(error);
  }
);

export default api;
