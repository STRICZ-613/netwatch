import { useEffect, useState } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function BandwidthChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      setData(prev => [
        ...prev.slice(-9),
        {
          time: new Date().toLocaleTimeString(),
          download: Math.random() * 100,
          upload: Math.random() * 50
        }
      ]);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-slate-900 p-4 rounded-lg border border-slate-800 mt-6">
      <h2 className="text-cyan-300 mb-3 font-semibold">
        Bande passante (simulation)
      </h2>

      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="download" stroke="#22c55e" />
          <Line type="monotone" dataKey="upload" stroke="#3b82f6" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}