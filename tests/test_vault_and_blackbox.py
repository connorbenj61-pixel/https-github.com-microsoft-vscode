"""
Tests for Locked Vault and Black Box Systems
"""

import unittest
import time
from vault_and_blackbox import (
    LockedVault, BlackBox, AccessLevel, EventSeverity,
    VaultSecret, BlackBoxEvent, create_vault_and_blackbox
)
from armourbound_guardian import ArmourboundGuardianAI


class TestLockedVault(unittest.TestCase):
    """Test cases for LockedVault system."""
    
    def setUp(self):
        """Create a fresh vault for each test."""
        self.vault = LockedVault("test_password")
    
    def test_vault_creation(self):
        """Test vault initialization."""
        self.assertIsNotNone(self.vault)
        self.assertEqual(self.vault.failed_attempts, 0)
        self.assertEqual(len(self.vault.secrets), 0)
    
    def test_store_and_retrieve_secret(self):
        """Test storing and retrieving secrets."""
        self.vault.store_secret(
            "test_password",
            "api_key",
            "secret_value_12345"
        )
        
        retrieved = self.vault.retrieve_secret("test_password", "api_key")
        self.assertEqual(retrieved, "secret_value_12345")
    
    def test_wrong_password_rejected(self):
        """Test that wrong password is rejected."""
        self.vault.store_secret("test_password", "key", "value")
        
        retrieved = self.vault.retrieve_secret("wrong_password", "key")
        self.assertIsNone(retrieved)
        self.assertEqual(self.vault.failed_attempts, 1)
    
    def test_delete_secret(self):
        """Test deleting secrets."""
        self.vault.store_secret("test_password", "key1", "value1")
        
        deleted = self.vault.delete_secret("test_password", "key1")
        self.assertTrue(deleted)
        
        retrieved = self.vault.retrieve_secret("test_password", "key1")
        self.assertIsNone(retrieved)
    
    def test_list_secrets(self):
        """Test listing secrets."""
        self.vault.store_secret("test_password", "key1", "value1")
        self.vault.store_secret("test_password", "key2", "value2")
        self.vault.store_secret("test_password", "key3", "value3")
        
        keys = self.vault.list_secrets("test_password")
        self.assertEqual(len(keys), 3)
        self.assertIn("key1", keys)
        self.assertIn("key2", keys)
        self.assertIn("key3", keys)
    
    def test_access_levels(self):
        """Test different access levels."""
        self.vault.store_secret(
            "test_password",
            "public_key",
            "public_value",
            AccessLevel.PUBLIC
        )
        self.vault.store_secret(
            "test_password",
            "restricted_key",
            "restricted_value",
            AccessLevel.RESTRICTED
        )
        
        # List public secrets
        public = self.vault.list_secrets("test_password", AccessLevel.PUBLIC)
        self.assertEqual(len(public), 1)
        self.assertIn("public_key", public)
    
    def test_secret_expiration(self):
        """Test that secrets expire."""
        self.vault.store_secret(
            "test_password",
            "temporary_key",
            "temporary_value",
            ttl_seconds=1  # Expires in 1 second
        )
        
        # Should be accessible immediately
        value = self.vault.retrieve_secret("test_password", "temporary_key")
        self.assertEqual(value, "temporary_value")
        
        # Wait for expiration
        time.sleep(1.1)
        
        # Should be expired now
        value = self.vault.retrieve_secret("test_password", "temporary_key")
        self.assertIsNone(value)
    
    def test_tags_search(self):
        """Test searching by tags."""
        self.vault.store_secret(
            "test_password",
            "db_password",
            "pass123",
            tags=["database", "production"]
        )
        self.vault.store_secret(
            "test_password",
            "api_token",
            "token123",
            tags=["api", "production"]
        )
        self.vault.store_secret(
            "test_password",
            "test_key",
            "testkey",
            tags=["testing"]
        )
        
        # Search for production secrets
        prod_secrets = self.vault.search_secrets("test_password", ["production"])
        self.assertEqual(len(prod_secrets), 2)
        self.assertIn("db_password", prod_secrets)
        self.assertIn("api_token", prod_secrets)
    
    def test_vault_statistics(self):
        """Test vault statistics."""
        self.vault.store_secret("test_password", "key1", "value1")
        self.vault.store_secret("test_password", "key2", "value2")
        
        stats = self.vault.get_vault_stats("test_password")
        self.assertIsNotNone(stats)
        self.assertEqual(stats["total_secrets"], 2)
        self.assertEqual(stats["active_secrets"], 2)
    
    def test_access_tracking(self):
        """Test that access is tracked."""
        self.vault.store_secret("test_password", "key1", "value")
        
        # Access the secret multiple times
        self.vault.retrieve_secret("test_password", "key1")
        self.vault.retrieve_secret("test_password", "key1")
        self.vault.retrieve_secret("test_password", "key1")
        
        secret = self.vault.secrets["key1"]
        self.assertEqual(secret.access_count, 3)


class TestBlackBox(unittest.TestCase):
    """Test cases for BlackBox logging system."""
    
    def setUp(self):
        """Create a fresh black box for each test."""
        self.blackbox = BlackBox()
    
    def test_blackbox_creation(self):
        """Test black box initialization."""
        self.assertIsNotNone(self.blackbox)
        self.assertEqual(len(self.blackbox.events), 0)
    
    def test_log_event(self):
        """Test logging events."""
        event_id = self.blackbox.log_event(
            event_type="test",
            message="Test event",
            actor="test_actor",
            action="test_action"
        )
        
        self.assertIsNotNone(event_id)
        self.assertEqual(len(self.blackbox.events), 1)
    
    def test_query_by_type(self):
        """Test querying events by type."""
        self.blackbox.log_event("action", "msg1", "actor1", "do_action")
        self.blackbox.log_event("decision", "msg2", "actor2", "make_decision")
        self.blackbox.log_event("action", "msg3", "actor1", "do_action")
        
        actions = self.blackbox.query_events(event_type="action")
        self.assertEqual(len(actions), 2)
    
    def test_query_by_actor(self):
        """Test querying events by actor."""
        self.blackbox.log_event("action", "msg1", "actor1", "action1")
        self.blackbox.log_event("action", "msg2", "actor2", "action2")
        self.blackbox.log_event("action", "msg3", "actor1", "action3")
        
        actor1_events = self.blackbox.query_events(actor="actor1")
        self.assertEqual(len(actor1_events), 2)
    
    def test_query_by_severity(self):
        """Test querying events by severity."""
        self.blackbox.log_event(
            "action", "msg1", "actor", "action",
            severity=EventSeverity.CRITICAL
        )
        self.blackbox.log_event(
            "action", "msg2", "actor", "action",
            severity=EventSeverity.WARNING
        )
        self.blackbox.log_event(
            "action", "msg3", "actor", "action",
            severity=EventSeverity.CRITICAL
        )
        
        critical = self.blackbox.query_events(severity=EventSeverity.CRITICAL)
        self.assertEqual(len(critical), 2)
    
    def test_event_result_tracking(self):
        """Test tracking event results."""
        self.blackbox.log_event(
            "operation", "msg1", "actor", "op",
            result="success"
        )
        self.blackbox.log_event(
            "operation", "msg2", "actor", "op",
            result="failure"
        )
        
        events = self.blackbox.query_events(event_type="operation")
        success_count = sum(1 for e in events if e.result == "success")
        failure_count = sum(1 for e in events if e.result == "failure")
        
        self.assertEqual(success_count, 1)
        self.assertEqual(failure_count, 1)
    
    def test_blackbox_statistics(self):
        """Test black box statistics."""
        self.blackbox.log_event("action", "msg1", "actor1", "action")
        self.blackbox.log_event("action", "msg2", "actor2", "action")
        self.blackbox.log_event("decision", "msg3", "actor1", "action")
        
        stats = self.blackbox.get_statistics()
        self.assertEqual(stats["total_events"], 3)
        self.assertEqual(stats["by_type"]["action"], 2)
        self.assertEqual(stats["by_type"]["decision"], 1)
        self.assertEqual(stats["by_actor"]["actor1"], 2)
    
    def test_export_json(self):
        """Test exporting events as JSON."""
        self.blackbox.log_event("action", "msg1", "actor", "action")
        self.blackbox.log_event("action", "msg2", "actor", "action")
        
        json_export = self.blackbox.export_events("json")
        self.assertIn("action", json_export)
        self.assertIn("actor", json_export)
    
    def test_export_csv(self):
        """Test exporting events as CSV."""
        self.blackbox.log_event("action", "msg1", "actor", "action")
        
        csv_export = self.blackbox.export_events("csv")
        self.assertIn("event_id", csv_export)
        self.assertIn("timestamp", csv_export)
        self.assertIn("event_type", csv_export)
    
    def test_export_text(self):
        """Test exporting events as text."""
        self.blackbox.log_event("action", "msg1", "actor", "action")
        
        text_export = self.blackbox.export_events("text")
        self.assertIn("action", text_export)
        self.assertIn("msg1", text_export)
    
    def test_event_handlers(self):
        """Test event handler registration."""
        handled_events = []
        
        def handler(event):
            handled_events.append(event)
        
        self.blackbox.register_handler("test_event", handler)
        self.blackbox.log_event("test_event", "msg", "actor", "action")
        
        self.assertEqual(len(handled_events), 1)


class TestGuardianVaultIntegration(unittest.TestCase):
    """Test Guardian AI integration with vault system."""
    
    def setUp(self):
        """Create Guardian AI instance."""
        self.guardian = ArmourboundGuardianAI("test_vault_password")
    
    def test_guardian_has_vault(self):
        """Test that Guardian has vault."""
        self.assertIsNotNone(self.guardian.vault)
        self.assertIsNotNone(self.guardian.blackbox)
    
    def test_guardian_store_secret(self):
        """Test storing secret through Guardian."""
        result = self.guardian.vault_store_secret(
            "api_key",
            "secret123",
            access_level="confidential"
        )
        self.assertTrue(result)
    
    def test_guardian_retrieve_secret(self):
        """Test retrieving secret through Guardian."""
        self.guardian.vault_store_secret("password", "pass123")
        
        retrieved = self.guardian.vault_retrieve_secret("password")
        self.assertEqual(retrieved, "pass123")
    
    def test_guardian_vault_with_tags(self):
        """Test storing secrets with tags."""
        self.guardian.vault_store_secret(
            "db_user",
            "admin",
            tags=["database", "prod"]
        )
        
        found = self.guardian.vault_search_by_tags(["database"])
        self.assertIn("db_user", found)
    
    def test_guardian_vault_statistics(self):
        """Test vault statistics through Guardian."""
        self.guardian.vault_store_secret("key1", "value1")
        self.guardian.vault_store_secret("key2", "value2")
        
        stats = self.guardian.vault_get_statistics()
        self.assertEqual(stats["total_secrets"], 2)


class TestGuardianBlackboxIntegration(unittest.TestCase):
    """Test Guardian AI integration with black box system."""
    
    def setUp(self):
        """Create Guardian AI instance."""
        self.guardian = ArmourboundGuardianAI("test_password")
    
    def test_guardian_logs_operations(self):
        """Test that Guardian logs operations."""
        initial_count = self.guardian.blackbox_get_operation_count()
        
        self.guardian.vault_store_secret("key", "value")
        
        new_count = self.guardian.blackbox_get_operation_count()
        self.assertGreater(new_count, initial_count)
    
    def test_guardian_blackbox_event_logging(self):
        """Test logging events through Guardian."""
        event_id = self.guardian.blackbox_log_event(
            "test_event",
            "Test message",
            "test_action"
        )
        
        self.assertIsNotNone(event_id)
    
    def test_guardian_blackbox_query(self):
        """Test querying black box events."""
        self.guardian.blackbox_log_event("action", "msg1", "do_action")
        self.guardian.blackbox_log_event("decision", "msg2", "make_decision")
        
        actions = self.guardian.blackbox_query_events(event_type="action")
        self.assertGreater(len(actions), 0)
    
    def test_guardian_blackbox_statistics(self):
        """Test black box statistics."""
        self.guardian.blackbox_log_event("action", "msg", "action")
        
        stats = self.guardian.blackbox_get_statistics()
        self.assertGreater(stats["total_events"], 0)
    
    def test_guardian_blackbox_export(self):
        """Test exporting black box log."""
        self.guardian.blackbox_log_event("action", "msg", "action")
        
        json_log = self.guardian.blackbox_export_log("json")
        self.assertIsNotNone(json_log)
        self.assertGreater(len(json_log), 0)


class TestVaultSecurityFeatures(unittest.TestCase):
    """Test security features of vault."""
    
    def test_failed_attempt_tracking(self):
        """Test tracking of failed password attempts."""
        vault = LockedVault("correct_password")
        
        # Try with wrong password
        vault.list_secrets("wrong_password")
        self.assertEqual(vault.failed_attempts, 1)
        
        vault.list_secrets("wrong_password")
        self.assertEqual(vault.failed_attempts, 2)
        
        # Correct password resets counter
        vault.list_secrets("correct_password")
        self.assertEqual(vault.failed_attempts, 0)
    
    def test_secret_encryption_flag(self):
        """Test that secrets are marked as encrypted."""
        vault = LockedVault("password")
        vault.store_secret("password", "key", "value")
        
        secret = vault.secrets["key"]
        self.assertTrue(secret.encrypted)
    
    def test_access_log_creation(self):
        """Test that access is logged."""
        vault = LockedVault("password")
        vault.store_secret("password", "key", "value")
        vault.retrieve_secret("password", "key")
        
        # Check access log has entries
        self.assertGreater(len(vault.access_log), 0)


class TestBlackboxAudit(unittest.TestCase):
    """Test audit trail capabilities of black box."""
    
    def test_immutable_log(self):
        """Test that events are immutable (append-only)."""
        bb = BlackBox()
        event_count = len(bb.events)
        
        bb.log_event("action", "msg", "actor", "action")
        self.assertEqual(len(bb.events), event_count + 1)
        
        bb.log_event("action", "msg", "actor", "action")
        self.assertEqual(len(bb.events), event_count + 2)
    
    def test_timestamp_ordering(self):
        """Test that events are timestamped in order."""
        bb = BlackBox()
        
        event1 = bb.log_event("action", "msg1", "actor", "action")
        time.sleep(0.01)
        event2 = bb.log_event("action", "msg2", "actor", "action")
        
        e1 = bb.get_event_history(event1)
        e2 = bb.get_event_history(event2)
        
        self.assertLess(e1.timestamp, e2.timestamp)
    
    def test_complete_operation_trace(self):
        """Test tracing a complete operation."""
        bb = BlackBox()
        
        # Simulate operation: store -> process -> retrieve
        bb.log_event("store", "Storing data", "system", "store_op")
        bb.log_event("process", "Processing data", "system", "process_op")
        bb.log_event("retrieve", "Retrieving data", "system", "retrieve_op")
        
        store_events = bb.query_events(event_type="store")
        self.assertEqual(len(store_events), 1)
        self.assertEqual(store_events[0].action, "store_op")


if __name__ == "__main__":
    unittest.main()
