import { useState } from 'react';
import Sidebar from '../components/sidebar.jsx';
import Chat from '../components/chat.jsx';
import Login from '../components/login.jsx';
import Head from 'next/head';

export default function HomePage() {
  const [showLogin, setShowLogin] = useState(false);
  const [startGame, setStartGame] = useState(false);
  const [playerName, setPlayerName] = useState('');
  const [killer, setKiller] = useState(false);
  const [gameInProgress, setGameInProgress] = useState(false);

  const callStartGame = () => {
    setStartGame(true);
    // forceUpdate();
  }

  return (
    <>
      <Head>
        <title>Hoodwinked</title>
        <meta name="description" content="AI Deception Game" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        {/* TODO: add favicon */}
      </Head>
      <div>
        <Sidebar 
          // playerName={playerName} 
          setShowLogin={(value)=>setShowLogin(value)}  
          gameInProgress={gameInProgress}
        />
        <Chat 
          startGame={startGame}
          setStartGame={(value)=>setStartGame(value)}
          playerName={playerName}
          killer={killer}
          // Add a setter for any global variables
        />
        {showLogin && 
          <Login 
            setShowLogin={(value)=>setShowLogin(value)} 
            setStartGame={callStartGame}
            setPlayerName={(value)=>setPlayerName(value)}
            setKiller={(value)=>setKiller(value)}
          />
        }
      </div>
    </>
  );
}