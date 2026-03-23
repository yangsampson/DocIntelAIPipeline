import boto3
import cv2

def get_signature_crop(img_color):

    """
    Detects a signature using AWS Textract and returns the cropped image array.
    """
    textract = boto3.client('textract')
    
    # 1. Convert OpenCV image (numpy array) to bytes for Textract
    _, buffer = cv2.imencode('.png', img_color)
    image_bytes = buffer.tobytes()

    # 2. Request Signature Detection
    response = textract.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=["SIGNATURES"]
    )

    height, width = img_color.shape[:2]
    
    # 3. Find the first Signature Block
    for block in response.get("Blocks", []):
        if block["BlockType"] == "SIGNATURE":
            box = block['Geometry']['BoundingBox']
            
            # Convert normalized coordinates to pixel locations
            left = int(width * box['Left'])
            top = int(height * box['Top'])
            right = int(left + (width * box['Width']))
            bottom = int(top + (height * box['Height']))

            # Return the cropped signature
            return img_color[top:bottom, left:right]

    # # Return None if no signature is found
    return None
