import os
import sys
import pytest
import asyncio

# Programmatically insert the root repository directory into the Python runtime search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def event_loop():
    """Configures the foundational async event loop lifecycle for testing modules."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
