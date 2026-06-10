import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

// DEVICES
export const getDevices = () => API.get("/devices");

// ALERTS
export const getAlerts = () => API.get("/alerts");

export default API;