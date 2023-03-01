import styles from "../styles/chat.module.css";
import React, { useState, useEffect, useRef, useContext } from "react";
import { GameStateContext } from "../pages";
import takeAction from '../api/takeAction.jsx'

// TODO: Remove history state object, use history property of GameStateContext

export default function Chat() {

  // State
  const [userInput, setUserInput] = useState("");

  // References
  const chatHistoryRef = useRef(null);
  const chatInputRef = useRef(null);

  // Context
  const [gameState, setGameState] = useContext(GameStateContext);

  // When the API returns, display the game's history
  // useEffect(() => {
  //   if (gameState.waiting == false) {
  //     // Show history
  //     setGameState({
  //       ...gameState,
  //       history: gameState.history.split("\n").filter((line) => line !== ""),
  //     })
  //   }
  // }, [gameState.waiting]);

  const getIntegers = (string, afterKeyword) => {
    const regex = /\d+/g;
    const matches = string.slice(string.indexOf(afterKeyword)).match(regex);
    const integers = matches.map(match => parseInt(match));
    return integers
  }

  const handleAction = async () => {  
    console.log('handleAction')
    
    // If userInput is not a valid action, request a new input
    const userAction = parseInt(userInput)
    const possibleActions = await getIntegers(gameState.history, "Possible Actions:")
    if (!possibleActions.includes(userAction)) {
      const error_message = "Sorry, that's not a valid action. Please enter a number from the list above."
      setGameState({
        ...gameState,
        history: gameState.history + "\n\n" + error_message,
        // history: [...history, error_message],
      })
    }

    // If userInput is a valid action, send it to the API and store response
    else {
      console.log('handleAction: valid action')
      const newGameState = await takeAction(userAction, gameState.game_id)
      await setGameState({
        ...gameState, 
        ...newGameState,
      })
      console.log(await gameState.history)
    }
  }

  // Handle the user's submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (userInput.trim() === "") { return }
    setUserInput("");

    // Begin waiting
    setGameState({
      ...gameState,
      waiting: true,
    });

    // Handle submission based on expected next_request
    if (gameState.next_request === "action") { handleAction() } 
    // TODO: Handle statement and vote requests

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

  const displayHistory = () => {
    if (gameState.history) {
      const history_list = gameState.history.split("\n").filter((line) => line !== "")
      return history_list.map((paragraph, index) => (
        <p key={index}>{paragraph}</p>
      ));
    }
  }

  return (
    <div className={styles.window}>
      <div ref={chatHistoryRef} className={styles.history}>
        {displayHistory()}
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

// Second API call: HandleSubmit should call the API
// TODO: Don't accept Enter or Send when gameState.loading is true
// TODO: Animated loading ellipsis
// TODO: Spacing between single \n lines
