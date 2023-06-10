export default async function request(input, game_id, api) {
  const startGameURL = "http://127.0.0.1:8000/" + api + "/";
  // const startGameURL = "https://hoodwinked.onrender.com/" + api + "/";
  try {
    const response = await fetch(startGameURL, {
      method: "POST",
      body: JSON.stringify({
          input: input,
          game_id: game_id,
      }),
    });
    return response;
  } catch (err) {
    // TODO: Handle error
    console.error(err);
  }
}