from google import genai
from google.genai import types
from django.conf import settings
from PIL import Image
from io import BytesIO

def get_image_description(image_file):
    """
    Calls the Gemini API to generate a description for an image file.

    :param image_file: An InMemoryUploadedFile (from DRF/Django request.FILES)
    :return: The generated text description or an error message.
    """
    if not settings.GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not configured."

    try:
        # 1. Initialize the client
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
        # 2. Read the image file content into a BytesIO object
        # This allows us to work with the image data without saving it
        # to the file system first.
        image_bytes_io = BytesIO(image_file.read())
        
        # 3. Open the image using Pillow (PIL)
        # This step is crucial to get the correct MIME type and raw bytes.
        pil_image = Image.open(image_bytes_io)
        
        # 4. Convert the PIL Image back to a byte array for the API
        buffer = BytesIO()
        # Save to buffer using the original format or a common one like JPEG
        pil_image.save(buffer, format=pil_image.format or 'JPEG') 
        image_bytes = buffer.getvalue()
        
        # 5. Define the content parts
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=image_file.content_type  # Use the MIME type from Django
        )
        
        prompt_text = "Describe the image in a concise but detailed manner. Identify key objects and the scene."

        # 6. Call the Gemini API
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Fast and efficient for description tasks
            contents=[image_part, prompt_text]
        )
        
        return response.text.strip()
        
    except Exception as e:
        # Log the error for debugging
        print(f"Gemini API Error: {e}")
        return f"An error occurred during image analysis: {str(e)}"