import React, { useContext } from "react";
import { GameStateContext, ShowLoginContext } from "../pages";
import styles from "../styles/topbar.module.css";

function Topbar() {
  const [{ gameInProgress }] = useContext(GameStateContext);
  const [, setShowLogin] = useContext(ShowLoginContext);

  return (
    <div className={styles.topbar}>
      <div className={styles.title}>
        <h1>hoodwinked</h1>
        <div className={styles.play}>
          {startGameButton(gameInProgress, setShowLogin)}
        </div>
      </div>
      <div className={styles.links}>
      <a href="https://arxiv.org/abs/2308.01404">about</a>
        <a href="https://github.com/aogara-ds/hoodwinked">github</a>
        <a href="https://www.linkedin.com/in/abogara/">contact</a>
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

export default Topbar;
