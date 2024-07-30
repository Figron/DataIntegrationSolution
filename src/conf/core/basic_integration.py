"""DataIntegration class that defines abstract read and write methods."""

from abc import ABC, abstractmethod
from typing import Any

from src.conf.utilities.logging_mixin import LoggingMixin


class DataIntegration(ABC, LoggingMixin):
    """Abstract class for the data sources."""

    @abstractmethod
    def read(self, *args: Any) -> Any:
        """Abstract method to read data."""

    @abstractmethod
    def write(self, *args: Any) -> None:
        """Abstract method to write data."""
