import { useState } from "react";

export default function PortScan() {
  const [ip, setIp] = useState("192.168.1.1");
  const [ports, setPorts] = useState([]);

  const scan = () => {
    setPorts([
      { port: 22, status: "OPEN" },
      { port: 80, status: "OPEN" },
      { port: 443, status: "OPEN" },
      { port: 3306, status: "CLOSED" },
      { port: 8080, status: "CLOSED" },
    ]);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">

      <h1 className="text-4xl font-extrabold text-cyan-400 mb-8">
        Port Scanner
      </h1>

      <div className="bg-slate-900 p-6 rounded-2xl border border-slate-800 mb-8">

        <label className="block mb-3 text-gray-400">
          IP Address
        </label>

        <div className="flex gap-4">

          <input
            type="text"
            value={ip}
            onChange={(e) => setIp(e.target.value)}
            className="flex-1 bg-slate-800 border border-slate-700 rounded-xl p-3 text-white"
          />

          <button
            onClick={scan}
            className="bg-cyan-600 hover:bg-cyan-500 px-6 rounded-xl font-bold"
          >
            Scan
          </button>

        </div>

      </div>

      {ports.length > 0 && (

        <div className="bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden">

          <div className="grid grid-cols-2 bg-slate-800 p-4 font-bold">
            <div>Port</div>
            <div>Status</div>
          </div>

          {ports.map((p, i) => (
            <div
              key={i}
              className="grid grid-cols-2 p-4 border-t border-slate-800"
            >
              <div>{p.port}</div>

              <div>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-bold ${
                    p.status === "OPEN"
                      ? "bg-green-500/20 text-green-400"
                      : "bg-red-500/20 text-red-400"
                  }`}
                >
                  {p.status}
                </span>
              </div>
            </div>
          ))}

        </div>

      )}

    </div>
  );
}