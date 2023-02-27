import React, { useState } from "react";
import Sidebar from "../components/sidebar.jsx";
import Chat from "../components/chat.jsx";
import Login from "../components/login.jsx";
import Head from "next/head";
import fetchStartGame from "../api/startGame.jsx";

export const ShowLoginContext = React.createContext();
export const GameStateContext = React.createContext();

const defaultGameState = {
  gameInProgress: false,
  game_id: null,
  history: "",
  killer: false,
  next_request: null,
  playerName: "",
  prompt_type: null,
};

function HomePage() {

  const [showLogin, setShowLogin] = useState(false);
  const [gameState, setGameState] = useState(defaultGameState);

  async function startGame(playerName, killer) {
    console.log("Parent startGame in HomePage")

    const newGameState = await fetchStartGame(playerName, killer);

    setGameState({
      ...defaultGameState,
      playerName: playerName,
      killer: killer,
      ...newGameState,
      gameInProgress: true,
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
