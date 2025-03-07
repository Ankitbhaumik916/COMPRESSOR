import cv2
import numpy as np
import pickle
import os

def apply_dct(image):
    """Apply DCT on 8x8 blocks."""
    image = np.float32(image) - 128  # Normalize
    dct_image = np.zeros(image.shape)
    
    for i in range(0, image.shape[0], 8):
        for j in range(0, image.shape[1], 8):
            dct_image[i:i+8, j:j+8] = cv2.dct(image[i:i+8, j:j+8])
    
    return dct_image

def apply_idct(dct_image):
    """Apply inverse DCT (IDCT) to reconstruct the image."""
    idct_image = np.zeros(dct_image.shape)
    
    for i in range(0, dct_image.shape[0], 8):
        for j in range(0, dct_image.shape[1], 8):
            idct_image[i:i+8, j:j+8] = cv2.idct(dct_image[i:i+8, j:j+8])
    
    return np.clip(idct_image + 128, 0, 255).astype(np.uint8)

def compress_image():
    """Compress an image using DCT and save as .pkl with user input."""
    
    input_path = input("Enter the image path to compress: ").strip()
    if not os.path.exists(input_path):
        print("Error: File not found.")
        return
    
    image = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print("Error: Unable to read the image.")
        return
    
    try:
        quality = int(input("Enter compression quality (10-100): "))
        if not (10 <= quality <= 100):
            raise ValueError("Quality must be between 10 and 100.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        return
    
    output_file = input("Enter the name for the compressed file (without extension): ").strip() + ".pkl"
    
    dct_transformed = apply_dct(image)
    
    quant_matrix = np.ones((8, 8)) * (quality / 50)  # Adaptive compression
    quantized = np.zeros(dct_transformed.shape)

    # Apply quantization block-wise
    for i in range(0, dct_transformed.shape[0], 8):
        for j in range(0, dct_transformed.shape[1], 8):
            quantized[i:i+8, j:j+8] = np.round(dct_transformed[i:i+8, j:j+8] / quant_matrix)

    with open(output_file, "wb") as f:
        pickle.dump((quantized, image.shape, quant_matrix), f)

    print(f"✅ Image compressed and saved as {output_file}")

def decompress_image():
    """Decompress an image from .pkl file."""
    
    input_file = input("Enter the compressed file path (like(xyz.pkl)): ").strip()
    if not os.path.exists(input_file):
        print("Error: File not found.")
        return
    
    with open(input_file, "rb") as f:
        quantized, original_shape, quant_matrix = pickle.load(f)

    dequantized = np.zeros(original_shape)

    # Dequantization block-wise
    for i in range(0, original_shape[0], 8):
        for j in range(0, original_shape[1], 8):
            dequantized[i:i+8, j:j+8] = quantized[i:i+8, j:j+8] * quant_matrix

    decompressed_image = apply_idct(dequantized)

    output_image = input("Enter the name for the decompressed image (with extension, e.g., output.jpg): ").strip()
    
    cv2.imwrite(output_image, decompressed_image)
    print(f"✅ Image decompressed and saved as {output_image}")

while True:
    print("\nOptions:")
    print("1. Compress an Image")
    print("2. Decompress an Image")
    print("3. Exit")
    
    choice = input("Enter your choice (1/2/3): ").strip()
    
    if choice == "1":
        compress_image()
    elif choice == "2":
        decompress_image()
    elif choice == "3":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
