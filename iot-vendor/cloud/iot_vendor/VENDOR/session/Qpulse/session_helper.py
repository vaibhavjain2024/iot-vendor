from QP.repositories.db_setup import get_session, create_tables_and_indexes_for_schema
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from QP.helper.session_interface import SecretFacade
import os

# SessionHelper storage
session_helper = {}


def get_session_helper(vendor_name, secret_arn, region, timeout=None):
    """Retrieve or create a SessionHelper instance for a given vendor."""
    if vendor_name not in session_helper:
        # Initialize SecretFacade dynamically
        secret_facade = SecretFacade(secret_arn=secret_arn, region=region)
        
        # Fetch the connection string for the vendor
        connection_string = secret_facade.get_db_string(vendor_name=vendor_name)
        
        # Create and store a new SessionHelper instance
        session_helper[vendor_name] = SessionHelper(connection_string, timeout)
    return session_helper[vendor_name]


class SessionHelper:
    def __init__(self, db_connection_string, timeout=None):
        """Initialize the SQLAlchemy engine with the connection string."""
        statement_timeout = int(os.environ.get("statement_timeout", 900000))
        work_mem = os.environ.get("work_mem", "4MB")

        connect_args = {}
        if timeout:
            connect_args["options"] = f"-c statement_timeout={timeout}"

        self.engine = create_engine(
            db_connection_string,
            pool_size=30,
            connect_args={
                "options": f"-c statement_timeout={statement_timeout} -c work_mem={work_mem}"
            }
        )

    def get_session(self, shop_id=None, create_tables_and_indexes=False):
        Session = sessionmaker(bind=self.engine)
        schema_name = None
        if shop_id:
            schema_name = f'SHOP_{shop_id}'
            schema_engine = self.engine.execution_options(
                schema_translate_map={None: schema_name}
            )
            session = Session(bind=schema_engine)
            session.connection(
                execution_options={"schema_translate_map": {None: schema_name}}
            )
            if create_tables_and_indexes:
                create_tables_and_indexes_for_schema(self.engine, schema_name)
        else:
            session = Session()
            session = get_session(session, self.engine)
        return session


def get_sessions(vendor_name, secret_arn, shop_id=None, region="ap-south-1", timeout=None):
    """Retrieve a session for the given vendor.

    Args:
        vendor_name (str): The name of the vendor.
        secret_arn (str): The ARN of the Secrets Manager where connection strings are stored.
        region (str): The AWS region of the Secrets Manager.

    Returns:
        session: The database session for the given vendor.
    """

    vendor_session_helper = get_session_helper(vendor_name, secret_arn, region, timeout)
    vendor_session = vendor_session_helper.get_session(shop_id = shop_id)

    return vendor_session
