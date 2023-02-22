import { setChatState } from '../components/chat.jsx'

export function fetchStartGame (newName, killer, setChatState) {
    const startGameURL = 'http://127.0.0.1:8000/start/'
    try {
      const response = fetch(startGameURL, {
        method: 'POST',
        body: JSON.stringify({
          playerName: newName,
          killer: killer,
        }),
      });
      const data = response.json();
      return data.history;
    } catch (err) {
      console.error(err);
    }
  }
  