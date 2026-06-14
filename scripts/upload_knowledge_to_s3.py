"""
One-time script to upload the landright knowledge base to S3.
Run this once: python scripts/upload_knowledge_to_s3.py
"""

import json
import sys
import os
import boto3
from pathlib import Path

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.knowledge.content import KNOWLEDGE_BASE
from backend.core.config import settings


def upload_knowledge_base():
    s3 = boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    # Create bucket if it doesn't exist
    existing_buckets = [b["Name"] for b in s3.list_buckets()["Buckets"]]
    if settings.s3_bucket_name not in existing_buckets:
        if settings.aws_region == "us-east-1":
            s3.create_bucket(Bucket=settings.s3_bucket_name)
        else:
            s3.create_bucket(
                Bucket=settings.s3_bucket_name,
                CreateBucketConfiguration={"LocationConstraint": settings.aws_region},
            )
        print(f"Created S3 bucket: {settings.s3_bucket_name}")
    else:
        print(f"Bucket already exists: {settings.s3_bucket_name}")

    # Upload knowledge base as JSON
    s3.put_object(
        Bucket=settings.s3_bucket_name,
        Key="knowledge_base.json",
        Body=json.dumps(KNOWLEDGE_BASE, indent=2).encode("utf-8"),
        ContentType="application/json",
    )

    print(f"Uploaded {len(KNOWLEDGE_BASE)} knowledge base entries to s3://{settings.s3_bucket_name}/knowledge_base.json")


if __name__ == "__main__":
    upload_knowledge_base()
