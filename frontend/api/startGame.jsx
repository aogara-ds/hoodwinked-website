export default async function fetchStartGame (newName, killer) {
    const startGameURL = 'http://127.0.0.1:8000/start/'
    try {
      const response = await fetch(startGameURL, {
        method: 'POST',
        body: JSON.stringify({
          playerName: newName,
          killer: killer,
        }),
      });
      const data = await response.json();
      console.log(data)
      return await data;
    } catch (err) {
      // TODO: Handle error
      console.error(err);
    }
  }
  