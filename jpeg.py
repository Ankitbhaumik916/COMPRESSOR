import cv2
import os
#JPEG COMPRESSION
def compress_to_jpeg():

    input_path = input("Enter the path of the image to compress: ").strip()
    
    # Check if the file exists
    if not os.path.exists(input_path):
        print("Error: File not found. Please enter a valid path.")
        return
    
    # Load the image
    image = cv2.imread(input_path)
    if image is None:
        print("Error: Unable to read the image file. Check the path.")
        return
    
    # Get user input for output filename
    output_filename = input("Enter the name for the compressed image (without extension): ").strip()
    output_path = output_filename + ".jpg"
    
    # Get user input for compression quality
    try:
        quality = int(input("Enter compression quality (0-100): "))
        if not (0 <= quality <= 100):
            raise ValueError("Quality must be between 0 and 100.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    
    # Compress and save as JPEG
    cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
    print(f"✅ Image compressed and saved as {output_path} with quality {quality}")

# Run the function
compress_to_jpeg()

def decompress_jpeg():
    """Decompress a JPEG image and save it in PNG or BMP format."""
    
    # Get user input for image path
    input_path = input("Enter the path of the JPEG image to decompress: ").strip()
    
    # Check if the file exists
    if not os.path.exists(input_path):
        print("Error: File not found. Please enter a valid path.")
        return

    # Load the JPEG image
    image = cv2.imread(input_path)
    if image is None:
        print("Error: Unable to read the JPEG file.")
        return

    # Get user input for output filename and format
    output_filename = input("Enter the name for the decompressed image (without extension): ").strip()
    output_format = input("Enter the output format (png/bmp): ").strip().lower()
    
    if output_format not in ["png", "bmp"]:
        print("Error: Unsupported format. Choose 'png' or 'bmp'.")
        return
    
    output_path = output_filename + "." + output_format
    
    # Save decompressed image
    cv2.imwrite(output_path, image)
    print(f"✅ Decompressed image saved as {output_path}")

# Run the function
decompress_jpeg()
