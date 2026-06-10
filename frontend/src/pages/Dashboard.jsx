import BandwidthChart from "../components/BandwidthChart";
import { useEffect, useState } from "react";
import { getDevices, getAlerts } from "../services/api";
import useWebSocket from "../hooks/useWebSocket";

export default function Dashboard() {
  const [devices, setDevices] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const liveMessage = useWebSocket();

  useEffect(() => {
    getDevices().then((res) => setDevices(res.data));
    getAlerts().then((res) => setAlerts(res.data));
  }, []);

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">

      {/* HEADER */}
      <h1 className="text-5xl font-extrabold text-cyan-400 mb-8">
        NetWatch Dashboard
      </h1>

      {/* STATS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">

        <div className="bg-slate-900 p-6 rounded-2xl border border-cyan-500 shadow-lg hover:scale-105 transition duration-300">
          <h3 className="text-gray-400 text-lg">Devices</h3>
          <p className="text-5xl font-extrabold text-cyan-400 mt-3">
            {devices.length}
          </p>
        </div>

        <div className="bg-slate-900 p-6 rounded-2xl border border-red-500 shadow-lg hover:scale-105 transition duration-300">
          <h3 className="text-gray-400 text-lg">Alerts</h3>
          <p className="text-5xl font-extrabold text-red-400 mt-3">
            {alerts.length}
          </p>
        </div>

        <div className="bg-slate-900 p-6 rounded-2xl border border-green-500 shadow-lg hover:scale-105 transition duration-300">
          <h3 className="text-gray-400 text-lg">Status</h3>
          <p className="text-4xl font-extrabold text-green-400 mt-3">
            Online
          </p>
        </div>

      </div>

      {/* LIVE EVENT */}
      <div className="bg-slate-900 border border-green-500 p-5 rounded-2xl mb-8 shadow-lg">
        <p className="text-green-400 text-lg font-semibold">
          🔔 Live Event: {liveMessage || "En attente..."}
        </p>
      </div>

      {/* BANDWIDTH */}
      <div className="bg-slate-900 border border-cyan-500 rounded-2xl p-6 mb-8 shadow-lg">

        <h2 className="text-3xl font-bold text-cyan-400 mb-6">
          Network Bandwidth
        </h2>

        <BandwidthChart />

      </div>

      {/* DEVICES + ALERTS */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        {/* DEVICES */}
        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-lg">

          <h2 className="text-2xl font-bold text-cyan-400 mb-4">
            Devices
          </h2>

          {devices.length === 0 && (
            <p className="text-gray-400">
              Aucun appareil détecté
            </p>
          )}

          {devices.map((d, i) => (
            <div
              key={i}
              className="bg-slate-800 p-4 rounded-xl mb-3 hover:bg-slate-700 transition"
            >
              <p className="font-bold text-lg">
                {d.name}
              </p>

              <p className="text-gray-300">
                {d.ip}
              </p>
            </div>
          ))}
        </div>

        {/* ALERTS */}
        <div className="bg-slate-900 p-5 rounded-2xl border border-slate-800 shadow-lg">

          <h2 className="text-2xl font-bold text-red-400 mb-4">
            Alerts
          </h2>

          {alerts.length === 0 && (
            <p className="text-gray-400">
              Aucune alerte
            </p>
          )}

          {alerts.map((a, i) => (
            <div
              key={i}
              className="bg-red-900/20 border border-red-500 p-4 rounded-xl mb-3"
            >
              {a.message}
            </div>
          ))}
        </div>

      </div>

    </div>
  );
}