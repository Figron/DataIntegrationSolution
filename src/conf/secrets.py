"""Emulates the cloud secrets module. This would be replaced by a real cloud secrets module in a real application."""


def return_minio_secrets() -> dict:
    """Return MinIO secrets."""
    return {
        "aws_access_key_id": "minioadmin",
        "aws_secret_access_key": "minioadmin",
    }
