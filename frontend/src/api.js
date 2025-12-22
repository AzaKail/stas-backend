import axios from "axios";

export const API_BASE = import.meta.env.VITE_API_BASE;
export const BACKEND_ORIGIN = import.meta.env.VITE_BACKEND_ORIGIN;

export const api = axios.create({
  baseURL: API_BASE,
  withCredentials: false,
});

export function absMedia(url) {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return `${BACKEND_ORIGIN}${url}`;
}
