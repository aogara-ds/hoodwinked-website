export default async function fetchStartGame(playerName, killer) {
  // TODO RUN LOCAL: Comment this out
  // const startGameURL = "https://hoodwinked.onrender.com/start/";
  const startGameURL = "http://127.0.0.1:8000/start/";

  try {
    const response = await fetch(startGameURL, {
      method: "POST",
      body: JSON.stringify({
        name: playerName,
        killer: killer,
      }),
    });

    if (!response.ok) {
      return { error: "Sorry, the backend server timed out! Please refresh and play again." };
    }

    const data = await response.json();
    return await data;
  } catch (err) {
    console.error("Sorry, the backend server timed out! Please refresh and play again.");
  }
}
