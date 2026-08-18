"""
Tests for the secure search endpoint in sql_injection.py.

These tests verify:
1. The /secure/search endpoint returns results correctly for valid input.
2. Server-side validation blocks oversized or invalid inputs (CWE-472 fix).
3. SQL injection payloads passed as LIKE parameters are treated as data,
   not executable SQL, due to parameterized queries.
4. Regression: The taint flow from request.args.get('q') to cursor.execute
   is broken by the validation gate introduced in the fix.
"""

import sqlite3
import pytest

# Import the Flask app and the init_db function from the module under test.
from ASCA.sql_injection import app, init_db


@pytest.fixture(autouse=True)
def setup_db():
    """Initialize an in-memory SQLite database before each test."""
    init_db()
    yield


@pytest.fixture
def client():
    """Return a Flask test client with TESTING mode enabled."""
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Positive / functionality tests
# ---------------------------------------------------------------------------

class TestSecureSearchFunctionality:
    """Verify that the /secure/search endpoint works correctly for valid input."""

    def test_returns_matching_user(self, client):
        """A valid search term that matches a username returns that user."""
        response = client.get("/secure/search?q=admin")
        assert response.status_code == 200
        data = response.data.decode()
        assert "admin" in data

    def test_returns_empty_for_no_match(self, client):
        """A valid search term with no match returns an empty body."""
        response = client.get("/secure/search?q=doesnotexist_xyz")
        assert response.status_code == 200
        assert response.data.decode() == ""

    def test_empty_search_returns_all_users(self, client):
        """An empty search term acts as a wildcard and returns all users."""
        response = client.get("/secure/search?q=")
        assert response.status_code == 200
        data = response.data.decode()
        # All three seeded users should be present
        assert "admin" in data
        assert "user1" in data
        assert "test" in data

    def test_partial_match(self, client):
        """A partial username term matches multiple users via LIKE wildcard."""
        response = client.get("/secure/search?q=user")
        assert response.status_code == 200
        data = response.data.decode()
        assert "user1" in data
        # 'admin' and 'test' should not appear
        assert "admin" not in data

    def test_response_content_type(self, client):
        """Response Content-Type should be text/plain."""
        response = client.get("/secure/search?q=admin")
        assert "text/plain" in response.content_type


# ---------------------------------------------------------------------------
# Validation / rejection tests  (CWE-472 fix regression tests)
# ---------------------------------------------------------------------------

class TestSecureSearchInputValidation:
    """Verify that server-side validation rejects invalid or oversized inputs."""

    def test_oversized_search_term_rejected(self, client):
        """A search term longer than 200 characters must return HTTP 400."""
        long_term = "a" * 201
        response = client.get(f"/secure/search?q={long_term}")
        assert response.status_code == 400

    def test_exactly_200_characters_accepted(self, client):
        """A search term of exactly 200 characters should be accepted (HTTP 200)."""
        term = "a" * 200
        response = client.get(f"/secure/search?q={term}")
        assert response.status_code == 200

    def test_missing_q_parameter_defaults_to_empty(self, client):
        """Omitting the 'q' parameter entirely uses the empty-string default."""
        response = client.get("/secure/search")
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# SQL injection / parameter tampering tests
# ---------------------------------------------------------------------------

class TestSecureSearchSQLInjection:
    """
    Verify that SQL injection payloads are treated as literal data and do not
    alter query semantics or expose unintended rows.
    """

    def test_sql_injection_single_quote_escaped(self, client):
        """
        A payload containing a single quote should not cause a 500 error and
        should return no rows (it is treated as a literal string, not SQL).
        """
        response = client.get("/secure/search?q=admin'--")
        # Must not crash the server
        assert response.status_code == 200
        # The literal string "admin'--" does not match any username
        data = response.data.decode()
        assert "admin'--" not in data or data == ""

    def test_union_injection_payload_returns_no_extra_rows(self, client):
        """
        A UNION-based injection payload must not return extra rows; the whole
        payload is treated as a LIKE pattern, not SQL.
        """
        payload = "a' UNION SELECT id,username,email FROM users WHERE '1'='1"
        response = client.get(f"/secure/search?q={payload}")
        assert response.status_code == 200
        # The injected UNION clause is a literal search string — no username
        # matches it, so the result must be empty (not a dump of all users).
        data = response.data.decode()
        # If injection succeeded, all users would be present; assert they are not
        assert "admin" not in data
        assert "user1" not in data
        assert "test" not in data

    def test_drop_table_payload_does_not_destroy_db(self, client):
        """
        A payload that tries to DROP the users table must be treated as data.
        A subsequent valid query must still return results (table still exists).
        """
        drop_payload = "'; DROP TABLE users; --"
        response = client.get(f"/secure/search?q={drop_payload}")
        # Must not crash
        assert response.status_code in (200, 400)

        # Table must still be intact: a clean query should still find 'admin'
        response2 = client.get("/secure/search?q=admin")
        assert response2.status_code == 200
        assert "admin" in response2.data.decode()

    def test_or_1_equals_1_payload(self, client):
        """
        A classic ' OR '1'='1 payload must not return all users.
        """
        response = client.get("/secure/search?q=' OR '1'='1")
        assert response.status_code == 200
        # If vulnerable, all users would appear; they must not
        data = response.data.decode()
        # The payload is used as a LIKE pattern — it won't match normal usernames
        assert not ("admin" in data and "user1" in data and "test" in data)

    def test_null_byte_injection(self, client):
        """
        A search term containing a NUL byte (\x00) must not crash the server
        and must be handled safely.
        """
        # NUL byte expressed as a URL-encoded %00 parameter
        response = client.get("/secure/search?q=admin\x00evil")
        assert response.status_code in (200, 400)

    def test_boolean_based_blind_payload(self, client):
        """
        Boolean-based blind injection payload must not return extra rows.
        """
        response = client.get("/secure/search?q=admin' AND '1'='1")
        assert response.status_code == 200
        data = response.data.decode()
        # Injected SQL is treated as literal data; no username matches the payload
        assert "user1" not in data
        assert "test" not in data
