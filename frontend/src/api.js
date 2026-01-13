import axios from "axios";

export const API_BASE =
  import.meta.env.VITE_API_BASE || "http://localhost:8000/api/";
export const BACKEND_ORIGIN =
  import.meta.env.VITE_BACKEND_ORIGIN || "http://localhost:8000";


export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false,
  paramsSerializer: (params) => {
    const search = new URLSearchParams();
    Object.entries(params || {}).forEach(([key, value]) => {
      if (value === undefined || value === null) return;
      if (Array.isArray(value)) {
        value.forEach((v) => search.append(key, v));
      } else {
        search.append(key, value);
      }
    });
    return search.toString();
  },
});

export function absMedia(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${BACKEND_ORIGIN}${url}`;
}
