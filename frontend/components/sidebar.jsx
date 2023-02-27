import React, { useContext } from "react";
import { GameStateContext, ShowLoginContext } from "../pages";
import styles from "../styles/sidebar.module.css";

function Sidebar() {
  const [{ gameInProgress }] = useContext(GameStateContext);
  const [, setShowLogin] = useContext(ShowLoginContext);

  return (
    <div className={styles.sidebar}>
      <h1 className={styles.h1}>hoodwinked</h1>
      <h3 className={styles.h3}>a game of lies and deceit</h3>
      <div className={styles.play}>
        {startGameButton(gameInProgress, setShowLogin)}
      </div>
      <div className={styles.info}>
        <p className={styles.option}>about</p>
        <p className={styles.option}>
          <a href="https://github.com/aogara-ds/hoodwinked">github</a>
        </p>
        <p className={styles.option}>contact</p>
      </div>
    </div>
  );
}

function startGameButton(gameInProgress, setShowLogin) {
  let text = "";
  if (gameInProgress) {
    text = "new game";
  } else {
    text = "start game";
  }
  return (
    <div>
      <p className={styles.option} onClick={() => setShowLogin(true)}>
        {text}
      </p>
    </div>
  );
}

export default Sidebar;
