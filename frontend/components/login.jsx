import { useRef } from 'react';
import React from 'react';
import styles from '../styles/login.module.css';

export default function Login({ setShowLogin, startGame }) {
    // Reference to the content of the input field
    const inputRef = useRef(null);

    // Set the name in the global state, and get rid of the login popup
    function handleSubmit(e) {
      e.preventDefault();
      setShowLogin(false);
      startGame(
        inputRef.current.value,
        // TODO: Ask player if they would like to be the killer
        (Math.floor(Math.random() * 2) == 0)
      )
    }
  
    return (
      <div className={styles.loginOverlay}>
        <div className={styles.login}>
            <form onSubmit={handleSubmit}>
                {/* <h2>login to play</h2> */}
                <p>What is your name?</p>
                <label>
                  <input type="text" ref={inputRef}/>
                </label>
                <button type="submit">submit</button>
            </form>
        </div>
      </div>
    );
  }
  