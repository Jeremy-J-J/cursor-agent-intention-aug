#!/usr/bin/env python3
"""
Test file for UserRepository implementation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'examples', 'demo_project'))

from src.repositories.user_repository import UserRepository
from database import Database
from models.user import User

def test_get_user_by_id():
    """Test the get_user_by_id method."""
    
    # Create a mock database
    db = Database("sqlite:///test.db")
    
    # Create a test user
    test_user = User(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    
    # Save the user to database
    db.save_user(test_user)
    
    # Create repository instance
    repo = UserRepository(db)
    
    # Test retrieving existing user
    user = repo.get_user_by_id("testuser")
    assert user is not None
    assert user.username == "testuser"
    print("✓ Successfully retrieved existing user")
    
    # Test retrieving non-existing user
    user = repo.get_user_by_id("nonexistent")
    assert user is None
    print("✓ Correctly returned None for non-existing user")
    
    # Test with empty ID
    try:
        repo.get_user_by_id("")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Correctly handled empty user ID")
    
    print("All tests passed!")

if __name__ == "__main__":
    test_get_user_by_id()