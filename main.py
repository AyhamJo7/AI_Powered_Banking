"""
AI-Powered Autonomous & Secure Banking System
Main application entry point
"""
import os
import time
from datetime import datetime
from typing import Dict, Any, List

# Import core components
from app.models.customer import Customer
from app.interfaces.login_interface import LoginInterface
from app.security.authentication_system import AuthenticationSystem
from app.ai.ai_engine import AIEngine
from app.models.user_database import UserDatabase
from app.security.proactive_defense_system import ProactiveDefenseSystem
from app.models.transaction import Transaction
from app.utils.encryption import hash_password, verify_password, generate_token

# Import configuration
from config.settings import get_config


def setup_demo_data(user_db: UserDatabase) -> Dict[int, Dict[str, Any]]:
    """
    Set up demo data for the banking system
    
    Args:
        user_db: UserDatabase instance
        
    Returns:
        Dict[int, Dict[str, Any]]: Dictionary of demo users
    """
    print("\n=== Setting up demo data ===")
    
    # Create demo users
    demo_users = {
        1001: {
            "username": "angel_abubakar",   
            "password": "Password@123",
            "face_data": "base64_encoded_face_data_for_angel",
            "typing_pattern": "angel_typing_pattern_data",
            "email": "angel_abubakar@gmail.com",
            "phone": "+963123456789",
            "balance": 5000.0
        },
        1002: {
            "username": "ahmad_ali",
            "password": "Password@456",
            "face_data": "base64_encoded_sface_data_for_ahmad",
            "typing_pattern": "ahmad_typing_pattern_data",
            "email": "ahmad.ali@hotmail.com",
            "phone": "+963123456780",
            "balance": 7500.0
        }
    }
    
    # Add users to database
    for user_id, user_data in demo_users.items():
        # Hash the password before storing
        password = user_data.pop("password")
        password_hash, salt = hash_password(password)
        user_data["password_hash"] = password_hash
        user_data["password_salt"] = salt
        
        # Add user to database
        user_db.add_user(user_id, user_data)
        print(f"Added demo user: {user_data['username']} (ID: {user_id})")
        
        # Add a trusted device
        user_db.add_trusted_device(user_id, "Windows 11, Chrome 98.0.4758.102")
        
        # Add some login history
        for _ in range(3):
            user_db.add_login_record(user_id, {
                "timestamp": datetime.now().isoformat(),
                "device_info": "Windows 11, Chrome 98.0.4758.102",
                "location": "33.5102,36.29128",  # Damascus coordinates
                "ip_address": "192.168.1.1",
                "success": True
            })
    
    return demo_users


def simulate_login(user_id: int, username: str, password: str, is_legitimate: bool = True) -> None:
    """
    Simulate a login attempt
    
    Args:
        user_id: User ID
        username: Username
        password: Password
        is_legitimate: Whether this is a legitimate login attempt
    """
    print(f"\n=== Simulating {'legitimate' if is_legitimate else 'suspicious'} login for {username} ===")
    
    # Create components
    session_id = int(time.time())
    login_interface = LoginInterface(session_id)
    auth_system = AuthenticationSystem()
    ai_engine = AIEngine()
    user_db = UserDatabase()
    
    # Get user data
    user_data = user_db.get_user_detail(user_id)
    if not user_data:
        print(f"User {username} not found")
        return
    
    # Collect login input
    print("Collecting login input...")
    login_input = login_interface.collect_input()
    
    # Override with provided credentials
    login_input["username"] = username
    login_input["password"] = password
    
    # If simulating suspicious login, modify some data
    if not is_legitimate:
        login_input["device_info"] = "Unknown Device"
        login_input["location"] = "1.2921,36.8219"  # Nairobi coordinates
        login_input["ip_address"] = "203.0.113.42"  # Example suspicious IP
    
    # Send to authentication
    print("Sending to authentication system...")
    login_interface.send_to_authentication(login_input)
    
    # Perform authentication
    auth_result, auth_details = auth_system.authenticate(login_input)
    
    # Verify biometric data if available
    verification_results = {}
    if "face_data" in login_input and "stored_face" in user_data:
        print("Verifying facial data...")
        face_result, face_confidence = ai_engine.verify_face(
            login_input["face_data"], user_data["stored_face"]
        )
        verification_results["face"] = (face_result, face_confidence)
    
    if "typing_pattern" in login_input and "stored_typing_pattern" in user_data:
        print("Analyzing typing pattern...")
        typing_result, typing_confidence = ai_engine.analyze_typing(
            login_input["typing_pattern"], user_data["stored_typing_pattern"]
        )
        verification_results["typing"] = (typing_result, typing_confidence)
    
    if "location" in login_input and "historical_logins" in user_data:
        print("Verifying location...")
        historical_locations = [
            login.get("location", "") 
            for login in user_data.get("historical_logins", [])
            if "location" in login
        ]
        location_result, location_risk = ai_engine.verify_location(
            login_input["location"], historical_locations
        )
        verification_results["location"] = (location_result, location_risk)
    
    if "device_info" in login_input and "trusted_devices" in user_data:
        print("Verifying device...")
        device_result, device_risk = ai_engine.verify_device(
            login_input["device_info"], user_data.get("trusted_devices", [])
        )
        verification_results["device"] = (device_result, device_risk)
    
    # Calculate overall risk
    risk_level = ai_engine.predict_risk_level(verification_results)
    print(f"Calculated risk level: {risk_level:.2f}")
    
    # Compare with historical patterns
    comparison = user_db.compare_with_current(user_id, login_input)
    if comparison.get("anomalies"):
        print(f"Detected anomalies: {', '.join(comparison.get('anomalies', []))}")
    
    # Determine authentication result
    if auth_result and risk_level < 0.5:
        print(f"Login successful for {username}")
        
        # Record successful login
        user_db.add_login_record(user_id, {
            "timestamp": datetime.now().isoformat(),
            "device_info": login_input.get("device_info", "Unknown"),
            "location": login_input.get("location", "Unknown"),
            "ip_address": login_input.get("ip_address", "Unknown"),
            "success": True,
            "risk_level": risk_level
        })
        
        # Add device to trusted devices if not already trusted
        if "device_info" in login_input and login_input["device_info"] not in user_data.get("trusted_devices", []):
            user_db.add_trusted_device(user_id, login_input["device_info"])
            print(f"Added {login_input['device_info']} to trusted devices")
    
    elif auth_result and 0.5 <= risk_level < 0.7:
        print(f"Login requires additional verification for {username}")
        print("Sending additional verification request...")
        auth_system.request_additional_verification("sms")
    
    else:
        print(f"Login denied for {username}")
        
        # Record failed login
        user_db.add_login_record(user_id, {
            "timestamp": datetime.now().isoformat(),
            "device_info": login_input.get("device_info", "Unknown"),
            "location": login_input.get("location", "Unknown"),
            "ip_address": login_input.get("ip_address", "Unknown"),
            "success": False,
            "risk_level": risk_level
        })
        
        # Check for potential threat
        defense_system = ProactiveDefenseSystem()
        activity_data = {
            "login_attempts": 1,
            "username": username,
            "ip_address": login_input.get("ip_address", "Unknown"),
            "device_info": login_input.get("device_info", "Unknown"),
            "location": login_input.get("location", "Unknown"),
            "risk_level": risk_level
        }
        
        threat_detected, threat_info = defense_system.detect_threat(activity_data)
        if threat_detected:
            print(f"Threat detected: {threat_info.get('threat_details', {}).get('type', 'Unknown')}")
            print(f"Response plan: {threat_info.get('response_plan', 'Unknown')}")
            
            # Block access if high risk
            if risk_level > 0.8:
                defense_system.block_access({
                    "ip_address": login_input.get("ip_address", "Unknown"),
                    "reason": "High risk login attempt"
                })
                print(f"Blocked access from IP: {login_input.get('ip_address', 'Unknown')}")
            
            # Alert security team
            defense_system.alert_security_team({
                "message": f"Suspicious login attempt for user {username}",
                "risk_level": risk_level,
                "details": login_input
            })
            print("Security team alerted")


def simulate_transaction(sender_id: int, receiver_id: int, amount: float, is_legitimate: bool = True) -> None:
    """
    Simulate a financial transaction
    
    Args:
        sender_id: Sender's user ID
        receiver_id: Receiver's user ID
        amount: Transaction amount
        is_legitimate: Whether this is a legitimate transaction
    """
    print(f"\n=== Simulating {'legitimate' if is_legitimate else 'suspicious'} transaction ===")
    
    # Create components
    user_db = UserDatabase()
    ai_engine = AIEngine()
    defense_system = ProactiveDefenseSystem()
    
    # Get user data
    sender_data = user_db.get_user_detail(sender_id)
    receiver_data = user_db.get_user_detail(receiver_id)
    
    if not sender_data or not receiver_data:
        print("Sender or receiver not found")
        return
    
    # Create transaction
    transaction = Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        description=f"Payment from {sender_data['username']} to {receiver_data['username']}"
    )
    
    print(f"Transaction created: {transaction}")
    print(f"Amount: ${amount:.2f}")
    
    # If simulating suspicious transaction, modify amount
    if not is_legitimate:
        # Make it a very large amount
        transaction.amount = 50000.0
        print(f"Modified amount to: ${transaction.amount:.2f}")
    
    # Check if sender has sufficient balance
    if transaction.amount > sender_data.get("balance", 0):
        print("Insufficient balance")
        transaction.fail("Insufficient balance")
        return
    
    # Check transaction against security settings
    security_settings = get_config("security")
    suspicious_threshold = security_settings.get("suspicious_transaction_threshold", 5000)
    
    # Analyze transaction risk
    risk_factors = []
    risk_score = 0.0
    
    # Check amount against threshold
    if transaction.amount > suspicious_threshold:
        risk_factors.append("Large transaction amount")
        risk_score += 0.3
    
    # Check if receiver is new (not in historical transactions)
    # In a real system, we would check the sender's transaction history
    if not is_legitimate:
        risk_factors.append("New receiver")
        risk_score += 0.2
    
    # Check for unusual time
    current_hour = datetime.now().hour
    if 1 <= current_hour <= 4:  # Unusual hours
        risk_factors.append("Unusual transaction time")
        risk_score += 0.2
    
    # Check for unusual location (if available)
    # In a real system, we would compare with the user's usual transaction locations
    
    # Detect potential threat
    activity_data = {
        "transaction": transaction.to_dict(),
        "risk_factors": risk_factors,
        "risk_score": risk_score
    }
    
    threat_detected, threat_info = defense_system.detect_threat(activity_data)
    
    # Process transaction based on risk assessment
    if risk_score > 0.7 or threat_detected:
        print(f"High risk transaction detected (score: {risk_score:.2f})")
        print(f"Risk factors: {', '.join(risk_factors)}")
        
        if threat_detected:
            print(f"Threat detected: {threat_info.get('threat_details', {}).get('type', 'Unknown')}")
            print(f"Response plan: {threat_info.get('response_plan', 'Unknown')}")
        
        # Flag transaction for review
        transaction.flag_for_review(risk_score)
        print("Transaction flagged for review")
        
        # Alert security team for high-risk transactions
        if risk_score > 0.8:
            defense_system.alert_security_team({
                "message": "High-risk transaction detected",
                "transaction_id": transaction.transaction_id,
                "risk_score": risk_score,
                "risk_factors": risk_factors
            })
            print("Security team alerted")
    
    elif 0.4 < risk_score <= 0.7:
        print(f"Medium risk transaction detected (score: {risk_score:.2f})")
        print(f"Risk factors: {', '.join(risk_factors)}")
        
        # In a real system, we would request additional verification
        print("Requesting additional verification from user")
        
        # For demo purposes, we'll complete the transaction
        transaction.complete()
        print("Transaction completed after verification")
    
    else:
        print(f"Low risk transaction (score: {risk_score:.2f})")
        
        # Complete the transaction
        transaction.complete()
        print("Transaction completed successfully")
    
    # Update transaction status
    print(f"Final transaction status: {transaction.status}")


def run_security_scan() -> None:
    """Run a comprehensive security scan"""
    print("\n=== Running Security Scan ===")
    
    defense_system = ProactiveDefenseSystem()
    scan_results = defense_system.run_security_scan()
    
    print(f"Scan completed at: {scan_results['scan_time']}")
    print(f"Vulnerabilities found: {scan_results['vulnerabilities_found']}")
    print(f"Suspicious patterns: {scan_results['suspicious_patterns']}")
    print(f"Current threat level: {scan_results['threat_level']}")
    print(f"Response plan: {scan_results['response_plan']}")


def main() -> None:
    """Main application entry point"""
    print("=" * 80)
    print("AI-POWERED AUTONOMOUS & SECURE BANKING SYSTEM")
    print("=" * 80)
    
    # Initialize database
    user_db = UserDatabase()
    
    # Set up demo data
    demo_users = setup_demo_data(user_db)
    
    # Simulate legitimate login
    user_id = 1001
    username = demo_users[user_id]["username"]
    password = "SecureP@ss123"  # Original password before hashing
    simulate_login(user_id, username, password, is_legitimate=True)
    
    # Simulate suspicious login
    simulate_login(user_id, username, password, is_legitimate=False)
    
    # Simulate legitimate transaction
    simulate_transaction(1001, 1002, 500.0, is_legitimate=True)
    
    # Simulate suspicious transaction
    simulate_transaction(1001, 1002, 500.0, is_legitimate=False)
    
    # Run security scan
    run_security_scan()
    
    print("\n" + "=" * 80)
    print("DEMO COMPLETED")
    print("=" * 80)


if __name__ == "__main__":
    main()
