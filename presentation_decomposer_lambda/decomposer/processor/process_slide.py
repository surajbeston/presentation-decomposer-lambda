import json
import os
import uuid
import tempfile
import logging
import requests
import base64

from .decompose import PresentationDecomposer
from .validators import SlideStructure


logger = logging.getLogger(__name__)


def handler(event, context):
    try:
        # Handle both direct Lambda invocations and API Gateway events
        if isinstance(event.get('body'), str):
            data = json.loads(event['body'])
        else:
            data = event.get('body', {})

        presentation = data["presentation"]


        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.pptx"
        file_path = os.path.join(tempfile.gettempdir(), unique_filename)
        
        presentation_bytes = base64.b64decode(presentation)
        with open(file_path, 'wb') as f:
            f.write(presentation_bytes)

        decomposer_obj = PresentationDecomposer()
        
        logger.info(f"Uploaded file saved to {file_path}")
        result_json = decomposer_obj.process_presentation(file_path)
        # result_dict = json.loads(result_json)
        # validated_data = SlideStructure(**result_dict)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": result_json
        }
    except Exception as e:
        logger.error(f"Error processing presentation: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"error": str(e)})
        }


if __name__ == "__main__":
    data = handler({"body": json.dumps({"presentation": "https://pub-7c765f3726084c52bcd5d180d51f1255.r2.dev/Your%20big%20idea.pptx"}), "context": {}}, {})
    print(data)