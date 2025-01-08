import json
import os
from abc import ABC, abstractmethod
from pathlib import Path

from pipes.config.config import PIPES_CONFIG_DIR


class AbstractSessionManager(ABC):
    """Abstract session manager class"""

    @abstractmethod
    def save_session(self, session):
        """Save session object into storage"""

    @abstractmethod
    def purge_session(self):
        """Purge the sessions"""


class FileBasedSessionManager(AbstractSessionManager):
    """Implement file-based session manager"""

    __filename__ = 'session'

    def __init__(self, base_dir=None):
        if base_dir:
            self.session_dir = Path(base_dir)
        else:
            self.session_dir = PIPES_CONFIG_DIR
        os.makedirs(self.session_dir, exist_ok=True)
        self.session_file = self.session_dir.joinpath(self.__filename__)

    def save_session(self, session):
        with open(self.session_file, "w") as f:
            json.dump(session.data, f, indent=2)

    def purge_session(self, session):
        session.data = {}
        self.save_session(session)


class Session:
    def __init__(self, data=None, base_dir=None):
        self.manager = FileBasedSessionManager(base_dir=base_dir)
        if os.path.isfile(self.manager.session_file):
            with open(self.manager.session_file, "r") as f:
                self.data = json.load(f)
        else:
            self.data = {}

        if data and isinstance(data, dict):
            self.update(data)

    def save(self):
        """Save the session into underlying storage"""
        self.manager.save_session(self)

    def contains(self, key):
        return key in self.data

    def get(self, key):
        return self.data.get(key)

    def pop(self, key, default=None):
        return self.data.pop(key, default)

    def update(self, data):
        self.data.update(data)
        self.save()
