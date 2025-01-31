from typing import Dict, List
from datetime import datetime, timedelta
from .schema import Message, ChatStore, Chat, ChatSettings


# Generate some mock conversations
def generate_mock_data() -> ChatStore:
    base_time = datetime.now() - timedelta(days=7)
    
    mock_chats: List[Chat] = [
        Chat(settings=ChatSettings(name="Alice"), messages=[
            Message(sender="Alice", message="Hey there! How are you?", timestamp=base_time + timedelta(minutes=5)),
            Message(sender="user", message="I'm doing great! How about you?", timestamp=base_time + timedelta(minutes=6)),
            Message(sender="Alice", message="Pretty good! Working on some interesting projects.", timestamp=base_time + timedelta(minutes=7)),
        ]),
        Chat(settings=ChatSettings(name="Bob"), messages=[


            Message(sender="Bob", message="Did you see the new movie?", timestamp=base_time + timedelta(days=1)),
            Message(sender="user", message="Not yet! Is it good?", timestamp=base_time + timedelta(days=1, minutes=1)),
            Message(sender="Bob", message="It's amazing! You should definitely watch it.", timestamp=base_time + timedelta(days=1, minutes=2)),
        ]),
        Chat(settings=ChatSettings(name="Team Chat"), messages=[
            Message(sender="Charlie", message="Team meeting at 2 PM", timestamp=base_time + timedelta(days=2)),


            Message(sender="David", message="I'll be there!", timestamp=base_time + timedelta(days=2, minutes=5)),
            Message(sender="user", message="Thanks for the reminder", timestamp=base_time + timedelta(days=2, minutes=10)),
        ]),
        Chat(settings=ChatSettings(name="Project Discussion"), messages=[
            Message(sender="Eve", message="How's the progress on the new feature?", timestamp=base_time + timedelta(days=3)),
            Message(sender="user", message="Almost done! Just fixing some bugs.", timestamp=base_time + timedelta(days=3, minutes=1)),


            Message(sender="Eve", message="Great! Let me know when it's ready for review.", timestamp=base_time + timedelta(days=3, minutes=2)),
        ]),
    ]



    return ChatStore(chats=mock_chats, active_chat="Alice")

# Current active chat (for demo purposes)
active_chat = "Alice" 