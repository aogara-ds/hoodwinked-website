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
      <a href="https://docs.google.com/document/d/1671h6NG9CpXYWrccapQBlAyPl99Qsjyl6eeslyoLlnI/edit?usp=sharing">about</a>
        <a href="https://github.com/aogara-ds/hoodwinked">github</a>
        <a href="mailto:aidanogara623@gmail.com">contact</a>
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