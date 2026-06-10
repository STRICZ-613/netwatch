import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import Navbar from "./components/Navbar";

import Dashboard from "./pages/Dashboard";
import Logs from "./pages/Logs";
import PortScan from "./pages/PortScan";

export default function App() {
  return (
    <BrowserRouter>
      <div className="bg-slate-950 min-h-screen text-white">

        <Sidebar />

        <div className="ml-72">
          <Navbar />

          <main className="p-6">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/logs" element={<Logs />} />
              <Route path="/scan" element={<PortScan />} />
            </Routes>
          </main>

        </div>

      </div>
    </BrowserRouter>
  );
}