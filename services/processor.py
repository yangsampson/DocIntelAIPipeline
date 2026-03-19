import cv2
import base64

def extract_elements(png_path):
    img = cv2.imread(png_path)
    height, width, _ = img.shape

    # 1. Perform the Cuts
    header_cut = img[0:int(height * 0.15), 0:width]
    footer_cut = img[int(height * 0.75):height, 0:width]

    # 2. Helper function to convert image to Base64
    def get_b64(image_array):
        _, buffer = cv2.imencode('.png', image_array)
        return base64.b64encode(buffer).decode('utf-8')

    # 3. Return ALL THREE to the frontend
    return {
        "header_text": "Header Data",
        "header_img": get_b64(header_cut),    # THE CUT
        "signature_text": "Signature Data",
        "signature_img": get_b64(footer_cut), # THE CUT
        "full_image": get_b64(img)            # THE FULL PAGE
    }
