import boto3
from langchain_aws import ChatBedrock
from backend.core.config import settings


def get_llm():
    bedrock_client = boto3.client(
        service_name="bedrock-runtime",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )

    return ChatBedrock(
        client=bedrock_client,
        model_id=settings.bedrock_model_id,
        model_kwargs={"temperature": 0.3, "max_gen_len": 1024},
    )
