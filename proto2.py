import cv2
import numpy as np
import pickle

# Define Quantization Matrix
DEFAULT_QUANTIZATION_MATRIX = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]
], dtype=np.float32)


def apply_dct(image_channel):
    """Applies DCT to image channel in 8x8 blocks."""
    h, w = image_channel.shape
    dct_image = np.zeros((h, w), dtype=np.float32)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            dct_image[i:i+8, j:j+8] = cv2.dct(np.float32(image_channel[i:i+8, j:j+8]) - 128)
    
    return dct_image


def quantize_dct(dct_transformed, quantization_matrix):
    """Quantizes DCT coefficients."""
    h, w = dct_transformed.shape
    quantized = np.zeros((h, w), dtype=np.float32)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            quantized[i:i+8, j:j+8] = np.round(dct_transformed[i:i+8, j:j+8] / quantization_matrix)
    
    return quantized


def compress_image(input_image_path, output_file, compression_level):
    """Compresses an image (color or grayscale) using DCT and saves it."""
    image = cv2.imread(input_image_path)

    if image is None:
        raise FileNotFoundError("Error: Image not found or path is incorrect!")

    height, width, channels = image.shape

    # Adjust Quantization Matrix Based on Compression Level
    quantization_matrix = DEFAULT_QUANTIZATION_MATRIX * compression_level

    compressed_data = []
    for c in range(channels):
        dct_transformed = apply_dct(image[:, :, c])
        quantized = quantize_dct(dct_transformed, quantization_matrix)
        compressed_data.append(quantized)

    # Save compressed data
    with open(output_file, 'wb') as f:
        pickle.dump((compressed_data, height, width, channels, quantization_matrix), f)

    print(f"✅ Compression completed! Saved to {output_file}")


def apply_idct(transformed):
    """Applies Inverse DCT in 8x8 blocks."""
    h, w = transformed.shape
    idct_image = np.zeros((h, w), dtype=np.float32)

    for i in range(0, h, 8):
        for j in range(0, w, 8):
            idct_image[i:i+8, j:j+8] = cv2.idct(transformed[i:i+8, j:j+8])

    return np.clip(idct_image + 128, 0, 255).astype(np.uint8)


def decompress_image(compressed_file, output_image_path):
    """Decompresses a previously compressed image and saves it."""
    with open(compressed_file, 'rb') as f:
        compressed_data, height, width, channels, quantization_matrix = pickle.load(f)

    decompressed_channels = []
    for c in range(channels):
        dequantized = np.zeros((height, width), dtype=np.float32)

        for i in range(0, height, 8):
            for j in range(0, width, 8):
                dequantized[i:i+8, j:j+8] = compressed_data[c][i:i+8, j:j+8] * quantization_matrix

        reconstructed = apply_idct(dequantized)
        decompressed_channels.append(reconstructed)

    # Merge channels and save decompressed image
    decompressed_image = cv2.merge(decompressed_channels)
    cv2.imwrite(output_image_path, decompressed_image)

    print(f" Decompression completed! Saved to {output_image_path}")


# ======== USER INTERFACE ========
if __name__ == "__main__":
    img_path = input("Enter input image path: ")
    compressed_path = "compressed.pkl"
    decompressed_path = "decompressed.jpg"

    compression_level = float(input("Enter compression level (1 = high quality, 5 = more compression): "))

    compress_image(img_path, compressed_path, compression_level)
    decompress_image(compressed_path, decompressed_path)

    print(" Process Completed! Check the decompressed image.")
