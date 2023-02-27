import styles from "../styles/chat.module.css";
import React, { useState, useEffect, useRef, useContext } from "react";
import { GameStateContext } from "../pages";

export default function Chat() {

  // State
  const [history, setHistory] = useState([]);
  const [userInput, setUserInput] = useState("");

  // References
  const chatHistoryRef = useRef(null);
  const chatInputRef = useRef(null);

  // Context
  const [gameState, setGameState] = useContext(GameStateContext);

  // Start the game when waiting changes
  useEffect(() => {
    if (gameState.waiting == false) {
      console.log('finished waiting!')
      // Show the game's history
      console.log(gameState)
      setHistory(gameState.history.split("\n\n"))
    } else {
      console.log('waiting...')
    }
  }, [gameState.waiting]);

  // Handle the user's action submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (userInput.trim() === "") { return }

    // Begin waiting
    setGameState({
      ...gameState,
      waiting: true,
    });

    setUserInput("");

    // TODO: Update history
    // await
    setHistory([...history, "lorem ipsum"]);

    // Finish waiting
    setGameState({
      ...gameState,
      waiting: false,
    });
  };

  // Handle the enter key
  const handleEnter = (e) => {
    if (e.key === "Enter" && userInput) {
      if (!e.shiftKey && userInput) {
        handleSubmit(e);
      }
    } else if (e.key === "Enter") {
      e.preventDefault();
    }
  };

  useEffect(() => {
    const history = chatHistoryRef.current;
    history.scrollTop = history.scrollHeight;
  });

  useEffect(() => {
    chatInputRef.current.focus();
  }, []);

  return (
    <div className={styles.window}>
      <div ref={chatHistoryRef} className={styles.history}>
        {history.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      <div className={styles.input}>
        <textarea
          disabled={gameState.waiting}
          onKeyDown={handleEnter}
          ref={chatInputRef}
          autoFocus={false}
          rows={1}
          maxLength={512}
          type="text"
          id="userInput"
          name="userInput"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <button type="submit" onClick={handleSubmit}>
          send
        </button>
      </div>
    </div>
  );
}
