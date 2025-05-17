"""
Command-line interface for the banking system
"""
import argparse
import getpass
import sys
import time
from datetime import datetime

from app.models.customer import Customer
from app.interfaces.login_interface import LoginInterface
from app.security.authentication_system import AuthenticationSystem
from app.ai.ai_engine import AIEngine
from app.models.user_database import UserDatabase
from app.security.proactive_defense_system import ProactiveDefenseSystem
from app.models.transaction import Transaction
from app.utils.encryption import hash_password, verify_password, generate_token


def login(args):
    """Handle login command"""
    print("\n=== AI-Powered Secure Banking System - Login ===\n")
    
    # Get username and password
    username = args.username or input("Username: ")
    password = args.password or getpass.getpass("Password: ")
    
    # Create components
    session_id = int(time.time())
    login_interface = LoginInterface(session_id)
    auth_system = AuthenticationSystem()
    ai_engine = AIEngine()
    user_db = UserDatabase()
    
    # Find user by username
    user_found = False
    user_id = None
    
    # In a real system, we would look up the user by username
    # For demo purposes, we'll just check the demo users
    for uid in ["1001", "1002"]:
        user_data = user_db.get_user_detail(int(uid))
        if user_data and user_data.get("username") == username:
            user_found = True
            user_id = int(uid)
            break
    
    if not user_found:
        print(f"User {username} not found")
        return False
    
    # Collect login input
    print("Collecting login data...")
    login_input = login_interface.collect_input()
    
    # Override with provided credentials
    login_input["username"] = username
    login_input["password"] = password
    
    # Send to authentication
    print("Authenticating...")
    login_interface.send_to_authentication(login_input)
    
    # Perform authentication
    auth_result, auth_details = auth_system.authenticate(login_input)
    
    # Verify biometric data if available
    verification_results = {}
    user_data = user_db.get_user_detail(user_id)
    
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
    
    # Calculate overall risk
    risk_level = ai_engine.predict_risk_level(verification_results)
    print(f"Risk assessment: {risk_level:.2f}")
    
    # Determine authentication result
    if auth_result and risk_level < 0.5:
        print(f"\nLogin successful. Welcome, {username}!")
        
        # Record successful login
        user_db.add_login_record(user_id, {
            "timestamp": datetime.now().isoformat(),
            "device_info": login_input.get("device_info", "Unknown"),
            "location": login_input.get("location", "Unknown"),
            "ip_address": login_input.get("ip_address", "Unknown"),
            "success": True,
            "risk_level": risk_level
        })
        
        # Show account information
        print("\nAccount Information:")
        print(f"Balance: ${user_data.get('balance', 0):.2f}")
        print(f"Email: {user_data.get('email', 'Not provided')}")
        print(f"Phone: {user_data.get('phone', 'Not provided')}")
        
        return True
    
    elif auth_result and 0.5 <= risk_level < 0.7:
        print("\nAdditional verification required.")
        print("A verification code has been sent to your registered device.")
        
        # In a real system, we would send a verification code
        # For demo purposes, we'll just simulate it
        verification_code = "123456"
        entered_code = input("Enter verification code: ")
        
        if entered_code == verification_code:
            print(f"\nVerification successful. Welcome, {username}!")
            return True
        else:
            print("\nIncorrect verification code. Login failed.")
            return False
    
    else:
        print("\nLogin failed. Invalid credentials or high security risk.")
        return False


def transfer(args):
    """Handle transfer command"""
    print("\n=== AI-Powered Secure Banking System - Transfer ===\n")
    
    # Get transfer details
    sender_id = args.sender
    receiver_id = args.receiver
    amount = args.amount
    
    # Create components
    user_db = UserDatabase()
    ai_engine = AIEngine()
    defense_system = ProactiveDefenseSystem()
    
    # Get user data
    sender_data = user_db.get_user_detail(sender_id)
    receiver_data = user_db.get_user_detail(receiver_id)
    
    if not sender_data or not receiver_data:
        print("Sender or receiver not found")
        return False
    
    # Create transaction
    transaction = Transaction(
        sender_id=sender_id,
        receiver_id=receiver_id,
        amount=amount,
        description=f"Transfer from {sender_data['username']} to {receiver_data['username']}"
    )
    
    print(f"Transaction created: {transaction}")
    print(f"Amount: ${amount:.2f}")
    
    # Check if sender has sufficient balance
    if transaction.amount > sender_data.get("balance", 0):
        print("Insufficient balance")
        transaction.fail("Insufficient balance")
        return False
    
    # Process transaction
    print("Processing transaction...")
    
    # Analyze transaction risk
    risk_factors = []
    risk_score = 0.0
    
    # Check amount against threshold
    if transaction.amount > 5000:
        risk_factors.append("Large transaction amount")
        risk_score += 0.3
    
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
        
        # Ask for confirmation
        confirmation = input("This transaction has been flagged as high risk. Proceed? (y/n): ")
        if confirmation.lower() != 'y':
            print("Transaction cancelled")
            transaction.fail("User cancelled high-risk transaction")
            return False
        
        print("Proceeding with high-risk transaction...")
    
    # Complete the transaction
    transaction.complete()
    print("Transaction completed successfully")
    
    # Update balances (in a real system, this would be handled by a proper database)
    # This is just for demonstration purposes
    sender_data["balance"] = sender_data.get("balance", 0) - transaction.amount
    receiver_data["balance"] = receiver_data.get("balance", 0) + transaction.amount
    
    user_db.update_user(sender_id, {"balance": sender_data["balance"]})
    user_db.update_user(receiver_id, {"balance": receiver_data["balance"]})
    
    print(f"New balance for {sender_data['username']}: ${sender_data['balance']:.2f}")
    
    return True


def security_scan(args):
    """Handle security scan command"""
    print("\n=== AI-Powered Secure Banking System - Security Scan ===\n")
    
    defense_system = ProactiveDefenseSystem()
    scan_results = defense_system.run_security_scan()
    
    print(f"Scan completed at: {scan_results['scan_time']}")
    print(f"Vulnerabilities found: {scan_results['vulnerabilities_found']}")
    print(f"Suspicious patterns: {scan_results['suspicious_patterns']}")
    print(f"Current threat level: {scan_results['threat_level']}")
    print(f"Response plan: {scan_results['response_plan']}")
    
    return True


def main():
    """Main entry point for the CLI"""
    parser = argparse.ArgumentParser(description="AI-Powered Secure Banking System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Login command
    login_parser = subparsers.add_parser("login", help="Log in to the banking system")
    login_parser.add_argument("--username", help="Username")
    login_parser.add_argument("--password", help="Password (not recommended, use prompt instead)")
    
    # Transfer command
    transfer_parser = subparsers.add_parser("transfer", help="Transfer money")
    transfer_parser.add_argument("--sender", type=int, required=True, help="Sender ID")
    transfer_parser.add_argument("--receiver", type=int, required=True, help="Receiver ID")
    transfer_parser.add_argument("--amount", type=float, required=True, help="Amount to transfer")
    
    # Security scan command
    security_parser = subparsers.add_parser("scan", help="Run a security scan")
    
    args = parser.parse_args()
    
    if args.command == "login":
        login(args)
    elif args.command == "transfer":
        transfer(args)
    elif args.command == "scan":
        security_scan(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
