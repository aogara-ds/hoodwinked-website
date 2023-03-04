export default async function takeAction(userAction, game_id) {
    const startGameURL = "http://127.0.0.1:8000/action/";
    try {
      const response = await fetch(startGameURL, {
        method: "POST",
        body: JSON.stringify({
            action_int: userAction,
            game_id: game_id,
        }),
      });
      const data = await response.json();
      return await data;
    } catch (err) {
      // TODO: Handle error
      console.error(err);
    }
  }
  