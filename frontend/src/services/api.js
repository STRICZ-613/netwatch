// frontend/src/services/api.js

// L'URL de base de ton serveur FastAPI local
const API_BASE_URL = "http://127.0.0.1:8000/api";

export const apiService = {
  // 1. Récupérer tous les appareils réseau
  getDevices: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/devices`);
      if (!response.ok) throw new Error("Erreur lors de la récupération des appareils");
      return await response.json();
    } catch (error) {
      console.error("Erreur apiService (getDevices):", error);
      throw error;
    }
  },

  // 2. Récupérer l'historique des événements / alertes
  getLogs: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/logs`);
      if (!response.ok) throw new Error("Erreur lors de la récupération des logs");
      return await response.json();
    } catch (error) {
      console.error("Erreur apiService (getLogs):", error);
      throw error;
    }
  },

  // 3. Récupérer les statistiques globales (si ta route stats existe)
  getStats: async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`);
      if (!response.ok) throw new Error("Erreur lors de la récupération des statistiques");
      return await response.json();
    } catch (error) {
      console.error("Erreur apiService (getStats):", error);
      return null; // On retourne null pour éviter de faire planter l'affichage si la route n'est pas prête
    }
  }
};