import React, { useEffect, useRef, useContext } from "react";
import styles from "../styles/login.module.css";
import { ShowLoginContext } from "../pages";

export default function Login({ startGame }) {
  const [, setShowLogin] = useContext(ShowLoginContext);

  // Reference to the content of the input field
  const inputRef = useRef(null);

  // Set the name in the global state, and get rid of the login popup
  async function startNewGame(e, startGameFunction) {
    e.preventDefault();

    setShowLogin(false);

    const playerName = inputRef.current.value;

    // TODO: Ask player if they'd like to be the killer
    const killer = Math.floor(Math.random() * 2) == 0;

    await startGameFunction(playerName, killer);
  }

  // Focus on the input field when the component mounts
  useEffect(() => {
    inputRef.current.focus();
  }, []);

  return (
    <div className={styles.loginOverlay}>
      <div className={styles.login}>
        <form onSubmit={startGame}>
          {/* <h2>login to play</h2> */}
          <p>What is your name?</p>
          <label>
            <input type="text" ref={inputRef} />
          </label>
          <button type="submit">submit</button>
        </form>
      </div>
    </div>
  );
}
