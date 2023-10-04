export default async function request(input, game_id, api) {
  // TODO RUN LOCAL: Comment this out
  const startGameURL = "https://hoodwinked.onrender.com/" + api + "/";
  // const startGameURL = "http://127.0.0.1:8000/" + api + "/";

  try {
    const response = await fetch(startGameURL, {
      method: "POST",
      body: JSON.stringify({
          input: input,
          game_id: game_id,
      }),
    });

    if (!response.ok) {
      return { error: "Sorry, the backend server timed out! Please refresh and play again." };
    }

    return response;
  } catch (err) {
    console.error("Sorry, the backend server timed out! Please refresh and play again.");
  }
}