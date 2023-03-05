import styles from "../styles/chat.module.css";
import React, { useState, useEffect, useRef, useContext } from "react";
import { GameStateContext } from "../pages";
import request from '../api/request.jsx'
import readStream from '../api/readStream.jsx'


export default function Chat() {

  // State
  const [userInput, setUserInput] = useState("");

  // References
  const chatHistoryRef = useRef(null);
  const chatInputRef = useRef(null);

  // Context
  const [gameState, setGameState] = useContext(GameStateContext);

  const getIntegers = (string, afterKeyword) => {
    const regex = /\d+/g;
    const matches = string.slice(string.indexOf(afterKeyword)).match(regex);
    const integers = matches.map(match => parseInt(match));
    return integers
  }

  const handleAction = async () => {  
    console.log('handleAction')
    
    // Parse userAction
    const userAction = parseInt(userInput)
    const possibleActions = await getIntegers(gameState.history, "Possible Actions:")

    // TODO: Show it in the expected spot

    // If userInput is a valid action, send it to the API and store response
    if (possibleActions.includes(userAction)) {
      console.log('handleAction: valid action')
      const response = await request(userAction, gameState.game_id, gameState.next_request)

      // Handle JSON response
      if (response.headers.get('Content-Type') == "application/json") {
        console.log('basic response!')
        const newGameState = await response.json()
        await setGameState({
          ...gameState, 
          ...newGameState,
        })
      } 

      // Handle streaming response
      else { handleStream(response, gameState.history) }
    }

    // If userInput is not a valid action, request a new input
    else { invalidInput() }
  }

  // Display message for invalid inputs
  const invalidInput = () => {
    const error_message = "Sorry, that's not a valid action. Please enter a number from the list above."
    setGameState({
      ...gameState,
      history: gameState.history + "\n\n" + error_message,
    })
  }

  // Display streaming responses in gameState.history
  // TODO: Store in another file, access history via context
  const handleStream = async (response) => {
    console.log('streaming response!')

    // Initialize streaming variables
    const stream = readStream(response);
    const textDecoder = new TextDecoder();
    var newHistory = gameState.history;
    
    // Display streaming discussion in gameState.history
    for await (const bytestream of stream) {
      const text = textDecoder.decode(bytestream)
      newHistory += "\n\n" + text
      setGameState({
        ...gameState,
        history: newHistory,
      })
    }

    // Set the next request type to either statement or vote
    if (newHistory.includes("Who do you vote to banish?")) {
      setGameState({
        ...gameState,
        history: newHistory,
        next_request: "vote",
      })
    } else {
      setGameState({
        ...gameState,
        history: newHistory,
        next_request: "statement",
      })
    }
  }

  const handleStatement = async () => {
    console.log('handleStatement')

    // Parse userStatement
    const userStatement = userInput

    // Remove the statement question from gameState.history
    // and replace it with the user's statement
    // TODO: Nice backspace and typing animations
    const statement_question = gameState.history.split("\n\n")[-1]
    var newHistory = gameState.history.replace(statement_question, userStatement)

    // Make API Request
    const response = await request(userStatement, gameState.game_id, gameState.next_request)

    // Handle response
    handleStream(response, newHistory)
  }

  const handleVote = async () => {
    console.log('handleVote')

    // Parse userVote
    const userVote = parseInt(userInput)
    const possibleVotes = await getIntegers(gameState.history, "Possible Votes:")

    // Remove the vote question from gameState.history, no replacement
    const vote_question = gameState.history.split("\n\n")[-1]
    setGameState({
      ...gameState,
      history: gameState.history.replace(vote_question, ""),
    })

    // If userInput is a valid vote, send it to the API and store response
    if (possibleVotes.includes(userVote)) {
      console.log('handleVote: valid vote')
      console.log(gameState.next_request)
      const response = await request(userVote, gameState.game_id, gameState.next_request)

      // Handle JSON response
      const newGameState = await response.json()
      await setGameState({
        ...gameState, 
        ...newGameState,
      })
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
    else if (gameState.next_request === "statement") { handleStatement() }
    else if (gameState.next_request === "vote") { handleVote() }

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
// TODO: Focus on input box after Login