from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

API_KEY = "qcDIchwFthiRegPA4FarvCcBXfT7Hj2zJERKd27tppM2"  # Replace with your actual API key
PROJECT_ID = "95bcebb4-c0be-4790-b245-de09ae72ea47"       # Replace with your actual project ID from Watsonx
REGION = "us-south"  # Change based on your IBM Cloud region if needed

# Set up authenticator
authenticator = IAMAuthenticator(apikey=API_KEY)

# Initialize Granite model - FIXED VERSION
granite = ModelInference(
    model_id="ibm/granite-3-2b-instruct",
    credentials={
        "url": f"https://{REGION}.ml.cloud.ibm.com",
        "apikey": API_KEY
    },
    project_id=PROJECT_ID,  # Move project_id here as a separate parameter
    params={}
)

def granite_generate_response(prompt):
    try:
        response = granite.generate(prompt, params={GenParams.MAX_NEW_TOKENS: 500})
        return response['results'][0]['generated_text']
    except Exception as e:
        return f"[Error generating response: {str(e)}]"

def analyze_sentiment(text):
    if "good" in text.lower():
        return "Positive"
    elif "bad" in text.lower():
        return "Negative"
    else:
        return "Neutral"