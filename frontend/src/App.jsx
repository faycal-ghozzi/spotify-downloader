import { useEffect, useState, useRef } from 'react';
import './App.css';
import { PlayIcon, StopIcon, DownloadIcon } from './icons.jsx';

function App() {
  const [token, setToken] = useState(null);
  const [playlists, setPlaylists] = useState([]);
  const [tracks, setTracks] = useState([]);
  const [currentTab, setCurrentTab] = useState("playlists");
  const [currentPlaylistId, setCurrentPlaylistId] = useState(null);
  const [offset, setOffset] = useState(0);
  const [total, setTotal] = useState(0);
  const [playingTrackId, setPlayingTrackId] = useState(null);
  const [loadingTrackId, setLoadingTrackId] = useState(null);
  const [showProgress, setShowProgress] = useState(false);

  const audioRef = useRef(null);

  let currentAudio = null;

  const handleDownloadTrack = async (track) => {
    const res = await fetch("http://localhost:8000/download/track", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        name: track.name,
        artist: track.artists?.[0]?.name
      })
    });

    const data = await res.json();
    alert(data.status === "ok" ? `Downloaded: ${data.title}` : `Error: ${data.error}`);
  };

  const togglePlayTrack = async (track, index) => {
    const current = audioRef.current;
  
    if (playingTrackId === index && current) {
      current.pause();
      audioRef.current = null;
      setPlayingTrackId(null);
      return;
    }
  
    if (current) {
      current.pause();
      audioRef.current = null;
      setPlayingTrackId(null);
    }
  
    setLoadingTrackId(index);
  
    try {
      const res = await fetch("http://localhost:8000/preview", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: track.name,
          artist: track.artists?.[0]?.name
        })
      });
  
      const data = await res.json();
      setLoadingTrackId(null);
  
      if (!data.preview_url) {
        alert("No preview available.");
        return;
      }
  
      const audio = new Audio(data.preview_url);
      audioRef.current = audio;
  
      audio.play();
      setPlayingTrackId(index);
  
      audio.onended = () => {
        setPlayingTrackId(null);
        audioRef.current = null;
      };
    } catch (err) {
      setLoadingTrackId(null);
      alert("Error playing preview.");
    }
  };
  

  const handleDownloadAll = async () => {
    setShowProgress(true);

    const trackData = tracks.map(t => t.track);
    const res = await fetch("http://localhost:8000/download/all", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tracks: trackData }),
    });

    const data = await res.json();
    setTimeout(() => setShowProgress(false), 2500);
    alert(`Started downloading ${data.count} track(s)`);
  };

  useEffect(() => {
    const hash = window.location.hash;
    if (hash.includes("access_token")) {
      const params = new URLSearchParams(hash.substring(1));
      const accessToken = params.get("access_token");
      setToken(accessToken);
      window.location.hash = "";
    }
  }, []);

  const fetchPlaylists = async () => {
    const res = await fetch("http://localhost:8000/spotify/playlists", {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();
    setPlaylists(data.items || []);
  };

  const fetchTracks = async (type, id = null, newOffset = 0) => {
    setTracks([]);
    setOffset(newOffset);

    let url;
    if (type === "liked") {
      url = `http://localhost:8000/spotify/liked?limit=20&offset=${newOffset}`;
    } else {
      url = `http://localhost:8000/spotify/playlist-tracks/${id}?limit=20&offset=${newOffset}`;
    }

    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await res.json();

    setTracks(data.items || []);
    setTotal(data.total || 0);
    setCurrentPlaylistId(type === "liked" ? "liked" : id);
  };

  const nextPage = () => fetchTracks(
    currentPlaylistId === "liked" ? "liked" : "playlist",
    currentPlaylistId === "liked" ? null : currentPlaylistId,
    offset + 20
  );

  const prevPage = () => {
    if (offset === 0) return;
    fetchTracks(
      currentPlaylistId === "liked" ? "liked" : "playlist",
      currentPlaylistId === "liked" ? null : currentPlaylistId,
      offset - 20
    );
  };

  return (
    <div className="container">
      <h1 className="title">Spotify Downloader</h1>

      {!token && (
        <a href="http://localhost:8000/auth/login">
          <button className="button">Login with Spotify</button>
        </a>
      )}

      {token && (
        <div className="tab-container">
          <div className="tabs">
            <button
              className={`tab ${currentTab === "playlists" ? "active" : ""}`}
              onClick={() => {
                setCurrentTab("playlists");
                setTracks([]);
                fetchPlaylists();
              }}
            >
              Playlists
            </button>
            <button
              className={`tab ${currentTab === "liked" ? "active" : ""}`}
              onClick={() => {
                setCurrentTab("liked");
                fetchTracks("liked");
              }}
            >
              Liked Songs
            </button>
          </div>

          {currentTab === "playlists" && (
            <div className="list">
              {playlists.map(p => (
                <button
                  key={p.id}
                  onClick={() => fetchTracks("playlist", p.id)}
                  className="item-button"
                >
                  {p.name}
                </button>
              ))}
            </div>
          )}

          {tracks.length > 0 && (
            <div className="track-section">
              <h2 className="subheading">Tracks</h2>
              <div className="track-list">
                {tracks.map((t, i) => (
                  <div key={i} className="track-item">
                    <div className="track-row">
                      <div className="track-info">
                        <button
                          className="icon-button"
                          onClick={() => togglePlayTrack(t.track, i)}
                        >
                          {playingTrackId === i
                            ? StopIcon
                            : loadingTrackId === i
                              ? <span>⏳</span>
                              : PlayIcon}
                        </button>
                        <div className="track-text">
                          <span className="track-name">{t.track?.name}</span>
                          <span className="artist">{t.track?.artists?.[0]?.name}</span>
                        </div>
                      </div>
                      <button
                        className="icon-button"
                        onClick={() => handleDownloadTrack(t.track)}
                      >
                        {DownloadIcon}
                      </button>
                    </div>
                  </div>
                ))}
              </div>

              <div className="pagination">
                <button
                  onClick={prevPage}
                  disabled={offset === 0}
                  className="page-button"
                >
                  Previous
                </button>
                <span className="page-info">
                  Page {Math.floor(offset / 20) + 1}
                </span>
                <button
                  onClick={nextPage}
                  disabled={offset + 20 >= total}
                  className="page-button"
                >
                  Next
                </button>
              </div>

              <button className="download-all" onClick={handleDownloadAll}>
                Download All
              </button>
            </div>
          )}
        </div>
      )}

      {showProgress && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>Downloading...</h2>
            <p>This may take a while.</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;