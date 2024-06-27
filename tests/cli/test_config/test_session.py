import os
import pickle
from tempfile import gettempdir

from pipes_cmd.config.settings import ClientSettings
from pipes_cmd.config.session import FileBasedSessionManager, Session, get_or_create_pipes_session


def test_file_based_session_manager():
    base_directory = gettempdir()
    manager = FileBasedSessionManager(base_directory)

    # session directory
    session_directory = manager.get_session_directory()
    assert os.path.exists(session_directory)
    assert os.path.basename(session_directory) == "sessions"

    # create a new session

    session1 = Session(data={"project": "P1", "model": "M1"})
    session1._manager = manager
    session1.save()
    session_file = os.path.join(base_directory, "sessions", session1.session_id)
    assert os.path.exists(session_file)

    # check session data
    data = manager.get_session_data_by_id(session_id=session1.session_id)
    session2 = Session(data=data)
    assert session2.has_key("project")
    assert session2.pop("project") == "P1"
    assert session2.has_key("model")
    assert session2.pop("model") == "M1"


def test_get_or_create_pipes_session():
    session = get_or_create_pipes_session()
    settings = ClientSettings()
    assert settings.pipes_session_id == session.session_id

if __name__=="__main__":
    test_file_based_session_manager()
    test_get_or_create_pipes_session()