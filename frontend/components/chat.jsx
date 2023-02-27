import styles from "../styles/chat.module.css";
import React, { useState, useEffect, useRef } from "react";

export default function Chat() {
  const [history, setHistory] = useState([]);
  const [userInput, setUserInput] = useState("");
  const [loading, setLoading] = useState(false);

  const chatHistoryRef = useRef(null);
  const chatInputRef = useRef(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (userInput.trim() === "") {
      return;
    }

    setLoading(true);

    // TODO: Send user question and history to API

    setUserInput("");

    // TODO: Update history
    // await
    setHistory([...history, "lorem ipsum"]);

    setLoading(false);
  };

  const handleEnter = (event) => {
    if (event.key === "Enter" && userInput) {
      if (!event.shiftKey && userInput) {
        handleSubmit(event);
      }
    } else if (event.key === "Enter") {
      event.preventDefault();
    }
  };

  useEffect(() => {
    const history = chatHistoryRef.current;
    history.scrollTop = history.scrollHeight;
  });

  useEffect(() => {
    chatInputRef.current.focus();
  }, []);

  return (
    <div className={styles.window}>
      <div ref={chatHistoryRef} className={styles.history}>
        {history.map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>
      <div className={styles.input}>
        <textarea
          disabled={loading}
          onKeyDown={handleEnter}
          ref={chatInputRef}
          autoFocus={false}
          rows={1}
          maxLength={512}
          type="text"
          id="userInput"
          name="userInput"
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
        />
        <button type="submit" onClick={handleSubmit}>
          send
        </button>
      </div>
    </div>
  );
}
