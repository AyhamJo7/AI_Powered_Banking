"""
LoginInterface class for the banking system
"""
from typing import Dict, Any, Optional


class LoginInterface:
    """
    LoginInterface class providing the interface for user authentication
    
    Attributes:
        session_id (int): Unique identifier for the login session
    """
    
    def __init__(self, session_id: int):
        """
        Initialize a new LoginInterface instance
        
        Args:
            session_id: Unique identifier for the login session
        """
        self.session_id = session_id
    
    def collect_input(self) -> Dict[str, Any]:
        """
        Collect user input for authentication
        
        Returns:
            Dict[str, Any]: Dictionary containing user credentials and biometric data
        """
        # In a real implementation, this would collect username, password,
        # and potentially biometric data from the user interface
        print(f"Collecting user input for session {self.session_id}")
        
        # Simulated user input
        return {
            "username": "user123",
            "password": "password123",
            "face_data": "base64_encoded_face_image",
            "typing_pattern": "keystroke_timing_data",
            "ip_address": "192.168.1.1",
            "device_info": "Windows 11, Chrome 98.0.4758.102",
            "location": "48.8566,2.3522"  # Paris coordinates
        }
    
    def send_to_authentication(self, auth_data: Dict[str, Any]) -> bool:
        """
        Send collected authentication data to the authentication system
        
        Args:
            auth_data: Dictionary containing authentication data
            
        Returns:
            bool: True if authentication data was successfully sent, False otherwise
        """
        # In a real implementation, this would send the data to the AuthenticationSystem
        print(f"Sending authentication data for session {self.session_id} to authentication system")
        
        # Log the keys of the data being sent (not the values for security)
        print(f"Data includes: {', '.join(auth_data.keys())}")
        
        return True
    
    def get_session_status(self) -> Dict[str, Any]:
        """
        Get the current status of the login session
        
        Returns:
            Dict[str, Any]: Dictionary containing session status information
        """
        return {
            "session_id": self.session_id,
            "status": "active",
            "last_activity": "2025-05-16T16:28:00Z",
            "authentication_level": "multi-factor"
        }
    
    def __str__(self) -> str:
        """String representation of the LoginInterface"""
        return f"LoginInterface(session_id={self.session_id})"
