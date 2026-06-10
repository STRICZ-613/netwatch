import { Link } from "react-router-dom";
import { FaTachometerAlt, FaHistory, FaNetworkWired } from "react-icons/fa";

export default function Sidebar() {
  return (
    <div className="w-72 h-screen bg-black border-r-2 border-cyan-500 fixed left-0 top-0">

      <div className="text-cyan-400 text-4xl font-bold p-6">
        NetWatch
      </div>

      <nav className="flex flex-col gap-4 p-4">

        <Link
          to="/"
          className="flex items-center gap-3 p-4 bg-slate-900 rounded-xl hover:bg-slate-800 transition"
        >
          <FaTachometerAlt className="text-cyan-400 text-xl" />
          Dashboard
        </Link>

        <Link
          to="/logs"
          className="flex items-center gap-3 p-4 bg-slate-900 rounded-xl hover:bg-slate-800 transition"
        >
          <FaHistory className="text-yellow-400 text-xl" />
          Logs
        </Link>

        <Link
          to="/scan"
          className="flex items-center gap-3 p-4 bg-slate-900 rounded-xl hover:bg-slate-800 transition"
        >
          <FaNetworkWired className="text-green-400 text-xl" />
          Port Scan
        </Link>

      </nav>
    </div>
  );
}