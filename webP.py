import cv2
import os

def compress_to_webp():
    #Compress an image to WebP with user-defined quality and filename.
    
    # Get user input for image path
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
    output_filename = input("Enter the name for the compressed image (without extension): ").strip()
    output_path = output_filename + ".webp"
    try:
        quality = int(input("Enter compression quality (0-100): "))
        if not (0 <= quality <= 100):
            raise ValueError("Quality must be between 0 and 100.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    cv2.imwrite(output_path, image, [cv2.IMWRITE_WEBP_QUALITY, quality])
    print(f" Image compressed and saved as {output_path} with quality {quality}")
compress_to_webp()

def decompress_webp():
    """Decompress a WebP image and save it in the chosen format."""
    
    # Get user input for image path
    input_path = input("Enter the path of the WebP image to decompress: ").strip()
    
    # Check if the file exists
    if not os.path.exists(input_path):
        print("Error: File not found. Please enter a valid path.")
        return

    # Load the WebP image
    image = cv2.imread(input_path)
    if image is None:
        print("Error: Unable to read the WebP file.")
        return

    # Get user input for output filename and format
    output_filename = input("Enter the name for the decompressed image (without extension): ").strip()
    output_format = input("Enter the output format (jpg/png): ").strip().lower()
    
    if output_format not in ["jpg", "png"]:
        print("Error: Unsupported format. Choose 'jpg' or 'png'.")
        return
    
    output_path = output_filename + "." + output_format
    
    # Save decompressed image
    cv2.imwrite(output_path, image)
    print(f"Decompressed image saved as {output_path}")

# Run the function
decompress_webp()
