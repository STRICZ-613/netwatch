export default function Navbar() {
  return (
    <div className="h-20 bg-black border-b-2 border-cyan-500 flex items-center justify-between px-8">
      <h1 className="text-3xl font-bold text-cyan-400">
        NetWatch Dashboard
      </h1>

      <div className="bg-green-600 px-4 py-2 rounded-lg text-white font-bold">
        🟢 System Online
      </div>
    </div>
  );
}