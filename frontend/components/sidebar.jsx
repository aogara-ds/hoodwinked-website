import { useState } from 'react';
import React from 'react';
import styles from '../styles/sidebar.module.css';

export default function Sidebar() {
  return (
  <div className={styles.sidebar}>
    <h1 className={styles.h1}>hoodwinked</h1>
    <h3 className={styles.h3}>a game of lies and deceit</h3>
    <div className={styles.play}>
      <p className={styles.option}>sign up</p>
      <p className={styles.option}>log in</p>
      <p className={styles.option}>play as guest</p>
    </div>
    <div className={styles.info}>
      <p className={styles.option}>about</p>
      <p className={styles.option}>github</p>
      <p className={styles.option}>contact</p>
    </div>
  </div>
  );
}

