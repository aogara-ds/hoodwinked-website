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
    const killer = Math.floor(Math.random() * 2) == 0;

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
          <h1 styles={styles.h1}>hoodwinked</h1>
          <p>enter your name to play:</p>
          <label>
            <input type="text" ref={inputRef} />
          </label>
          <button type="submit">submit</button>
        </form>
        <disclaimer>
          Anonymous data from your gameplay will be stored and analyzed in <a href="https://docs.google.com/document/d/1671h6NG9CpXYWrccapQBlAyPl99Qsjyl6eeslyoLlnI/edit?usp=sharing">our research paper</a>.
        </disclaimer>
      </div>
    </div>
  );
}
