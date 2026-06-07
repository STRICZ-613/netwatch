import { useEffect, useState } from 'react';
import { apiService } from '../services/api';

// À l'intérieur de ton composant Dashboard :
const [devices, setDevices] = useState([]);
const [logs, setLogs] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  const fetchDashboardData = async () => {
    try {
      const devicesData = await apiService.getDevices();
      const logsData = await apiService.getLogs();
      setDevices(devicesData);
      setLogs(logsData);
    } catch (error) {
      console.error("Erreur lors du chargement du dashboard:", error);
    } finally {
      setLoading(setFalse);
    }
  };

  fetchDashboardData();
}, []);