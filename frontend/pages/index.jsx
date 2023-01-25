import { useState, createContext, Component } from 'react';
import Sidebar from '../components/sidebar.jsx';
import Chat from '../components/chat.jsx';
import Login from '../components/login.jsx';

export default class HomePage extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showLogin: false,
      name: ''
    };
  }

  render() {
    return (
      <div>
        <Sidebar name={this.state.name} setShowLogin={this.setShowLogin}  />
        <Chat />
        {this.state.showLogin && <Login setShowLogin={this.setShowLogin} setName={this.setName}/>}
      </div>
    );
  }

  setShowLogin = (value) => {
    this.setState({showLogin: value});
  }

  setName = (value) => {
    this.setState({name: value});
  }
}

  // Store player's name as a global variable. How?
  // const [data, setData] = useState(null);
