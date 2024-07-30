"""A script to generate CSV files with flaws and send them to Minio."""
import logging
import random
import time
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from src.conf.integrations.minio_integration import MinioIntegration
from src.conf.utilities.logging_mixin import LoggingMixin


class CSVGenerator(LoggingMixin):
    """A class to generate CSV files with flaws."""

    def __init__(self):
        self.output_dir = Path("../../../source_data")
        self.day_counter = 0
        self.start_date = datetime.strptime("2023-01-01", "%Y-%m-%d")

        self.minio = MinioIntegration()

        self.output_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%y/%m/%d %H:%M:%S",
            level=logging.INFO,
        )

    @staticmethod
    def random_decision() -> bool:
        """Make a random decision between True and False.

        Returns
            bool: The random decision.

        """
        return random.choice([True, False])

    def generate_sales_data_with_flaws(self, target_date: datetime) -> None:
        """Generate sales data with flaws.

        Such as:
            - Invalid date format
            - Invalid quantity
            - Invalid price
            - Duplicated row
            - Outliers

        Args:
            target_date: The date to generate the data for.

        Returns: None

        """
        data = {
            "date": [target_date.strftime("%Y-%m-%d") if not self.random_decision() else "invalid_date"] * 4,
            "product": ["Product A", "Product B", "Product C", "Invalid Product"],
            "quantity": [10 + target_date.day if not self.random_decision() else 999999, "twenty", 15, -30],
            "price": [100, 200, 150, "three hundred"],
        }
        # TODO: Create more rows?

        sales_df = pd.DataFrame(data)

        if self.random_decision():
            duplicated_row = sales_df.iloc[0:1].copy()
            sales_df = pd.concat([sales_df, duplicated_row], ignore_index=True)

        self.save_to_minio(sales_df, f'sales_data_{target_date.strftime("%Y%m%d")}.csv')

    def save_to_minio(self, df_to_save: DataFrame, file_name: str) -> None:
        """Save the DataFrame to a CSV bytes object and send it to Minio.

        Args:
            df_to_save: The DataFrame to save.
            file_name: The name of the file.

        Returns: None

        """
        csv_buffer = BytesIO()
        df_to_save.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        self.minio.write(csv_buffer, file_name)
        self.logger.info(f"Uploaded {file_name} to MinIO bucket {self.minio.bucket_name}")

    def run(self) -> None:
        """Run the CSV generator."""
        self.logger.info("Starting CSV generator.")
        while True:
            current_date = self.start_date + timedelta(days=self.day_counter)
            self.generate_sales_data_with_flaws(current_date)
            self.day_counter += 1
            time.sleep(5)  # TODO change to higher value?


if __name__ == "__main__":
    generator = CSVGenerator()
    generator.run()
