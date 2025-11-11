import boto3
import json

def test_bedrock():
    client = boto3.client('bedrock-runtime', region_name='us-east-1')
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": "Hello! Can you confirm you're working?"}
        ]
    }
    
    try:
        response = client.invoke_model(
            # Use inference profile instead of direct model ID
            modelId='us.anthropic.claude-3-5-sonnet-20241022-v2:0',
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        print("✅ Success! Claude says:")
        print(result['content'][0]['text'])
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_bedrock()