from textual.containers import ScrollableContainer
from rich.panel import Panel
from rich.text import Text
from rich.box import ROUNDED
from rich.console import Group
from datetime import datetime
from typing import List
from ..models.schema import Message
import json


class MessageView(ScrollableContainer):
    """A widget that displays chat messages."""
    
    def __init__(self):
        super().__init__()
        self.messages = []
    
    def update_messages(self, messages: List[Message]):
        """Update the messages displayed in the view."""
        self.messages = messages
        self.refresh()
    
    def render(self):
        """Render the messages with nice formatting."""
        message_panels = []
        
        for msg in self.messages:
            # Format timestamp
            timestamp = msg.timestamp
            time_str = timestamp.strftime("%H:%M")
            
            # Create message content with sender and time
            is_user = msg.sender == "user"
            
            # Choose colors based on sender
            style = "bold blue" if is_user else "bold green"
            align = "right" if is_user else "left"
            
            # Create the message content
            header = Text()
            header.append(f"{msg.sender} ", style=style)
            header.append(time_str, style="dim")
            
            content = Text(msg.message)
            
            # Group the header and content
            message_group = Group(header, content)
            
            # Create the message panel

            panel = Panel(
                message_group,
                box=ROUNDED,
                style="white on default",
                border_style=style,
                width=60,
                padding=(0, 1),
            )
            
            message_panels.append(panel)
        
        # If no messages, show a placeholder
        if not message_panels:
            return Text("No messages yet", style="dim")
        
        # Return all panels as a group
        return Group(*message_panels) 