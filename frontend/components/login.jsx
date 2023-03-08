import React, { useEffect, useRef, useContext } from "react";
import styles from "../styles/login.module.css";
import { ShowLoginContext } from "../pages";

export default function Login(props) {
  const [, setShowLogin] = useContext(ShowLoginContext);

  // Reference to the content of the input field
  const inputRef = useRef(null);

  // Set the name in the global state, and get rid of the login popup
  async function useStartGame(e) {

    // Prevent page from reloading
    e.preventDefault();

    // Hide the login popup
    setShowLogin(false);

    // Get information from the input field
    const playerName = inputRef.current.value;
    // TODO: Ask the user if they want to be the killer
    // const killer = Math.floor(Math.random() * 2) == 0;
    const killer = true;

    // Start game by calling function passed by the parent
    await props.startGame(playerName, killer);
  }

  // Focus on the input field when the component mounts
  useEffect(() => {
    inputRef.current.focus();
  }, []);

  return (
    <div className={styles.loginOverlay}>
      <div className={styles.login}>
        <form onSubmit={useStartGame}>
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
