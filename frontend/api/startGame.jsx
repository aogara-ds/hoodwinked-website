export default async function fetchStartGame(playerName, killer) {
  const startGameURL = "https://hoodwinked.onrender.com/start/";
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
