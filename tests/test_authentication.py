"""
Tests for the authentication system
"""
import unittest
from datetime import datetime
from app.security.authentication_system import AuthenticationSystem
from app.ai.ai_engine import AIEngine
from app.models.user_database import UserDatabase


class TestAuthentication(unittest.TestCase):
    """Test cases for the authentication system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.auth_system = AuthenticationSystem()
        self.ai_engine = AIEngine()
        self.user_db = UserDatabase("tests/test_data.json")
        
        # Create a test user
        self.test_user_id = 9999
        self.test_user_data = {
            "username": "test_user",
            "password_hash": b"fake_hash",
            "password_salt": b"fake_salt",
            "face_data": "test_face_data",
            "typing_pattern": "test_typing_pattern",
            "email": "test@example.com",
            "phone": "+1234567890",
            "balance": 1000.0
        }
        
        # Add test user to database
        self.user_db.add_user(self.test_user_id, self.test_user_data)
        
        # Add a trusted device
        self.user_db.add_trusted_device(self.test_user_id, "Test Device")
        
        # Add some login history
        self.user_db.add_login_record(self.test_user_id, {
            "timestamp": datetime.now().isoformat(),
            "device_info": "Test Device",
            "location": "48.8566,2.3522",  # Paris coordinates
            "ip_address": "192.168.1.1",
            "success": True
        })
    
    def tearDown(self):
        """Clean up after tests"""
        # In a real test, we would clean up the test database
        pass
    
    def test_authentication_success(self):
        """Test successful authentication"""
        # Create login data
        login_data = {
            "username": "test_user",
            "password": "test_password",
            "device_info": "Test Device",
            "location": "48.8566,2.3522",  # Paris coordinates
            "ip_address": "192.168.1.1",
            "face_data": "test_face_data",
            "typing_pattern": "test_typing_pattern"
        }
        
        # Authenticate
        result, details = self.auth_system.authenticate(login_data)
        
        # In a real test, we would check the actual authentication
        # Here we're just testing the interface
        self.assertIsInstance(result, bool)
        self.assertIsInstance(details, dict)
        self.assertIn("risk_level", details)
    
    def test_risk_evaluation(self):
        """Test risk evaluation"""
        # Create login data with missing biometric data
        login_data = {
            "username": "test_user",
            "password": "test_password",
            "device_info": "Test Device",
            "location": "48.8566,2.3522",  # Paris coordinates
            "ip_address": "192.168.1.1"
            # Missing face_data and typing_pattern
        }
        
        # Evaluate risk
        risk_level = self.auth_system.evaluate_risk(login_data)
        
        # Risk should be higher due to missing biometric data
        self.assertGreater(risk_level, 0.0)
        self.assertLessEqual(risk_level, 1.0)
        self.assertGreaterEqual(len(self.auth_system.risk_factors), 1)
    
    def test_ai_verification(self):
        """Test AI verification functions"""
        # Test face verification
        face_result, face_confidence = self.ai_engine.verify_face(
            "test_face_data", "test_face_data"
        )
        self.assertIsInstance(face_result, bool)
        self.assertIsInstance(face_confidence, float)
        
        # Test typing pattern analysis
        typing_result, typing_confidence = self.ai_engine.analyze_typing(
            "test_typing_pattern", "test_typing_pattern"
        )
        self.assertIsInstance(typing_result, bool)
        self.assertIsInstance(typing_confidence, float)
        
        # Test location verification
        location_result, location_risk = self.ai_engine.verify_location(
            "48.8566,2.3522", ["48.8566,2.3522"]
        )
        self.assertIsInstance(location_result, bool)
        self.assertIsInstance(location_risk, float)
        
        # Test device verification
        device_result, device_risk = self.ai_engine.verify_device(
            "Test Device", ["Test Device"]
        )
        self.assertIsInstance(device_result, bool)
        self.assertIsInstance(device_risk, float)
    
    def test_user_database(self):
        """Test user database functions"""
        # Get user details
        user_data = self.user_db.get_user_detail(self.test_user_id)
        self.assertIsNotNone(user_data)
        self.assertEqual(user_data["username"], "test_user")
        
        # Compare with current
        current_data = {
            "device_info": "Test Device",
            "location": "48.8566,2.3522"
        }
        comparison = self.user_db.compare_with_current(self.test_user_id, current_data)
        self.assertIsInstance(comparison, dict)
        self.assertIn("anomalies", comparison)


if __name__ == "__main__":
    unittest.main()
