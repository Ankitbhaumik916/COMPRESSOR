import cv2
import numpy as np
import pickle

# More Aggressive Quantization Matrix (Higher Values = More Compression)
quantization_matrix = np.array([
    [32, 24, 20, 32, 48, 80, 102, 122],  
    [24, 26, 28, 38, 52, 116, 120, 110],  
    [28, 26, 32, 48, 80, 114, 138, 112],  
    [28, 34, 44, 58, 102, 174, 160, 124],  
    [36, 44, 74, 112, 136, 218, 206, 154],  
    [48, 70, 110, 128, 162, 208, 226, 184],  
    [98, 128, 156, 174, 206, 242, 240, 202],  
    [144, 184, 190, 196, 224, 200, 206, 198]  
])

# Function to Apply DCT and Zero Out High Frequencies
def apply_dct(image, keep_ratio=0.2):  
    h, w = image.shape
    dct_blocks = np.zeros((h, w), dtype=np.float32)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = image[i:i+8, j:j+8].astype(np.float32) - 128
            dct_block = cv2.dct(block)

            # Keep Only a Fraction of DCT Coefficients
            threshold = np.percentile(np.abs(dct_block), (1 - keep_ratio) * 100)
            dct_block[np.abs(dct_block) < threshold] = 0  # Zero Out Small Coefficients
            
            dct_blocks[i:i+8, j:j+8] = dct_block

    return dct_blocks

# Function to Apply IDCT
def apply_idct(dct_blocks):
    h, w = dct_blocks.shape
    image_reconstructed = np.zeros((h, w), dtype=np.float32)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            block = dct_blocks[i:i+8, j:j+8]
            image_reconstructed[i:i+8, j:j+8] = cv2.idct(block) + 128

    return np.clip(image_reconstructed, 0, 255).astype(np.uint8)

# Function to Compress Image with Higher Compression
def compress_image(image_path, compressed_file):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at {image_path}.")
        return

    h, w, c = image.shape
    compressed_data = {}

    for channel in range(c):
        dct_transformed = apply_dct(image[:, :, channel], keep_ratio=0.15)  # Keep only 15% coefficients

        quantized = np.zeros((h, w), dtype=np.float32)
        for i in range(0, h, 8):
            for j in range(0, w, 8):
                quantized[i:i+8, j:j+8] = np.round(dct_transformed[i:i+8, j:j+8] / quantization_matrix)

        compressed_data[channel] = quantized

    # Save compressed data
    with open(compressed_file, 'wb') as f:
        pickle.dump((compressed_data, h, w, c), f)

    print("✅ High Compression Done!")

# Function to Decompress Image
def decompress_image(compressed_file, output_path):
    with open(compressed_file, 'rb') as f:
        compressed_data, h, w, c = pickle.load(f)

    decompressed_image = np.zeros((h, w, c), dtype=np.uint8)

    for channel in range(c):
        dequantized = np.zeros((h, w), dtype=np.float32)

        for i in range(0, h, 8):
            for j in range(0, w, 8):
                dequantized[i:i+8, j:j+8] = compressed_data[channel][i:i+8, j:j+8] * quantization_matrix

        decompressed_image[:, :, channel] = apply_idct(dequantized)

    cv2.imwrite(output_path, decompressed_image)
    print("✅ Decompression Done! Saved as:", output_path)

# Run Compression & Decompression
compress_image("as.png", "compressed_high.pkl")
decompress_image("compressed_high.pkl", "output_high_compression.png")
