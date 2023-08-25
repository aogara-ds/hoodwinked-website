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
        <p className={styles.option}><a href="https://arxiv.org/abs/2308.01404">about</a></p>
        <p className={styles.option}>
          <a href="https://github.com/aogara-ds/hoodwinked">github</a>
        </p>
        <p className={styles.option}><a href="https://www.linkedin.com/in/abogara/">contact</a></p>
      </div>
    </div>
  );
}

function startGameButton(gameInProgress, setShowLogin) {
  return (
    <div>
      <p className={styles.option} onClick={() => setShowLogin(true)}>
        new game
      </p>
    </div>
  );
}

export default Sidebar;
