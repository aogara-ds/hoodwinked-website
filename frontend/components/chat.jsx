import styles from "../styles/chat.module.css";
import React, { useState, useEffect, useRef, useContext } from "react";
import { GameStateContext } from "../pages";
import request from '../api/request.jsx'
import readStream from '../api/readStream.jsx'

export default function Chat() {

  // State
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);


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
    // This will get overwritten by the next response, how do I do it right?
    // Maybe wait for the API to return the action.
    // var newHistory = gameState.history + userAction.toString()
    // await setGameState({
    //   ...gameState,
    //   history: newHistory,
    // })

    // If userInput is a valid action, send it to the API and store response
    if (possibleActions.includes(userAction)) {
      console.log('handleAction: valid action')

      // Convert integer to action name
      const regex = `${"Possible Actions:"}[\\s\\S]*?${userAction}\\.\\s+(.*?)\\n`
      const actionName = gameState.history.match(regex)[1]

      // 


      // Make API Request
      const response = await request(userAction, gameState.game_id, gameState.next_request)

      // Handle JSON response
      if (response.headers.get('Content-Type') == "application/json") {
        console.log('basic response!')
        const newGameState = await response.json()

        console.log(newGameState.history)

        await setGameState({
          ...gameState, 
          ...newGameState,
        })

        // Allow the user to type again
        setLoading(false);
      } 

      // Handle streaming response
      else { handleStream(response, gameState.history) }
    }

    // If userInput is not a valid action, request a new input
    else { invalidInput() }
  }

  const handleStatement = async () => {
    console.log('handleStatement')

    // Parse userStatement
    const userStatement = userInput

    // Remove the statement question from gameState.history
    // and replace it with the user's statement
    // TODO: Nice backspace and typing animations
    const statement_question = gameState.history.split("\n\n").pop()
    console.log('statement question')
    console.log(statement_question)
    var newHistory = gameState.history.replace(statement_question, '')

    // Make API Request
    const response = await request(userStatement, gameState.game_id, gameState.next_request)

    // Handle response
    handleStream(response, newHistory)
  }

  const handleVote = async () => {
    console.log('handleVote')

    // Parse userVote
    const userVote = parseInt(userInput)
    const possibleVotes = await getIntegers(gameState.history, "Who do you vote to banish?")

    // Remove the vote question from gameState.history, no replacement
    const vote_question = gameState.history.split("\n\n")[-1]
    var newHistory = gameState.history.replace(vote_question, "")
    setGameState({
      ...gameState,
      history: newHistory,
    })

    // If userInput is a valid vote, send it to the API and store response
    if (possibleVotes.includes(userVote)) {
      console.log('handleVote: valid vote')
      console.log(gameState.next_request)

      // Convert integer to player name
      const regex = `${"Who do you vote to banish?"}[\\s\\S]*?${userVote}\\.\\s+(.*?)\\n`
      const playerName = gameState.history.match(regex)[1]

      console.log(userVote)
      console.log(playerName)

      // Make API Request
      const response = await request(playerName, gameState.game_id, gameState.next_request)


      // Handle JSON response
      const newGameState = await response.json()
      console.log(await newGameState.history)
      await setGameState({
        ...gameState, 
        ...newGameState
      })

      // Allow the user to type again
      setLoading(false);
    }
  }

  // Display streaming responses in gameState.history
  // TODO: Store in another file, access history via context
  const handleStream = async (response, newHistory) => {
    console.log('handleStream()')
    console.log('next_')

    // Initialize streaming variables
    const stream = readStream(response);
    const textDecoder = new TextDecoder();
    
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
    if (gameState.next_request.includes("statement")) {
      setGameState({
        ...gameState,
        history: newHistory,
        next_request: "vote",
      })
    } else if (gameState.next_request.includes("action")) {
      setGameState({
        ...gameState,
        history: newHistory,
        next_request: "statement",
      })
    } else { Exception("Invalid next_request")}

    // Allow the user to type again
    setLoading(false);
  }

  // Display message for invalid inputs
  const invalidInput = () => {
    const error_message = "Sorry, that's not a valid action. Please enter a number from the list above."
    setGameState({
      ...gameState,
      history: gameState.history + "\n\n" + error_message,
    })
    setLoading(false);
  }

  // Handle the user's submission
  const handleSubmit = (e) => {
    console.log('handleSubmit')
    e.preventDefault();
    if (userInput.trim() === "") { return }
    setUserInput("");

    // Begin waiting
    setGameState({
      ...gameState,
    });

    // Disable the chat input
    setLoading(true);

    console.log('before choosing handler?')
    console.log(gameState.next_request)

    // Handle submission based on expected next_request
    if (gameState.next_request === "action") { handleAction() } 
    else if (gameState.next_request === "statement") { handleStatement() }
    else if (gameState.next_request === "vote") { handleVote() }
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

  // Scroll to the bottom of the chat history
  useEffect(() => {
    const history = chatHistoryRef.current;
    history.scrollTop = history.scrollHeight;
  });

  // Focus on the chat input
  useEffect(() => {
    chatInputRef.current.focus();
  }, [gameState]);

  const displayHistory = () => {
    console.log(gameState.history);
    if (gameState.history) {
      const message_blocks = gameState.history.split("\n\n").filter((block) => block !== "");
      return message_blocks.map((block, index) => {
        const paragraphs = block.split("\n").filter((paragraph) => paragraph !== "");
        const listRegex = /^\d+\./;
        return (
          <div key={index} className={styles["message-block"]}>
            {paragraphs.map((paragraph, index) => {
              if (listRegex.test(paragraph)) {
                return <li key={index} style={{ marginLeft: "1rem" }}>{paragraph.slice(2)}</li>;
              }
              return <p key={index}>{paragraph}</p>;
            })}
          </div>
        );
      });
    }
  }

  return (
    <div className={styles.window}>
      <div ref={chatHistoryRef} className={styles.history}>
        {displayHistory()}
      </div>
      <div className={styles.input}>
        <textarea
          readOnly={loading}
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
        <button type="submit" onClick={handleSubmit} disabled={loading}>
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