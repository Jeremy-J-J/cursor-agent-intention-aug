#!/usr/bin/env python3
"""
User repository implementation for database operations.
"""

import logging
from typing import Optional
from src.models.user import User
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class UserRepository:
    """
    Repository class for user-related database operations.
    """

    def __init__(self, db: Session):
        """
        Initialize the UserRepository with a database session.
        
        Args:
            db: Database session to use for operations
        """
        self.db = db

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The unique identifier for the user
            
        Returns:
            User object if found, None otherwise
            
        Raises:
            Exception: If there's an error during database operation
        """
        try:
            logger.debug(f"Retrieving user with ID: {user_id}")
            
            # Validate input
            if not user_id:
                logger.error("User ID cannot be empty")
                raise ValueError("User ID cannot be empty")
            
            # Retrieve user from database
            user = self.db.query(User).filter(User.id == user_id).first()
            
            if user:
                logger.info(f"Successfully retrieved user: {user_id}")
            else:
                logger.info(f"No user found with ID: {user_id}")
                
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user with ID {user_id}: {str(e)}")
            raise

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        
        Args:
            username: The username to search for
            
        Returns:
            User object if found, None otherwise
            
        Raises:
            Exception: If there's an error during database operation
        """
        try:
            logger.debug(f"Retrieving user with username: {username}")
            
            # Validate input
            if not username:
                logger.error("Username cannot be empty")
                raise ValueError("Username cannot be empty")
            
            # Retrieve user from database
            user = self.db.query(User).filter(User.username == username).first()
            
            if user:
                logger.info(f"Successfully retrieved user: {username}")
            else:
                logger.info(f"No user found with username: {username}")
                
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user with username {username}: {str(e)}")
            raise
logger = logging.getLogger(__name__)

class UserRepository:
    """
    Repository class for user-related database operations.
    """

    def __init__(self, database: Database):
        """
        Initialize the UserRepository with a database instance.
        
        Args:
            database: Database instance to use for operations
        """
        self.database = database

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The unique identifier for the user
            
        Returns:
            User object if found, None otherwise
            
        Raises:
            Exception: If there's an error during database operation
        """
        try:
            logger.debug(f"Retrieving user with ID: {user_id}")
            
            # Validate input
            if not user_id:
                logger.error("User ID cannot be empty")
                raise ValueError("User ID cannot be empty")
            
            # Retrieve user from database
            user = self.database.get_user(user_id)
            
            if user:
                logger.info(f"Successfully retrieved user: {user_id}")
            else:
                logger.info(f"No user found with ID: {user_id}")
                
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user with ID {user_id}: {str(e)}")
            raise

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by their username.
        
        Args:
            username: The username to search for
            
        Returns:
            User object if found, None otherwise
            
        Raises:
            Exception: If there's an error during database operation
        """
        try:
            logger.debug(f"Retrieving user with username: {username}")
            
            # Validate input
            if not username:
                logger.error("Username cannot be empty")
                raise ValueError("Username cannot be empty")
            
            # Retrieve user from database
            user = self.database.get_user_by_username(username)
            
            if user:
                logger.info(f"Successfully retrieved user: {username}")
            else:
                logger.info(f"No user found with username: {username}")
                
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user with username {username}: {str(e)}")
            raise
logger = logging.getLogger(__name__)


class UserRepository:
    """
    Repository class for user-related database operations.
    """

    def __init__(self, database: Database):
        """
        Initialize the UserRepository with a database instance.
        
        Args:
            database: Database instance to use for operations
        """
        self.database = database

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The unique identifier for the user
            
        Returns:
            User object if found, None otherwise
            
        Raises:
            Exception: If there's an error during database operation
        """
        try:
            logger.debug(f"Retrieving user with ID: {user_id}")
            
            # Validate input
            if not user_id:
                logger.error("User ID cannot be empty")
                raise ValueError("User ID cannot be empty")
            
            # Retrieve user from database
            user = self.database.get_user(user_id)
            
            if user:
                logger.info(f"Successfully retrieved user: {user_id}")
            else:
                logger.info(f"No user found with ID: {user_id}")
                
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user with ID {user_id}: {str(e)}")
            raise