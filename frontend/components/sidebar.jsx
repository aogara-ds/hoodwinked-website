import { Component } from 'react';
import React from 'react';
import styles from '../styles/sidebar.module.css';

export default class Sidebar extends Component {
  constructor(props) {
    super(props);
    this.state = {
      playerName: this.props.playerName,
      setShowLogin: this.props.setShowLogin,
      gameInProgress: this.props.gameInProgress,
    };
  }

  render() {
    return (
      <div className={styles.sidebar}>
        <h1 className={styles.h1}>hoodwinked</h1>
        <h3 className={styles.h3}>a game of lies and deceit</h3>
        <div className={styles.play}>
          {startGameButton(this.props.setShowLogin)}
        </div>
        <div className={styles.info}>
          <p className={styles.option}>about</p>
          <p className={styles.option}>github</p>
          <p className={styles.option}>contact</p>
        </div>
      </div>
    );
  }
}

function startGameButton(gameInProgress, setShowLogin) {
  let text = '';
  if (gameInProgress) {
    text = 'new game'
  } else {
    text = 'start game'
  }
  return (
    <div>
      <p className={styles.option} onClick={() => setShowLogin(true)}>{text}</p>
    </div>
  );
}


