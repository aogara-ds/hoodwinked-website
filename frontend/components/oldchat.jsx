import styles from '../styles/chat.module.css';
import { useEffect, Component, createRef } from 'react'
import fetchStartGame from '../api/startGame.jsx';

const loremIpsum = "The name of the game is cribbage. First one to blink, loses! Cribbage is a game for two players or four players in two partnerships. The game is played with a standard deck of 52 cards. The objective of the game is to be the first player to reach 121 points. Points are earned by forming certain combinations of cards and by pegging. But this is a different game. We're not playing a normal game of cribbage. In fact, our game doesn't use cards at all. It's much more chaotic than that. Here are the rules. The game is played on a board that has 61 squares. Two players each take 15 pieces of their own color, and place them on the 61 squares in any way they choose. The goal is to be the first to have all 15 of your pieces in a row. The players take turns moving their pieces one at a time, and try to block their opponent's pieces from forming a row. If a player has all 15 pieces in a row, they win the game. If a player blinks or looks away while the other player is making their move, they lose the game. What will be the consequence for winning, you ask? Aye, read on, if you dare... The winner of the game earns bragging rights and the right to gloat in the loser's face. There is no prize or reward for winning other than the satisfaction of knowing you bested your opponent. The loser, however, must do whatever the winner says. It could range from making the loser do a silly dance, to buying the winner a milkshake, to doing any kind of task the winner desires. So, be sure to choose your opponent wisely!"

export default class Chat extends Component {
    constructor(props) {
        super(props)

        this.state = {
            history: [],
            userInput: "",
            loading: false
        };

        this.chatHistoryRef = createRef();
        this.chatInputRef = createRef();
    
    }

    componentDidUpdate = (prevProps) => {
        console.log('componentDidUpdate 1')
        const { startGame, setStartGame, playerName, killer } = this.props;
        if (startGame && !prevProps.startGame) {
            console.log('if is yes')
            setStartGame(false);
            fetchStartGame(playerName, killer).then((response) => {
                this.setState({
                    gameId: response.game_id,
                    history: response.history.split("\n\n"),
                    promptType: response.prompt_type,
                    nextRequest: response.next_request,
                })
            })
        }
    }

    handleSubmit = (event) => {
        if (this.state.userInput.trim() == "") {
            return
        }

        // TODO: If the next message is supposed to be an action, verify this is an integer
        
        this.setState({loading: true});

        // TODO: Send user question and history to API

        // Reset user input
        this.setState({userInput: ""})

        // TODO: Update history
        // await
        this.setState({history: [...this.state.history, loremIpsum]})
        this.setState({loading: false})
    }

    // Focus on the input field when the component mounts
    componentDidMount() {
        this.chatInputRef.current.focus();
    }

    // Scroll to the bottom of the chat history when the component updates
    componentDidUpdate(prevProps, prevState) {
        const history = this.chatHistoryRef.current;
        history.scrollTop = history.scrollHeight;
    }

    // Incorporate this function to handle the Enter button
    // Prevent blank submissions and allow for multiline input
    handleEnter = (event) => { // What is e?
        if (event.key === "Enter" && this.state.userInput) {
            if(!event.shiftKey && this.state.userInput) {
                this.handleSubmit(event);
            }
        } else if (event.key === "Enter") {
            event.preventDefault();
        }
    };

    render() {
        return (
            <div className={styles.window}>
                <div ref={this.chatHistoryRef} className = {styles.history}>
                    {this.state.history.map((paragraph, index) => (
                        <p key={index}>{paragraph}</p>
                    ))}
                </div>
                <div className = {styles.input}>
                    <textarea 
                        disabled = {this.state.loading}
                        onKeyDown={this.handleEnter}
                        ref = {this.chatInputRef}
                        autoFocus = {false}
                        rows = {1}
                        maxLength = {512}
                        type="text" 
                        id="userInput" 
                        name="userInput" 
                        // placeholder = {loading? "Waiting for response..." : "Type your question..."}  
                        value = {this.state.userInput} 
                        onChange = {e => this.setState({userInput: e.target.value})}
                    /> 
                    <button type="submit" onClick={this.handleSubmit}>send</button>
                </div>
            </div>
        )
    }
}



Hi Matt! I'm building a React webapp that lets you chat with the OpenAI API. I've got most of the frontend built, but I'm having a lot of trouble with state management and passing props between different components. I've been stuck for several hours on this bug:

There's a parent (HomePage) which contains two children (Chat and Login). Login contains a form that allows you to begin the conversation with OpenAI. The API calls are made by a separate file whose functions we can import wherever we like. Chat is responsible for tracking and displaying all of the message history, so ideally I'd make the API call inside of Chat. So my trouble is this: How do I communicate to Chat that Login's form has been submitted? 

Currently, I'm trying to do this via props. The parent component HomePage has a state variable called startGame. Login uses setState to update this variable upon form submission. Chat receives the variable as a property, and uses useEffect or componentDidUpdate to track changes in the variable and make the API call if it turns from false to true. I think this approach should work, and I've even had it working for moments at a time, but never in a very predictable way. In a moment of misguided ambition, I also tried to rewrite everything from class components to functional components, increasing my confusion. 

Here is the code: https://github.com/aogara-ds/hoodwinked/tree/state_management

I would be hugely appreciative if you could help me with this. Happy to pay you for a full hour even if we solve it in less. And as a beginner tutor in data science and ML, I know the value of a good review! Let me know if you're free tomorrow morning to chat. Aidan