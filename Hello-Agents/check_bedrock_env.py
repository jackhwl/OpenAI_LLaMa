import os
import sys
import json

print(f"Python executable: {sys.executable}")
print(f"Environment keys: {[k for k in os.environ.keys() if 'AWS' in k]}")

try:
    import boto3
    print(f"Boto3 version: {boto3.__version__}")
except ImportError:
    print("Boto3 NOT installed")
    sys.exit(1)

region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
print(f"Target Region: {region}")

try:
    client = boto3.client('bedrock-runtime', region_name=region)
    print("Bedrock client created.")
    
    model_id = "amazon.titan-embed-text-v1"
    print(f"Invoking model: {model_id}")
    
    body = json.dumps({"inputText": "health_check"})
    response = client.invoke_model(
        modelId=model_id,
        body=body
    )
    
    print("Invoke response received.")
    body_read = response['body'].read()
    result = json.loads(body_read)
    
    if 'embedding' in result:
        vec = result['embedding']
        print(f"Success! Vector dimension: {len(vec)}")
    else:
        print(f"Unexpected response structure: {result.keys()}")

except Exception as e:
    print(f"Error occurred: {e}")
    import traceback
    traceback.print_exc()

