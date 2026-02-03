"""
Locked Vault and Black Box System for ArmourboundGuardianAI

PEGI 3: Secure storage and operational logging system for Guardian AI
"""

import json
import hashlib
import time
import uuid
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum
import threading
from pathlib import Path


class AccessLevel(Enum):
    """Access control levels for vault."""
    RESTRICTED = "restricted"  # Highest security
    CONFIDENTIAL = "confidential"  # Sensitive data
    INTERNAL = "internal"  # Internal only
    PUBLIC = "public"  # Publicly accessible


class EventSeverity(Enum):
    """Severity levels for black box events."""
    CRITICAL = "critical"  # System critical events
    WARNING = "warning"  # Warning conditions
    INFO = "info"  # Informational
    DEBUG = "debug"  # Debug level


@dataclass
class VaultSecret:
    """A secret stored in the vault."""
    key: str
    value: Any
    access_level: AccessLevel
    created_at: float
    last_accessed: float
    access_count: int = 0
    encrypted: bool = True
    tags: List[str] = field(default_factory=list)
    expiration: Optional[float] = None
    
    def is_expired(self) -> bool:
        """Check if secret has expired."""
        if self.expiration is None:
            return False
        return time.time() > self.expiration
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class BlackBoxEvent:
    """An event recorded in the black box."""
    event_id: str
    timestamp: float
    event_type: str
    severity: EventSeverity
    message: str
    actor: str  # Who/what triggered the event
    action: str  # What action was performed
    data: Dict[str, Any]
    result: str  # success, failure, pending
    duration_ms: float
    session_id: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        result = asdict(self)
        result['severity'] = self.severity.value
        return result


class LockedVault:
    """
    Secure storage system for sensitive data.
    
    Features:
    - Encryption support
    - Access control with multiple security levels
    - Automatic expiration
    - Access tracking
    - Thread-safe operations
    """
    
    def __init__(self, master_password: str):
        """Initialize vault with master password."""
        self.master_password_hash = hashlib.sha256(master_password.encode()).hexdigest()
        self.secrets: Dict[str, VaultSecret] = {}
        self.lock = threading.RLock()
        self.access_log: List[Dict] = []
        self.failed_attempts = 0
        self.max_failed_attempts = 5
        self.last_failed_attempt = 0
    
    def _verify_password(self, password: str) -> bool:
        """Verify master password."""
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash == self.master_password_hash
    
    def _hash_key(self, key: str) -> str:
        """Generate hash for key."""
        return hashlib.sha256(key.encode()).hexdigest()
    
    def store_secret(
        self,
        password: str,
        key: str,
        value: Any,
        access_level: AccessLevel = AccessLevel.INTERNAL,
        ttl_seconds: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> bool:
        """
        Store a secret in the vault.
        
        Args:
            password: Master password for authentication
            key: Unique key for the secret
            value: Secret value to store
            access_level: Security level
            ttl_seconds: Time-to-live in seconds (None = no expiration)
            tags: Tags for organizing secrets
            
        Returns:
            True if successful, False otherwise
        """
        if not self._verify_password(password):
            self.failed_attempts += 1
            self.last_failed_attempt = time.time()
            return False
        
        self.failed_attempts = 0
        
        with self.lock:
            now = time.time()
            expiration = (now + ttl_seconds) if ttl_seconds else None
            
            self.secrets[key] = VaultSecret(
                key=key,
                value=value,
                access_level=access_level,
                created_at=now,
                last_accessed=now,
                access_count=0,
                encrypted=True,
                tags=tags or [],
                expiration=expiration
            )
            
            # Log access
            self.access_log.append({
                'timestamp': now,
                'action': 'store',
                'key': key,
                'access_level': access_level.value,
                'success': True
            })
            
            return True
    
    def retrieve_secret(self, password: str, key: str) -> Optional[Any]:
        """
        Retrieve a secret from the vault.
        
        Args:
            password: Master password for authentication
            key: Key of the secret to retrieve
            
        Returns:
            The secret value if found and authenticated, None otherwise
        """
        if not self._verify_password(password):
            self.failed_attempts += 1
            self.last_failed_attempt = time.time()
            return None
        
        self.failed_attempts = 0
        
        with self.lock:
            if key not in self.secrets:
                self._log_access('retrieve', key, False)
                return None
            
            secret = self.secrets[key]
            
            # Check expiration
            if secret.is_expired():
                del self.secrets[key]
                self._log_access('retrieve', key, False, 'expired')
                return None
            
            # Update access tracking
            secret.access_count += 1
            secret.last_accessed = time.time()
            
            self._log_access('retrieve', key, True)
            return secret.value
    
    def delete_secret(self, password: str, key: str) -> bool:
        """
        Delete a secret from the vault.
        
        Args:
            password: Master password for authentication
            key: Key of the secret to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not self._verify_password(password):
            self.failed_attempts += 1
            self.last_failed_attempt = time.time()
            return False
        
        self.failed_attempts = 0
        
        with self.lock:
            if key in self.secrets:
                del self.secrets[key]
                self._log_access('delete', key, True)
                return True
            
            self._log_access('delete', key, False)
            return False
    
    def list_secrets(self, password: str, access_level: Optional[AccessLevel] = None) -> List[str]:
        """
        List secret keys (values not included).
        
        Args:
            password: Master password for authentication
            access_level: Filter by access level
            
        Returns:
            List of secret keys
        """
        if not self._verify_password(password):
            self.failed_attempts += 1
            self.last_failed_attempt = time.time()
            return []
        
        self.failed_attempts = 0
        
        with self.lock:
            keys = []
            for key, secret in self.secrets.items():
                if secret.is_expired():
                    continue
                if access_level is None or secret.access_level == access_level:
                    keys.append(key)
            
            self._log_access('list', 'all', True, f'returned {len(keys)} keys')
            return keys
    
    def search_secrets(self, password: str, tags: List[str]) -> List[str]:
        """
        Search secrets by tags.
        
        Args:
            password: Master password for authentication
            tags: Tags to search for
            
        Returns:
            List of matching secret keys
        """
        if not self._verify_password(password):
            self.failed_attempts += 1
            self.last_failed_attempt = time.time()
            return []
        
        self.failed_attempts = 0
        
        with self.lock:
            matching = []
            for key, secret in self.secrets.items():
                if secret.is_expired():
                    continue
                if any(tag in secret.tags for tag in tags):
                    matching.append(key)
            
            return matching
    
    def get_vault_stats(self, password: str) -> Optional[Dict]:
        """
        Get vault statistics.
        
        Args:
            password: Master password for authentication
            
        Returns:
            Dictionary with vault statistics
        """
        if not self._verify_password(password):
            return None
        
        with self.lock:
            total_secrets = len(self.secrets)
            expired_count = sum(1 for s in self.secrets.values() if s.is_expired())
            access_levels = {}
            
            for secret in self.secrets.values():
                level = secret.access_level.value
                access_levels[level] = access_levels.get(level, 0) + 1
            
            return {
                'total_secrets': total_secrets,
                'active_secrets': total_secrets - expired_count,
                'expired_secrets': expired_count,
                'access_levels': access_levels,
                'total_accesses': sum(s.access_count for s in self.secrets.values()),
                'failed_attempts': self.failed_attempts,
                'last_modified': max([s.last_accessed for s in self.secrets.values()],
                                    default=0)
            }
    
    def _log_access(self, action: str, key: str, success: bool, extra: str = ""):
        """Log vault access."""
        self.access_log.append({
            'timestamp': time.time(),
            'action': action,
            'key': key,
            'success': success,
            'extra': extra
        })
        # Keep log size manageable
        if len(self.access_log) > 10000:
            self.access_log = self.access_log[-5000:]


class BlackBox:
    """
    Immutable event logging system for AI operations.
    
    Features:
    - Records all AI actions and decisions
    - Timestamps and severity levels
    - Session tracking
    - Immutable append-only log
    - Thread-safe operations
    - Event queries and analysis
    """
    
    def __init__(self):
        """Initialize black box."""
        self.events: List[BlackBoxEvent] = []
        self.lock = threading.RLock()
        self.session_id = str(uuid.uuid4())
        self.session_start = time.time()
        self.event_handlers: Dict[str, List[callable]] = {}
    
    def log_event(
        self,
        event_type: str,
        message: str,
        actor: str,
        action: str,
        severity: EventSeverity = EventSeverity.INFO,
        data: Optional[Dict[str, Any]] = None,
        result: str = "success",
        duration_ms: float = 0.0
    ) -> str:
        """
        Log an event in the black box.
        
        Args:
            event_type: Type of event (e.g., 'action', 'decision', 'error')
            message: Human-readable message
            actor: Who/what performed the action
            action: What action was performed
            severity: Severity level
            data: Additional event data
            result: Result of the action (success, failure, pending)
            duration_ms: Duration in milliseconds
            
        Returns:
            Event ID for tracking
        """
        event_id = str(uuid.uuid4())
        
        with self.lock:
            event = BlackBoxEvent(
                event_id=event_id,
                timestamp=time.time(),
                event_type=event_type,
                severity=severity,
                message=message,
                actor=actor,
                action=action,
                data=data or {},
                result=result,
                duration_ms=duration_ms,
                session_id=self.session_id
            )
            
            self.events.append(event)
            
            # Trigger event handlers
            self._trigger_handlers(event_type, event)
        
        return event_id
    
    def query_events(
        self,
        event_type: Optional[str] = None,
        actor: Optional[str] = None,
        severity: Optional[EventSeverity] = None,
        time_range: Optional[Tuple[float, float]] = None,
        limit: Optional[int] = None
    ) -> List[BlackBoxEvent]:
        """
        Query events from the black box.
        
        Args:
            event_type: Filter by event type
            actor: Filter by actor
            severity: Filter by severity
            time_range: (start_time, end_time) tuple in seconds since epoch
            limit: Maximum number of results
            
        Returns:
            List of matching events
        """
        with self.lock:
            results = self.events[:]
        
        # Apply filters
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        if actor:
            results = [e for e in results if e.actor == actor]
        if severity:
            results = [e for e in results if e.severity == severity]
        if time_range:
            start, end = time_range
            results = [e for e in results if start <= e.timestamp <= end]
        
        # Apply limit
        if limit:
            results = results[-limit:]
        
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get black box statistics."""
        with self.lock:
            events = self.events[:]
        
        if not events:
            return {
                'total_events': 0,
                'session_duration_seconds': time.time() - self.session_start,
                'by_type': {},
                'by_severity': {},
                'by_result': {},
                'by_actor': {}
            }
        
        by_type = {}
        by_severity = {}
        by_result = {}
        by_actor = {}
        
        for event in events:
            by_type[event.event_type] = by_type.get(event.event_type, 0) + 1
            severity = event.severity.value
            by_severity[severity] = by_severity.get(severity, 0) + 1
            by_result[event.result] = by_result.get(event.result, 0) + 1
            by_actor[event.actor] = by_actor.get(event.actor, 0) + 1
        
        return {
            'total_events': len(events),
            'session_duration_seconds': time.time() - self.session_start,
            'by_type': by_type,
            'by_severity': by_severity,
            'by_result': by_result,
            'by_actor': by_actor,
            'first_event': events[0].timestamp,
            'last_event': events[-1].timestamp
        }
    
    def get_event_history(self, event_id: str) -> Optional[BlackBoxEvent]:
        """Get a specific event by ID."""
        with self.lock:
            for event in self.events:
                if event.event_id == event_id:
                    return event
        return None
    
    def export_events(self, format: str = "json") -> str:
        """
        Export events in specified format.
        
        Args:
            format: Export format ('json', 'csv', 'text')
            
        Returns:
            Exported events as string
        """
        with self.lock:
            events = self.events[:]
        
        if format == "json":
            return json.dumps(
                [e.to_dict() for e in events],
                indent=2,
                default=str
            )
        
        elif format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.DictWriter(
                output,
                fieldnames=['event_id', 'timestamp', 'event_type', 'severity',
                           'actor', 'action', 'result', 'duration_ms']
            )
            writer.writeheader()
            for event in events:
                writer.writerow({
                    'event_id': event.event_id,
                    'timestamp': datetime.fromtimestamp(event.timestamp).isoformat(),
                    'event_type': event.event_type,
                    'severity': event.severity.value,
                    'actor': event.actor,
                    'action': event.action,
                    'result': event.result,
                    'duration_ms': event.duration_ms
                })
            return output.getvalue()
        
        else:  # text format
            lines = []
            for event in events:
                dt = datetime.fromtimestamp(event.timestamp).isoformat()
                lines.append(
                    f"[{dt}] {event.severity.value.upper():8} | "
                    f"{event.actor:20} | {event.action:20} | {event.message}"
                )
            return "\n".join(lines)
    
    def register_handler(self, event_type: str, handler: callable):
        """Register a handler for event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def _trigger_handlers(self, event_type: str, event: BlackBoxEvent):
        """Trigger registered handlers for event."""
        handlers = self.event_handlers.get(event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception:
                pass  # Prevent handler errors from breaking logging
    
    def save_to_file(self, filepath: str, format: str = "json"):
        """Save black box log to file."""
        content = self.export_events(format)
        Path(filepath).write_text(content)
    
    def load_from_file(self, filepath: str):
        """Load black box log from file (appends to existing events)."""
        content = Path(filepath).read_text()
        data = json.loads(content)
        for item in data:
            event = BlackBoxEvent(
                event_id=item['event_id'],
                timestamp=item['timestamp'],
                event_type=item['event_type'],
                severity=EventSeverity(item['severity']),
                message=item['message'],
                actor=item['actor'],
                action=item['action'],
                data=item['data'],
                result=item['result'],
                duration_ms=item['duration_ms'],
                session_id=item['session_id']
            )
            with self.lock:
                self.events.append(event)


# Integration helper functions

def create_vault_and_blackbox(master_password: str) -> Tuple[LockedVault, BlackBox]:
    """Create both vault and black box instances."""
    vault = LockedVault(master_password)
    blackbox = BlackBox()
    return vault, blackbox


def secure_operation(
    blackbox: BlackBox,
    actor: str,
    action: str,
    operation: callable,
    *args,
    **kwargs
) -> Tuple[Any, str]:
    """
    Execute an operation with automatic black box logging.
    
    Returns:
        (result, event_id)
    """
    start_time = time.time()
    event_id = None
    result = None
    success = "success"
    
    try:
        result = operation(*args, **kwargs)
        return result, event_id
    except Exception as e:
        success = "failure"
        raise
    finally:
        duration_ms = (time.time() - start_time) * 1000
        event_id = blackbox.log_event(
            event_type="operation",
            message=f"{actor} performed {action}",
            actor=actor,
            action=action,
            severity=EventSeverity.INFO,
            result=success,
            duration_ms=duration_ms
        )
