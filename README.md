# Image Compression Project

## Overview
This project implements multiple techniques for image compression, providing efficient storage and transmission of image files. It includes various compression algorithms and formats, such as **Discrete Cosine Transform (DCT), JPEG, and WebP**.

## Features
- **DCT Compression (`dct.py`)**: Uses Discrete Cosine Transform to reduce image size while maintaining quality.
- **JPEG Compression (`jpeg.py`)**: Implements JPEG compression techniques for lossy image reduction.
- **Prototype Implementations (`proto.py`, `proto2.py`)**: Experimental algorithms for compression optimization.
- **WebP Compression (`webP.py`)**: Efficient WebP format compression for high-quality images at reduced sizes.
- **Sample Image (`as.png`)**: Test image used for validating compression techniques.

## Usage
### Setup
1. Install dependencies:
   ```sh
   pip install numpy opencv-python pillow
   ```
2. Run any script to compress an image:
   ```sh
   python dct.py input_image.jpg output_image.jpg
   ```

### Running WebP Compression
```sh
python webP.py input_image.jpg output_image.webp
```

### Running JPEG Compression
```sh
python jpeg.py input_image.jpg output_image_compressed.jpg
```

## Future Enhancements
- Add **GUI for user-friendly compression settings**
- Implement **lossless compression techniques**
- Explore **machine learning-based image enhancement**

---
Contributors: Ankit Bhaumik & Team

