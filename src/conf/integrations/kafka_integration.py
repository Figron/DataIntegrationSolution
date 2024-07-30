"""Class to handle Kafka integration."""
import json
import time

from kafka import KafkaProducer

from src.conf.constants import KAFKA_BOOTSTRAP_SERVERS
from src.conf.utilities.logging_mixin import LoggingMixin


class KafkaIntegration(LoggingMixin):
    """A class containing configuration for Kafka related operations."""

    def __init__(self):
        time.sleep(5)
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
                                      value_serializer=lambda v: json.dumps(v).encode("utf-8"))

    def write(self, data: dict, topic: str) -> None:
        """Write the data to Kafka."""
        self.producer.send(topic, data)
