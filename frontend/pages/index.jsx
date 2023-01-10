import Sidebar from '../components/sidebar.jsx';
import Chat from '../components/chat.jsx';

export default function HomePage() {
    return (
      <div>
        {Sidebar()}
        {Chat()}
      </div>
    );
  }