from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from PG.repositories.db_setup import get_session
from VENDOR.helper.session_interface import SecretFacade

# SessionHelper storage
session_helper = {}


def get_session_helper(vendor_name, secret_arn, region):
    """Retrieve or create a SessionHelper instance for a given vendor."""
    if vendor_name not in session_helper:
        # Initialize SecretFacade dynamically
        secret_facade = SecretFacade(secret_arn=secret_arn, region=region)
        
        # Fetch the connection string for the vendor
        connection_string = secret_facade.get_db_string(vendor_name=vendor_name)
        
        # Create and store a new SessionHelper instance
        session_helper[vendor_name] = SessionHelper(connection_string)
    return session_helper[vendor_name]


class SessionHelper:
    def __init__(self, db_connection_string):
        """Initialize the SQLAlchemy engine with the connection string."""
        self.engine = create_engine(db_connection_string, pool_size=30)

    def get_session(self):
        """Create and return a new database session."""
        Session = sessionmaker(bind=self.engine)
        session = Session()
        self.session = get_session(session, self.engine)
        return self.session


def get_sessions(vendor_name, secret_arn, region="ap-south-1"):
    """Retrieve a session for the given vendor.

    Args:
        vendor_name (str): The name of the vendor.
        secret_arn (str): The ARN of the Secrets Manager where connection strings are stored.
        region (str): The AWS region of the Secrets Manager.

    Returns:
        session: The database session for the given vendor.
    """

    vendor_session_helper = get_session_helper(vendor_name, secret_arn, region)
    vendor_session = vendor_session_helper.get_session()

    return vendor_session
