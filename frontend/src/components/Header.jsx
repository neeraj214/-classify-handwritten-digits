export default function Header() {
  return (
    <header className="w-full py-6 px-4 text-center">
      <div className="inline-flex items-center gap-3 mb-2">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br 
                        from-violet-500 to-indigo-600 
                        flex items-center justify-center text-white 
                        text-xl font-bold shadow-lg">
          ✍
        </div>
        <h1 className="text-3xl font-bold bg-gradient-to-r 
                       from-violet-400 to-indigo-400 
                       bg-clip-text text-transparent">
          Digit Classifier
        </h1>
      </div>
      <p className="text-slate-400 text-sm">
        Draw a digit (0–9) and let the model predict it
      </p>
    </header>
  );
}

