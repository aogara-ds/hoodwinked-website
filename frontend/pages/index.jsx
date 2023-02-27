import React, { useState } from "react";
import Sidebar from "../components/sidebar.jsx";
import Chat from "../components/chat.jsx";
import Login from "../components/login.jsx";
import Head from "next/head";
import { fetchStartGame } from "../api/startGame.jsx";

// Matt: I think we should use a single context for game state, to make updates easier.
export const ShowLoginContext = React.createContext();
export const GameStateContext = React.createContext();

// Matt: I think we should have a default game state, so we can reset the game state easily.
const defaultGameState = {
  gameInProgress: false,
  game_id: null,
  history: "",
  killer: false,
  next_request: null,
  playerName: "",
  prompt_type: null,
};

// Matt: I set this back to a functional component, since it doesn't need to be a class.
function HomePage() {
  const [showLogin, setShowLogin] = useState(false);

  const [gameState, setGameState] = useState(defaultGameState);

  // Matt: This can be passed individually, or we can include it in the GameStateContext.
  // In this case, we're passing startGame as a prop to Chat and Login.
  async function startGame(newName, killer) {
    const newGameState = await fetchStartGame(newName, killer);

    // This replaces the multiple functions for updating state that we used before.
    setGameState({
      ...defaultGameState,
      playerName: newName,
      killer: killer,
      ...newGameState,
      gameInProgress: true,
    });
  }

  // Matt: Any components under the Providers will have access to the Contexts.
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
