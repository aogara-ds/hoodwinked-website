export default async function fetchStartGame(playerName, killer) {
  const startGameURL = "http://127.0.0.1:8000/start/";
  try {
    const response = await fetch(startGameURL, {
      method: "POST",
      body: JSON.stringify({
        name: playerName,
        killer: killer,
      }),
    });
    const data = await response.json();
    return await data;
  } catch (err) {
    // TODO: Handle error
    console.error(err);
  }
}
