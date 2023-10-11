import { useEffect, useState } from 'react'
import './App.css'
import { io } from 'socket.io-client';

const URL = "localhost:5000";

const socket = io(URL);

function useSocket() {
  const [transcript, setTranscript] = useState([])
  const [isConnected, setIsConnected] = useState(socket.connected);

  useEffect(() => {
    function onConnect() {
      setIsConnected(true);
    }

    function onDisconnect() {
      setIsConnected(false);
    }

    function onServerMsg(msg) {
      setTranscript(prev => [...prev, msg])
    }
    
    socket.on('connect', onConnect);
    socket.on('disconnect', onDisconnect);
    socket.on('server-msg', onServerMsg)

    return () => {
      socket.off('connect', onConnect);
      socket.off('disconnect', onDisconnect);
      socket.off('server-msg', onServerMsg)
    };
  }, []);
  return [isConnected, transcript, setTranscript]
}

function App() {
  const [isChatStarted, setIsChatStarted] = useState(false)
  const [isConnected, transcript, setTranscript] = useSocket()

  function startChat() {
    socket.emit('start-chat', "aaron-brekke")
    setIsChatStarted(true)
  }

  function onSubmit(e) {
    e.preventDefault()
    const formData = new FormData(e.target)
    const chatMsg = formData.get("chatInput")
    setTranscript(prev => [...prev, chatMsg])
    socket.emit('client-msg', chatMsg)
  }

  return (
    <>
      <h1>Simple frontend to test responses</h1>
      <p>{isConnected ? "Connected" : "Not Connected"}</p>
      <div className="card">
        <button disabled={isChatStarted} onClick={startChat}>
          Start Chat
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
        <form onSubmit={onSubmit}>
          <input name="chatInput" defaultValue="user question" />
          <button type="submit">Submit</button>
        </form>
      </div>
      <ul>
        {transcript.map((line, idx) =>
          <li key={idx}>{line}</li>)}
      </ul>
    </>
  )
}

export default App
