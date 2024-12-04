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
        if isinstance(event.get('body'), str):
            data = json.loads(event['body'])
        else:
            data = event.get('body', {})

        presentation = data["presentation"]
        index = data["index"]

        
        unique_filename = f"{uuid.uuid4()}.pptx"
        file_path = os.path.join("/tmp", unique_filename)

        response = requests.get(presentation)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        decomposer_obj = PresentationDecomposer()

        logger.info(f"Uploaded file saved to {file_path}")
        result_json = decomposer_obj.process_presentation(file_path, index)
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
        import traceback
        logger.error(f"Stack trace: {''.join(traceback.format_tb(e.__traceback__))}")
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
    data = handler({"body": json.dumps({
        "index": 0,
        "presentation": "https://pub-7c765f3726084c52bcd5d180d51f1255.r2.dev/Your%20big%20idea.pptx"}), "context": {}}, {})
    print(data)