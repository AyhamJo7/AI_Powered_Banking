"""
Customer class for the banking system
"""
from typing import Optional


class Customer:
    """
    Customer class representing a bank customer
    
    Attributes:
        customer_id (int): Unique identifier for the customer
        username (str): Customer's username
        password (str): Customer's password (should be encrypted in production)
        face_data (str): Customer's facial biometric data
        typing_pattern (str): Customer's typing pattern for keystroke dynamics
    """
    
    def __init__(self, customer_id: int, username: str, password: str, 
                 face_data: Optional[str] = None, typing_pattern: Optional[str] = None):
        """
        Initialize a new Customer instance
        
        Args:
            customer_id: Unique identifier for the customer
            username: Customer's username
            password: Customer's password
            face_data: Customer's facial biometric data (optional)
            typing_pattern: Customer's typing pattern (optional)
        """
        self.customer_id = customer_id
        self.username = username
        self.password = password
        self.face_data = face_data
        self.typing_pattern = typing_pattern
    
    def login(self) -> bool:
        """
        Attempt to log in the customer
        
        Returns:
            bool: True if login successful, False otherwise
        """
        # In a real implementation, this would interact with the LoginInterface
        # and AuthenticationSystem classes
        print(f"Customer {self.username} attempting to login")
        return True
    
    def request_access(self, resource: str) -> bool:
        """
        Request access to a specific resource
        
        Args:
            resource: The resource to access
            
        Returns:
            bool: True if access granted, False otherwise
        """
        # In a real implementation, this would check permissions and
        # potentially trigger additional authentication
        print(f"Customer {self.username} requesting access to {resource}")
        return True
    
    def __str__(self) -> str:
        """String representation of the Customer"""
        return f"Customer(id={self.customer_id}, username={self.username})"
