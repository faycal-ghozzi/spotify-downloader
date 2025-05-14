import { useState } from 'react'

function App() {
  const [token, setToken] = useState(null);
  const [playlists, setPlaylists] = useState([]);

  const fetchPlaylists = async () => {
    const res = await fetch("http://localhost:8000/spotify/playlists", {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    setPlaylists(data.items || []);
  };

  return (
    <div>
      <h1>Spotify Downloader</h1>
      <a href="http://localhost:8000/auth/login">Login with Spotify</a>

      <input placeholder="Paste access token here" onChange={e => setToken(e.target.value)} />

      <button onClick={fetchPlaylists}>Load Playlists</button>

      <ul>
        {playlists.map(p => <li key={p.id}>{p.name}</li>)}
      </ul>
    </div>
  )
}

export default App;
