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
      // startGame: false,
      playerName: '',
      killer: false,
      gameInProgress: false,
    };
  }

  render() {
    return (
      <div>
        <Sidebar 
          playerName={this.state.playerName} 
          setShowLogin={this.setShowLogin}  
          gameInProgress={this.gameInProgress}
        />
        <Chat 
          startGame={this.state.startGame}
          setStartGame={(value)=>this.setState({startGame: value})}
          playerName={this.state.playerName}
          killer={this.state.killer}
          // Add a setter for any global variables
        />
        {this.state.showLogin && 
          <Login 
            setShowLogin={(value)=>this.setState({showLogin: value})} 
            setStartGame={(value)=>this.setState({startGame: value})}
            setPlayerName={(value)=>this.setState({playerName: value})}
            setKiller={(value)=>this.setState({killer: value})}
          />
        }
      </div>
    );
  }

  startGame = async (newName, killer) => {
    this.setState({playerName: newName});
    this.setState({killer: killer});
    this.setState({gameState: await fetchStartGame(newName, killer)});
    this.setState({gameInProgress: true})
  }
}
