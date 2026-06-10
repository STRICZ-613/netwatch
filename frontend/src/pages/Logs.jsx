import { useEffect, useState } from "react";

export default function Logs() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    setLogs([
      {
        time: "09:15:23",
        type: "INFO",
        message: "PC Bureau connecté",
      },
      {
        time: "09:18:11",
        type: "INFO",
        message: "Téléphone détecté",
      },
      {
        time: "09:22:45",
        type: "WARNING",
        message: "Scan des ports effectué",
      },
      {
        time: "09:30:12",
        type: "CRITICAL",
        message: "Appareil inconnu détecté",
      },
    ]);
  }, []);

  const getColor = (type) => {
    if (type === "INFO") return "text-green-400";
    if (type === "WARNING") return "text-yellow-400";
    return "text-red-400";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">

      <h1 className="text-4xl font-extrabold text-cyan-400 mb-8">
        System Logs
      </h1>

      <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">

        <div className="grid grid-cols-3 bg-slate-800 p-4 font-bold">
          <div>Time</div>
          <div>Level</div>
          <div>Message</div>
        </div>

        {logs.map((log, i) => (
          <div
            key={i}
            className="grid grid-cols-3 p-4 border-t border-slate-800 hover:bg-slate-800 transition"
          >
            <div>{log.time}</div>

            <div className={getColor(log.type)}>
              {log.type}
            </div>

            <div>{log.message}</div>
          </div>
        ))}

      </div>

    </div>
  );
}