"""Module that watches for new files in a MinIO bucket and sends them to a Kafka topic."""
import time

from src.conf.integrations.kafka_integration import KafkaIntegration
from src.conf.integrations.minio_integration import MinioIntegration
from src.conf.utilities.logging_mixin import LoggingMixin


class MinioWatcher(LoggingMixin):
    """A class to watch for new files in a MinIO bucket and send them to a Kafka topic."""

    def __init__(self):
        self.minio = MinioIntegration()
        self.kafka = KafkaIntegration()
        self.processed_files = set()

    def run(self) -> None:
        """Run the watcher."""
        self.logger.info("Starting MinIO watcher.")
        while True:
            files = self.minio.fetch_new_files()
            new_files = set(files) - self.processed_files
            self.logger.info(f"New files: {new_files}")
            for file_key in new_files:
                data = self.minio.read(file_key)
                self.logger.info("Sending data to Kafka.")
                self.kafka.write({"file_key": file_key, "data": data}, "data_topic")
                self.logger.info("Data sent to Kafka successfully.")
                self.processed_files.add(file_key)
            time.sleep(2)


if __name__ == "__main__":
    watcher = MinioWatcher()
    watcher.run()
