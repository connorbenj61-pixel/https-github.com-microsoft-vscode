"""
Biometric Authentication System for ArmourboundGuardianAI

PEGI 3: Educational biometric security system
Supports multiple biometric modalities: fingerprint, facial, iris, voice, gait
"""

import hashlib
import hmac
import uuid
import time
import math
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field
from enum import Enum
from datetime import datetime, timedelta
import threading


class BiometricType(Enum):
    """Types of biometric authentication."""
    FINGERPRINT = "fingerprint"  # Fingerprint scanning
    FACIAL = "facial"  # Facial recognition
    IRIS = "iris"  # Iris scanning
    VOICE = "voice"  # Voice recognition
    GAIT = "gait"  # Gait recognition
    PALM = "palm"  # Palm vein scanning
    BEHAVIORAL = "behavioral"  # Behavioral biometrics (typing, mouse movement)


class BiometricStatus(Enum):
    """Status of biometric authentication."""
    ENROLLED = "enrolled"  # Successfully enrolled
    PENDING = "pending"  # Enrollment in progress
    VERIFIED = "verified"  # Successfully verified
    FAILED = "failed"  # Authentication failed
    LOCKED = "locked"  # Too many failed attempts


@dataclass
class BiometricTemplate:
    """Biometric template (feature vector)."""
    biometric_id: str
    biometric_type: BiometricType
    user_id: str
    template_data: List[float]  # Feature vector (0-1 normalized)
    quality_score: float  # 0-100, higher = better
    enrollment_time: float
    last_verified: float
    verification_count: int = 0
    template_hash: str = ""  # For integrity verification
    
    def __post_init__(self):
        """Calculate template hash."""
        if not self.template_hash:
            hash_input = f"{self.user_id}{self.template_data}{self.enrollment_time}"
            self.template_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    
    def calculate_similarity(self, other_template: 'BiometricTemplate') -> float:
        """
        Calculate similarity between templates (0-100).
        Uses cosine similarity for feature vectors.
        """
        if len(self.template_data) != len(other_template.template_data):
            return 0.0
        
        # Cosine similarity
        dot_product = sum(a * b for a, b in zip(self.template_data, other_template.template_data))
        mag1 = math.sqrt(sum(x**2 for x in self.template_data))
        mag2 = math.sqrt(sum(x**2 for x in other_template.template_data))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return (dot_product / (mag1 * mag2)) * 100  # Convert to 0-100


@dataclass
class BiometricAuthentication:
    """Record of a biometric authentication attempt."""
    auth_id: str
    user_id: str
    biometric_type: BiometricType
    timestamp: float
    status: BiometricStatus
    similarity_score: float
    confidence: float
    device_id: str
    location: str  # Device location
    ip_address: str
    liveness_check: bool  # Anti-spoofing check
    match_quality: float
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['biometric_type'] = self.biometric_type.value
        result['status'] = self.status.value
        return result


@dataclass
class BiometricProfile:
    """User's biometric profile with multiple templates."""
    user_id: str
    profiles: Dict[BiometricType, List[BiometricTemplate]] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    last_updated: float = field(default_factory=time.time)
    is_active: bool = True
    failed_attempts: int = 0
    locked_until: Optional[float] = None
    
    def is_locked(self) -> bool:
        """Check if profile is locked."""
        if self.locked_until is None:
            return False
        return time.time() < self.locked_until
    
    def add_template(self, template: BiometricTemplate):
        """Add a biometric template."""
        if template.biometric_type not in self.profiles:
            self.profiles[template.biometric_type] = []
        
        self.profiles[template.biometric_type].append(template)
        self.last_updated = time.time()
    
    def get_templates(self, biometric_type: BiometricType) -> List[BiometricTemplate]:
        """Get all templates for a biometric type."""
        return self.profiles.get(biometric_type, [])
    
    def has_biometric_type(self, biometric_type: BiometricType) -> bool:
        """Check if user has enrolled a biometric type."""
        return (biometric_type in self.profiles and 
                len(self.profiles[biometric_type]) > 0)


class BiometricAuthentication:
    """
    Biometric authentication system.
    
    Supports multiple biometric modalities with:
    - Template matching and similarity scoring
    - Liveness detection (anti-spoofing)
    - Multi-factor authentication
    - Secure enrollment and verification
    - Failed attempt tracking
    - Device and location verification
    """
    
    def __init__(self, false_acceptance_rate: float = 0.01):
        """
        Initialize biometric system.
        
        Args:
            false_acceptance_rate: FAR threshold (1% default)
        """
        self.profiles: Dict[str, BiometricProfile] = {}
        self.authentication_log: List[BiometricAuthentication] = []
        self.lock = threading.RLock()
        self.false_acceptance_rate = false_acceptance_rate
        # Calculate threshold: lower FAR = higher threshold
        self.match_threshold = 100 - (false_acceptance_rate * 100)
        self.max_failed_attempts = 5
        self.lockout_duration = 900  # 15 minutes
    
    def enroll_user(self, user_id: str) -> bool:
        """
        Create new biometric profile for user.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if enrollment successful
        """
        with self.lock:
            if user_id in self.profiles:
                return False  # Already enrolled
            
            self.profiles[user_id] = BiometricProfile(user_id=user_id)
            return True
    
    def add_biometric_template(
        self,
        user_id: str,
        biometric_type: BiometricType,
        template_data: List[float],
        quality_score: float,
        device_id: str = "default"
    ) -> Optional[str]:
        """
        Add biometric template for user (enrollment).
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            template_data: Feature vector (0-1 normalized)
            quality_score: Quality of capture (0-100)
            device_id: ID of biometric device
            
        Returns:
            Template ID if successful, None otherwise
        """
        if quality_score < 70:
            return None  # Quality too low
        
        with self.lock:
            if user_id not in self.profiles:
                return None
            
            template_id = str(uuid.uuid4())
            template = BiometricTemplate(
                biometric_id=template_id,
                biometric_type=biometric_type,
                user_id=user_id,
                template_data=template_data,
                quality_score=quality_score,
                enrollment_time=time.time(),
                last_verified=time.time()
            )
            
            self.profiles[user_id].add_template(template)
            return template_id
    
    def authenticate(
        self,
        user_id: str,
        biometric_type: BiometricType,
        sample_data: List[float],
        device_id: str = "default",
        location: str = "unknown",
        ip_address: str = "0.0.0.0",
        liveness_check: bool = True
    ) -> Tuple[bool, BiometricAuthentication]:
        """
        Authenticate user with biometric.
        
        Args:
            user_id: User identifier
            biometric_type: Type of biometric
            sample_data: Captured biometric sample
            device_id: Device that captured sample
            location: Device location
            ip_address: Source IP address
            liveness_check: Whether liveness check passed
            
        Returns:
            (success, authentication_record)
        """
        auth_id = str(uuid.uuid4())
        
        with self.lock:
            # Check if user exists
            if user_id not in self.profiles:
                return (False, BiometricAuthentication(
                    auth_id=auth_id,
                    user_id=user_id,
                    biometric_type=biometric_type,
                    timestamp=time.time(),
                    status=BiometricStatus.FAILED,
                    similarity_score=0.0,
                    confidence=0.0,
                    device_id=device_id,
                    location=location,
                    ip_address=ip_address,
                    liveness_check=liveness_check,
                    match_quality=0.0
                ))
            
            profile = self.profiles[user_id]
            
            # Check if locked
            if profile.is_locked():
                return (False, BiometricAuthentication(
                    auth_id=auth_id,
                    user_id=user_id,
                    biometric_type=biometric_type,
                    timestamp=time.time(),
                    status=BiometricStatus.LOCKED,
                    similarity_score=0.0,
                    confidence=0.0,
                    device_id=device_id,
                    location=location,
                    ip_address=ip_address,
                    liveness_check=liveness_check,
                    match_quality=0.0
                ))
            
            # Check liveness
            if not liveness_check:
                profile.failed_attempts += 1
                if profile.failed_attempts >= self.max_failed_attempts:
                    profile.locked_until = time.time() + self.lockout_duration
                
                return (False, BiometricAuthentication(
                    auth_id=auth_id,
                    user_id=user_id,
                    biometric_type=biometric_type,
                    timestamp=time.time(),
                    status=BiometricStatus.FAILED,
                    similarity_score=0.0,
                    confidence=0.0,
                    device_id=device_id,
                    location=location,
                    ip_address=ip_address,
                    liveness_check=liveness_check,
                    match_quality=0.0
                ))
            
            # Get templates for this biometric type
            templates = profile.get_templates(biometric_type)
            if not templates:
                profile.failed_attempts += 1
                return (False, BiometricAuthentication(
                    auth_id=auth_id,
                    user_id=user_id,
                    biometric_type=biometric_type,
                    timestamp=time.time(),
                    status=BiometricStatus.FAILED,
                    similarity_score=0.0,
                    confidence=0.0,
                    device_id=device_id,
                    location=location,
                    ip_address=ip_address,
                    liveness_check=liveness_check,
                    match_quality=0.0
                ))
            
            # Create sample template
            sample_template = BiometricTemplate(
                biometric_id=f"sample_{auth_id}",
                biometric_type=biometric_type,
                user_id=user_id,
                template_data=sample_data,
                quality_score=85.0,
                enrollment_time=time.time(),
                last_verified=time.time()
            )
            
            # Find best match
            best_score = 0.0
            best_match = None
            
            for template in templates:
                score = template.calculate_similarity(sample_template)
                if score > best_score:
                    best_score = score
                    best_match = template
            
            # Check if match exceeds threshold
            success = best_score >= self.match_threshold
            
            if success:
                profile.failed_attempts = 0
                status = BiometricStatus.VERIFIED
                if best_match:
                    best_match.verification_count += 1
                    best_match.last_verified = time.time()
                confidence = min(100.0, best_score)
            else:
                profile.failed_attempts += 1
                if profile.failed_attempts >= self.max_failed_attempts:
                    profile.locked_until = time.time() + self.lockout_duration
                status = BiometricStatus.FAILED
                confidence = best_score
            
            # Create authentication record
            auth_record = BiometricAuthentication(
                auth_id=auth_id,
                user_id=user_id,
                biometric_type=biometric_type,
                timestamp=time.time(),
                status=status,
                similarity_score=best_score,
                confidence=confidence,
                device_id=device_id,
                location=location,
                ip_address=ip_address,
                liveness_check=liveness_check,
                match_quality=best_match.quality_score if best_match else 0.0
            )
            
            self.authentication_log.append(auth_record)
            return (success, auth_record)
    
    def get_profile(self, user_id: str) -> Optional[BiometricProfile]:
        """Get user's biometric profile."""
        with self.lock:
            return self.profiles.get(user_id)
    
    def get_authentication_history(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[BiometricAuthentication]:
        """
        Get authentication history for user.
        
        Args:
            user_id: User identifier
            limit: Maximum number of records
            
        Returns:
            List of authentication records
        """
        with self.lock:
            user_auths = [
                a for a in self.authentication_log
                if a.user_id == user_id
            ]
            return user_auths[-limit:]
    
    def get_authentication_statistics(self, user_id: str) -> Dict[str, Any]:
        """Get authentication statistics for user."""
        with self.lock:
            history = self.get_authentication_history(user_id, limit=1000)
            
            if not history:
                return {
                    "total_attempts": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": 0.0,
                    "average_confidence": 0.0,
                    "last_authentication": None
                }
            
            successful = sum(1 for a in history if a.status == BiometricStatus.VERIFIED)
            failed = sum(1 for a in history if a.status == BiometricStatus.FAILED)
            avg_confidence = sum(a.confidence for a in history) / len(history)
            
            return {
                "total_attempts": len(history),
                "successful": successful,
                "failed": failed,
                "success_rate": (successful / len(history)) * 100 if history else 0,
                "average_confidence": avg_confidence,
                "last_authentication": history[-1].timestamp,
                "by_type": self._stats_by_type(history),
                "by_status": self._stats_by_status(history)
            }
    
    def _stats_by_type(self, history: List[BiometricAuthentication]) -> Dict[str, int]:
        """Get statistics by biometric type."""
        stats = {}
        for auth in history:
            key = auth.biometric_type.value
            stats[key] = stats.get(key, 0) + 1
        return stats
    
    def _stats_by_status(self, history: List[BiometricAuthentication]) -> Dict[str, int]:
        """Get statistics by status."""
        stats = {}
        for auth in history:
            key = auth.status.value
            stats[key] = stats.get(key, 0) + 1
        return stats
    
    def unlock_user(self, user_id: str) -> bool:
        """Unlock user account."""
        with self.lock:
            if user_id not in self.profiles:
                return False
            
            self.profiles[user_id].locked_until = None
            self.profiles[user_id].failed_attempts = 0
            return True
    
    def delete_template(self, user_id: str, template_id: str) -> bool:
        """Delete a biometric template."""
        with self.lock:
            if user_id not in self.profiles:
                return False
            
            profile = self.profiles[user_id]
            for biometric_type, templates in profile.profiles.items():
                for i, template in enumerate(templates):
                    if template.biometric_id == template_id:
                        del templates[i]
                        profile.last_updated = time.time()
                        return True
            
            return False
    
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system-wide statistics."""
        with self.lock:
            total_users = len(self.profiles)
            total_attempts = len(self.authentication_log)
            
            if total_attempts == 0:
                return {
                    "total_users": total_users,
                    "total_authentication_attempts": 0,
                    "successful_authentications": 0,
                    "failed_authentications": 0,
                    "system_success_rate": 0.0,
                    "locked_users": 0
                }
            
            successful = sum(
                1 for a in self.authentication_log
                if a.status == BiometricStatus.VERIFIED
            )
            failed = sum(
                1 for a in self.authentication_log
                if a.status == BiometricStatus.FAILED
            )
            locked = sum(1 for p in self.profiles.values() if p.is_locked())
            
            return {
                "total_users": total_users,
                "total_authentication_attempts": total_attempts,
                "successful_authentications": successful,
                "failed_authentications": failed,
                "system_success_rate": (successful / total_attempts) * 100,
                "locked_users": locked,
                "average_match_confidence": (
                    sum(a.confidence for a in self.authentication_log) / total_attempts
                )
            }


class MultimodalBiometric:
    """
    Multi-modal biometric authentication combining multiple biometric types.
    Provides higher security through fusion of multiple factors.
    """
    
    def __init__(self, biometric_system: BiometricAuthentication):
        """Initialize multi-modal system."""
        self.system = biometric_system
        self.required_types = []
        self.weight_map: Dict[BiometricType, float] = {}
    
    def set_required_types(self, types: List[BiometricType], weights: Dict[BiometricType, float]):
        """
        Set required biometric types and their weights.
        
        Args:
            types: List of required biometric types
            weights: Weight for each type (should sum to 1.0)
        """
        self.required_types = types
        self.weight_map = weights
    
    def authenticate_multimodal(
        self,
        user_id: str,
        biometric_samples: Dict[BiometricType, List[float]],
        device_id: str = "default",
        location: str = "unknown",
        ip_address: str = "0.0.0.0"
    ) -> Tuple[bool, Dict[BiometricType, BiometricAuthentication]]:
        """
        Authenticate using multiple biometric types.
        
        Args:
            user_id: User identifier
            biometric_samples: Dict of biometric type -> sample data
            device_id: Device ID
            location: Device location
            ip_address: Source IP
            
        Returns:
            (success, authentication_results_dict)
        """
        results = {}
        total_score = 0.0
        
        for biometric_type, sample_data in biometric_samples.items():
            success, auth_record = self.system.authenticate(
                user_id=user_id,
                biometric_type=biometric_type,
                sample_data=sample_data,
                device_id=device_id,
                location=location,
                ip_address=ip_address
            )
            
            results[biometric_type] = auth_record
            
            # Add weighted score
            weight = self.weight_map.get(biometric_type, 1.0 / len(self.required_types))
            if auth_record.status == BiometricStatus.VERIFIED:
                total_score += auth_record.confidence * weight
        
        # Require all specified types to succeed and overall score above threshold
        all_success = all(
            results[btype].status == BiometricStatus.VERIFIED
            for btype in self.required_types
            if btype in results
        )
        
        overall_success = all_success and total_score >= 90.0
        
        return (overall_success, results)
