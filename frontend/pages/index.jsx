import React, { useState } from "react";
import Sidebar from "../components/sidebar.jsx";
import Chat from "../components/chat.jsx";
import Login from "../components/login.jsx";
import Head from "next/head";
import fetchStartGame from "../api/startGame.jsx";

export const ShowLoginContext = React.createContext();
export const GameStateContext = React.createContext();

const defaultGameState = {
  gameCount: 0,
  game_id: null,
  history: "",
  killer: false,
  next_request: null,
  playerName: "",
  prompt_type: null,
  waiting: false,
};

function HomePage() {

  const [showLogin, setShowLogin] = useState(false);
  const [gameState, setGameState] = useState(defaultGameState);

  // Login calls this function to start a new game
  async function startGame(playerName, killer) {
    setGameState({
      ...defaultGameState,
      playerName: playerName,
      killer: killer,
      gameCount: gameState.gameCount + 1,
      waiting: true
    });

    const newGameState = await fetchStartGame(playerName, killer);
    // await new Promise(resolve => setTimeout(resolve, 1000));
    // const newGameState = {history: 'test'}

    setGameState({
      ...gameState,
      ...newGameState,
      waiting: false
    });
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
        <GameStateContext.Provider value={[gameState, setGameState]}>
          <ShowLoginContext.Provider value={[showLogin, setShowLogin]}>
            <Sidebar />
            <Chat startGame={startGame} />
            {showLogin && <Login startGame={startGame} />}
          </ShowLoginContext.Provider>
        </GameStateContext.Provider>
      </div>
    </>
  );
}

export default HomePage;
