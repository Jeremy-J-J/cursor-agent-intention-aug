#!/usr/bin/env python3
"""
Simple token manager for handling conversation token counts.
This is a minimal implementation focused on core functionality.
"""

import tiktoken
from typing import List, Dict, Any
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleTokenManager:
    """
    Simple token manager for basic token counting operations.
    """
    
    def __init__(self, model: str = "gpt-4"):
        """
        Initialize the token manager.
        
        Args:
            model: OpenAI model name to use for token encoding
        """
        self.model = model
        try:
            self.tokenizer = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base if model is not recognized
            logger.warning(f"Model {model} not found, using cl100k_base")
            self.tokenizer = tiktoken.get_encoding("cl100k_base")
    
    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a text string.
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Number of tokens in the text
        """
        if not text:
            return 0
        return len(self.tokenizer.encode(text))
    
    def count_message_tokens(self, message: Dict[str, Any]) -> int:
        """
        Count the number of tokens in a single message.
        
        Args:
            message: Message dictionary with 'role' and 'content' keys
            
        Returns:
            Number of tokens in the message
        """
        role_tokens = self.count_tokens(message.get('role', ''))
        content_tokens = self.count_tokens(message.get('content', ''))
        # Add overhead for message structure (approximate)
        return role_tokens + content_tokens + 3
    
    def count_conversation_tokens(self, conversation: List[Dict[str, Any]]) -> int:
        """
        Count the total number of tokens in a conversation.
        
        Args:
            conversation: List of message dictionaries
            
        Returns:
            Total number of tokens in the conversation
        """
        total_tokens = 0
        for message in conversation:
            total_tokens += self.count_message_tokens(message)
        return total_tokens