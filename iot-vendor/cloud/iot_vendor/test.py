import unittest
from VENDOR.session_helper import get_sessions
from sqlalchemy.sql import text

class TestSessionHelper(unittest.TestCase):
    def setUp(self):
        """Setup test data."""
        # self.connection_string = "postgresql://postgres:msiliotplatform@msil-iot-platform-db-development.cqugg5zx1no1.ap-south-1.rds.amazonaws.com/msil-iot-pqc-db"
        self.vendor_name = "vendor01"
        self.secret_arn = "arn:aws:secretsmanager:ap-south-1:881345909107:secret:apikey/32/38v1atzl51-82meJD"

    def test_session_creation(self):
        """Test if a session is created successfully."""
        # Call the function to get a session
        session = get_sessions(vendor_name=self.vendor_name, secret_arn=self.secret_arn) #connection_string=self.connection_string

        # Assert the session is not None
        self.assertIsNotNone(session, "Session should not be None")
        try:
            # Perform a simple query
            result = session.execute(text("SELECT 1")).scalar()
            print(result)
            self.assertEqual(result, 1, "Expected query result to be 1")
        finally:
            session.close()

if __name__ == "__main__":
    unittest.main()