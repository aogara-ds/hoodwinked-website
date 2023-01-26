import { useState, createContext, Component } from 'react';
import Sidebar from '../components/sidebar.jsx';
import Chat from '../components/chat.jsx';
import Login from '../components/login.jsx';
import axios from 'axios';

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showLogin: false,
      playerName: '',
      killer: false,
      history: '',
    };
  }

  render() {
    return (
      <div>
        <Sidebar 
          playerName={this.state.playerName} 
          setShowLogin={this.setShowLogin}  
        />
        <Chat history={this.state.history}/>
        {this.state.showLogin && 
          <Login 
            setShowLogin={this.setShowLogin} 
            startGame={this.startGame}
          />
        }
      </div>
    );
  }

  setShowLogin = (value) => {
    this.setState({showLogin: value});
  }

  startGame = async (newName, killer) => {
    console.log('here we go');
    console.log(newName);
    this.setState({playerName: newName});
    this.setState({killer: killer});
    this.setState({history: await fetchStartGame(newName, killer)});
    console.log('awaited');
    console.log(this.state.history);
  }
}



async function fetchStartGame (newName, killer) {
  console.log('beginning');
  const startGameURL = 'http://127.0.0.1:8000/start/'
  try {
    const response = await fetch(startGameURL, {
      method: 'POST',
      // credentials: 'include',
      mode: 'cors',
      body: JSON.stringify({
        playerName: newName,
        killer: killer,
      }),
    });
    const data = await response.json();
    console.log('end');
    return data.history;
  } catch (err) {
    console.error(err);
  }
}
