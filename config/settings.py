"""
Configuration settings for the banking system
"""
import os
from typing import Dict, Any

# Database settings
DATABASE_FILE = os.path.join("data", "user_data.json")

# Security settings
SECURITY_SETTINGS = {
    "password_min_length": 8,
    "password_require_uppercase": True,
    "password_require_lowercase": True,
    "password_require_number": True,
    "password_require_special": True,
    "max_login_attempts": 5,
    "lockout_duration_minutes": 30,
    "session_timeout_minutes": 15,
    "token_expiry_minutes": 60,
    "mfa_required": True,
    "biometric_verification_threshold": 0.8,
    "typing_pattern_verification_threshold": 0.75,
    "location_verification_enabled": True,
    "device_verification_enabled": True,
    "suspicious_transaction_threshold": 5000,
    "high_risk_countries": [
        "CountryA",
        "CountryB",
        "CountryC"
    ]
}

# AI Engine settings
AI_SETTINGS = {
    "face_recognition_model": "FaceNet_v2",
    "typing_pattern_model": "KeystrokeDynamics_v1",
    "location_model": "GeoVerify_v3",
    "risk_assessment_model": "RiskNet_v1",
    "anomaly_detection_threshold": 0.7,
    "continuous_learning_enabled": True,
    "update_frequency_days": 7
}

# Proactive Defense settings
DEFENSE_SETTINGS = {
    "threat_scan_interval_minutes": 60,
    "auto_block_suspicious_ips": True,
    "honeypot_enabled": True,
    "self_healing_enabled": True,
    "zero_trust_architecture": True,
    "adaptive_authentication": True,
    "threat_intelligence_feeds": [
        "feed1.example.com",
        "feed2.example.com"
    ]
}

# Notification settings
NOTIFICATION_SETTINGS = {
    "email_notifications_enabled": True,
    "sms_notifications_enabled": True,
    "push_notifications_enabled": True,
    "notify_on_login": True,
    "notify_on_password_change": True,
    "notify_on_large_transaction": True,
    "notify_on_suspicious_activity": True,
    "large_transaction_threshold": 1000
}

# Logging settings
LOGGING_SETTINGS = {
    "log_level": "INFO",
    "log_file": os.path.join("data", "banking.log"),
    "max_log_size_mb": 10,
    "backup_count": 5,
    "log_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# API settings
API_SETTINGS = {
    "rate_limit": 100,  # requests per minute
    "enable_cors": True,
    "allowed_origins": ["https://example.com"],
    "api_keys_enabled": True
}

# Get a specific configuration section
def get_config(section: str) -> Dict[str, Any]:
    """
    Get a specific configuration section
    
    Args:
        section: Name of the configuration section
        
    Returns:
        Dict[str, Any]: Configuration settings for the specified section
    """
    config_map = {
        "security": SECURITY_SETTINGS,
        "ai": AI_SETTINGS,
        "defense": DEFENSE_SETTINGS,
        "notification": NOTIFICATION_SETTINGS,
        "logging": LOGGING_SETTINGS,
        "api": API_SETTINGS
    }
    
    return config_map.get(section.lower(), {})
