import styles from '../styles/chat.module.css';

const loremIpsum = "The name of the game is cribbage. First one to blink, loses! Cribbage is a game for two players or four players in two partnerships. The game is played with a standard deck of 52 cards. The objective of the game is to be the first player to reach 121 points. Points are earned by forming certain combinations of cards and by pegging. The first player to reach 121 points is the winner. But this is a different game. We're not playing a normal game of cribbage. In fact, our game doesn't use cards at all. It's much more chaotic than that. Here are the rules. The game is played on a board that has 61 squares. Two players each take 15 pieces of their own color, and place them on the 61 squares in any way they choose. The goal is to be the first to have all 15 of your pieces in a row. The players take turns moving their pieces one at a time, and try to block their opponent's pieces from forming a row. If a player has all 15 pieces in a row, they win the game. If a player blinks or looks away while the other player is making their move, they lose the game. What will be the consequence for winning, you ask? Aye, read on, if you dare... The winner of the game earns bragging rights and the right to gloat in the loser's face. There is no prize or reward for winning other than the satisfaction of knowing you bested your opponent. The loser, however, must do whatever the winner says. It could range from making the loser do a silly dance, to buying the winner a milkshake, to doing any kind of task the winner desires. So, be sure to choose your opponent wisely!"

export default function Chat(history) {
    return (
        <div className={styles.window}>
            {ChatHistory(history)}
            {ChatInput()}
        </div>
    )
}

function ChatHistory(history) {
    const history_text = history.history
    let paragraphs = history_text.split('\n')
    return (
        <div className={styles.history}>
            {paragraphs.map(paragraph => <p>{paragraph}</p>)}
        </div>
    )
}

function ChatInput() {
    return (
        <div className={styles.input}>
            <input></input>
            <button>send</button>
        </div>
    )
}