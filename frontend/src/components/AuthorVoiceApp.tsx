import { useState } from 'react';

export default function AuthorVoiceApp() {
  const [text, setText] = useState('');
  const [author, setAuthor] = useState('');
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const generateAudio = async () => {
    setLoading(true);
    setAudioUrl(null);

    const response = await fetch(`${import.meta.env.VITE_BACKEND_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, author }),
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold text-center">📖 AuthorVoice</h1>
      <textarea
        className="w-full p-2 border rounded"
        placeholder="Enter your text here..."
        rows={6}
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <select
        className="w-full p-2 border rounded"
        value={author}
        onChange={(e) => setAuthor(e.target.value)}
      >
        <option value="">Choose an author</option>
        <option value="Rachel">Rachel</option>
      </select>
      <button
        className="w-full bg-blue-600 text-white p-2 rounded disabled:opacity-50"
        onClick={generateAudio}
        disabled={!text || !author || loading}
      >
        {loading ? 'Generating...' : 'Generate Audio'}
      </button>

      {audioUrl && (
        <audio controls className="w-full mt-4">
          <source src={audioUrl} type="audio/mpeg" />
          Your browser does not support the audio element.
        </audio>
      )}
    </div>
  );
}
