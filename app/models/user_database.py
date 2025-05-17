"""
UserDatabase class for the banking system
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import os
import base64


class UserDatabase:
    """
    UserDatabase class for storing and retrieving user data
    
    Attributes:
        stored_face (str): Stored facial biometric data
        stored_typing_pattern (str): Stored typing pattern data
        trusted_devices (List[str]): List of trusted devices
        historical_logins (List[Dict]): List of historical login data
    """
    
    def __init__(self, data_file: str = "data/user_data.json"):
        """
        Initialize a new UserDatabase instance
        
        Args:
            data_file: Path to the data file
        """
        self.data_file = data_file
        self.users = {}
        self.stored_face = {}
        self.stored_typing_pattern = {}
        self.trusted_devices = {}
        self.historical_logins = {}
        
        # Load data if file exists
        self._load_data()
    
    def _load_data(self) -> None:
        """Load user data from file if it exists"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.users = data.get('users', {})
                    self.stored_face = data.get('stored_face', {})
                    self.stored_typing_pattern = data.get('stored_typing_pattern', {})
                    self.trusted_devices = data.get('trusted_devices', {})
                    self.historical_logins = data.get('historical_logins', {})
                    
                    # Convert base64 encoded binary data back to bytes
                    for user_id, user_data in self.users.items():
                        if 'password_hash_b64' in user_data:
                            user_data['password_hash'] = base64.b64decode(user_data['password_hash_b64'])
                            del user_data['password_hash_b64']
                        if 'password_salt_b64' in user_data:
                            user_data['password_salt'] = base64.b64decode(user_data['password_salt_b64'])
                            del user_data['password_salt_b64']
                
                print(f"Loaded user data from {self.data_file}")
            else:
                print(f"Data file {self.data_file} does not exist, starting with empty database")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def _save_data(self) -> None:
        """Save user data to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            # Create a copy of the data to modify for saving
            users_for_json = {}
            for user_id, user_data in self.users.items():
                # Create a copy of the user data
                user_copy = user_data.copy()
                
                # Convert bytes to base64 for JSON serialization
                if 'password_hash' in user_copy and isinstance(user_copy['password_hash'], bytes):
                    user_copy['password_hash_b64'] = base64.b64encode(user_copy['password_hash']).decode('utf-8')
                    del user_copy['password_hash']
                
                if 'password_salt' in user_copy and isinstance(user_copy['password_salt'], bytes):
                    user_copy['password_salt_b64'] = base64.b64encode(user_copy['password_salt']).decode('utf-8')
                    del user_copy['password_salt']
                
                users_for_json[user_id] = user_copy
            
            with open(self.data_file, 'w') as f:
                json.dump({
                    'users': users_for_json,
                    'stored_face': self.stored_face,
                    'stored_typing_pattern': self.stored_typing_pattern,
                    'trusted_devices': self.trusted_devices,
                    'historical_logins': self.historical_logins
                }, f, indent=2)
            print(f"Saved user data to {self.data_file}")
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """
        Add a new user to the database
        
        Args:
            user_id: Unique identifier for the user
            user_data: Dictionary containing user data
            
        Returns:
            bool: True if user was added successfully, False otherwise
        """
        if str(user_id) in self.users:
            print(f"User {user_id} already exists")
            return False
        
        self.users[str(user_id)] = user_data
        
        # Initialize biometric data if provided
        if 'face_data' in user_data:
            self.stored_face[str(user_id)] = user_data['face_data']
        
        if 'typing_pattern' in user_data:
            self.stored_typing_pattern[str(user_id)] = user_data['typing_pattern']
        
        # Initialize empty lists for devices and logins
        self.trusted_devices[str(user_id)] = []
        self.historical_logins[str(user_id)] = []
        
        self._save_data()
        return True
    
    def get_user_detail(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user details from the database
        
        Args:
            user_id: Unique identifier for the user
            
        Returns:
            Optional[Dict[str, Any]]: User data if found, None otherwise
        """
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            print(f"User {user_id} not found")
            return None
        
        # Combine all user data
        user_data = self.users[user_id_str].copy()
        
        # Add biometric data
        if user_id_str in self.stored_face:
            user_data['stored_face'] = self.stored_face[user_id_str]
        
        if user_id_str in self.stored_typing_pattern:
            user_data['stored_typing_pattern'] = self.stored_typing_pattern[user_id_str]
        
        # Add trusted devices and login history
        if user_id_str in self.trusted_devices:
            user_data['trusted_devices'] = self.trusted_devices[user_id_str]
        
        if user_id_str in self.historical_logins:
            user_data['historical_logins'] = self.historical_logins[user_id_str]
        
        return user_data
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> bool:
        """
        Update user data in the database
        
        Args:
            user_id: Unique identifier for the user
            user_data: Dictionary containing updated user data
            
        Returns:
            bool: True if user was updated successfully, False otherwise
        """
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            print(f"User {user_id} not found")
            return False
        
        # Update user data
        self.users[user_id_str].update(user_data)
        
        # Update biometric data if provided
        if 'face_data' in user_data:
            self.stored_face[user_id_str] = user_data['face_data']
        
        if 'typing_pattern' in user_data:
            self.stored_typing_pattern[user_id_str] = user_data['typing_pattern']
        
        self._save_data()
        return True
    
    def add_login_record(self, user_id: int, login_data: Dict[str, Any]) -> bool:
        """
        Add a login record to the user's history
        
        Args:
            user_id: Unique identifier for the user
            login_data: Dictionary containing login data
            
        Returns:
            bool: True if record was added successfully, False otherwise
        """
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            print(f"User {user_id} not found")
            return False
        
        # Ensure login_data has a timestamp
        if 'timestamp' not in login_data:
            login_data['timestamp'] = datetime.now().isoformat()
        
        # Add login record
        if user_id_str not in self.historical_logins:
            self.historical_logins[user_id_str] = []
        
        self.historical_logins[user_id_str].append(login_data)
        
        self._save_data()
        return True
    
    def add_trusted_device(self, user_id: int, device_info: str) -> bool:
        """
        Add a trusted device for the user
        
        Args:
            user_id: Unique identifier for the user
            device_info: Information about the device
            
        Returns:
            bool: True if device was added successfully, False otherwise
        """
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            print(f"User {user_id} not found")
            return False
        
        # Initialize trusted devices list if it doesn't exist
        if user_id_str not in self.trusted_devices:
            self.trusted_devices[user_id_str] = []
        
        # Add device if not already trusted
        if device_info not in self.trusted_devices[user_id_str]:
            self.trusted_devices[user_id_str].append(device_info)
            self._save_data()
        
        return True
    
    def compare_with_current(self, user_id: int, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare current login data with historical patterns
        
        Args:
            user_id: Unique identifier for the user
            current_data: Dictionary containing current login data
            
        Returns:
            Dict[str, Any]: Comparison results
        """
        user_id_str = str(user_id)
        if user_id_str not in self.users:
            print(f"User {user_id} not found")
            return {"error": "User not found", "anomalies": []}
        
        anomalies = []
        
        # Check if device is trusted
        if 'device_info' in current_data:
            device_trusted = False
            if user_id_str in self.trusted_devices:
                device_trusted = any(current_data['device_info'] in device 
                                    for device in self.trusted_devices[user_id_str])
            
            if not device_trusted:
                anomalies.append("Untrusted device")
        
        # Check if location matches historical patterns
        if 'location' in current_data and user_id_str in self.historical_logins:
            location_matches = False
            for login in self.historical_logins[user_id_str]:
                if 'location' in login and login['location'] == current_data['location']:
                    location_matches = True
                    break
            
            if not location_matches and len(self.historical_logins[user_id_str]) > 0:
                anomalies.append("Unusual location")
        
        # Check login time pattern
        if user_id_str in self.historical_logins and len(self.historical_logins[user_id_str]) > 0:
            current_time = datetime.now()
            current_hour = current_time.hour
            
            # Count logins by hour
            hour_counts = {}
            for login in self.historical_logins[user_id_str]:
                if 'timestamp' in login:
                    try:
                        login_time = datetime.fromisoformat(login['timestamp'])
                        hour = login_time.hour
                        hour_counts[hour] = hour_counts.get(hour, 0) + 1
                    except (ValueError, TypeError):
                        pass
            
            # Check if current hour is common
            if hour_counts and current_hour in hour_counts:
                if hour_counts[current_hour] < 2:  # Less than 2 logins at this hour
                    anomalies.append("Unusual login time")
        
        return {
            "user_id": user_id,
            "anomalies": anomalies,
            "anomaly_count": len(anomalies),
            "is_suspicious": len(anomalies) > 1
        }
    
    def __str__(self) -> str:
        """String representation of the UserDatabase"""
        return f"UserDatabase(users={len(self.users)})"
