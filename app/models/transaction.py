"""
Transaction class for the banking system
"""
from typing import Dict, Any, Optional
from datetime import datetime
import uuid


class Transaction:
    """
    Transaction class representing a financial transaction
    
    Attributes:
        transaction_id (str): Unique identifier for the transaction
        sender_id (int): ID of the sender
        receiver_id (int): ID of the receiver
        amount (float): Transaction amount
        timestamp (datetime): Time of the transaction
        status (str): Status of the transaction
        description (str): Description of the transaction
    """
    
    # Transaction status constants
    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"
    STATUS_BLOCKED = "blocked"
    STATUS_UNDER_REVIEW = "under_review"
    
    def __init__(self, sender_id: int, receiver_id: int, amount: float, 
                 description: str = "", transaction_id: Optional[str] = None):
        """
        Initialize a new Transaction instance
        
        Args:
            sender_id: ID of the sender
            receiver_id: ID of the receiver
            amount: Transaction amount
            description: Description of the transaction (optional)
            transaction_id: Unique identifier for the transaction (optional, generated if not provided)
        """
        self.transaction_id = transaction_id if transaction_id else str(uuid.uuid4())
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.amount = amount
        self.timestamp = datetime.now()
        self.status = self.STATUS_PENDING
        self.description = description
        self.risk_score = 0.0
        self.metadata = {}
    
    def complete(self) -> bool:
        """
        Mark the transaction as completed
        
        Returns:
            bool: True if status was updated successfully, False otherwise
        """
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_COMPLETED
            self.metadata["completed_at"] = datetime.now().isoformat()
            return True
        return False
    
    def fail(self, reason: str) -> bool:
        """
        Mark the transaction as failed
        
        Args:
            reason: Reason for failure
            
        Returns:
            bool: True if status was updated successfully, False otherwise
        """
        if self.status != self.STATUS_COMPLETED:
            self.status = self.STATUS_FAILED
            self.metadata["failed_at"] = datetime.now().isoformat()
            self.metadata["failure_reason"] = reason
            return True
        return False
    
    def block(self, reason: str) -> bool:
        """
        Block the transaction due to security concerns
        
        Args:
            reason: Reason for blocking
            
        Returns:
            bool: True if status was updated successfully, False otherwise
        """
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_BLOCKED
            self.metadata["blocked_at"] = datetime.now().isoformat()
            self.metadata["block_reason"] = reason
            return True
        return False
    
    def flag_for_review(self, risk_score: float) -> bool:
        """
        Flag the transaction for manual review
        
        Args:
            risk_score: Risk score for the transaction
            
        Returns:
            bool: True if status was updated successfully, False otherwise
        """
        if self.status == self.STATUS_PENDING:
            self.status = self.STATUS_UNDER_REVIEW
            self.risk_score = risk_score
            self.metadata["flagged_at"] = datetime.now().isoformat()
            self.metadata["risk_score"] = risk_score
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary
        
        Returns:
            Dict[str, Any]: Dictionary representation of the transaction
        """
        return {
            "transaction_id": self.transaction_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "amount": self.amount,
            "timestamp": self.timestamp.isoformat(),
            "status": self.status,
            "description": self.description,
            "risk_score": self.risk_score,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """
        Create a Transaction instance from a dictionary
        
        Args:
            data: Dictionary containing transaction data
            
        Returns:
            Transaction: New Transaction instance
        """
        transaction = cls(
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            amount=data["amount"],
            description=data.get("description", ""),
            transaction_id=data.get("transaction_id")
        )
        
        # Set additional attributes
        if "timestamp" in data:
            try:
                transaction.timestamp = datetime.fromisoformat(data["timestamp"])
            except (ValueError, TypeError):
                pass
        
        transaction.status = data.get("status", cls.STATUS_PENDING)
        transaction.risk_score = data.get("risk_score", 0.0)
        transaction.metadata = data.get("metadata", {})
        
        return transaction
    
    def __str__(self) -> str:
        """String representation of the Transaction"""
        return f"Transaction(id={self.transaction_id}, amount={self.amount}, status={self.status})"
