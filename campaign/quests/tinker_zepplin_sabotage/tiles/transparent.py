import os
from PIL import Image

def is_close_to_white(pixel, threshold=10):
    # Check if each color channel (R, G, B) is close to white (255)
    return all(abs(255 - val) <= threshold for val in pixel[:3])

def replace_white_with_transparency(image_path, threshold=10):
    try:
        with Image.open(image_path) as img:
            # Convert the image to RGBA mode (with alpha channel)
            img = img.convert("RGBA")

            # Get the pixel data
            data = img.getdata()

            # Replace pixels close to white with transparent ones
            new_data = [(r, g, b, 0) if is_close_to_white((r, g, b), threshold) else (r, g, b, a) for r, g, b, a in data]

            # Update the image with the new pixel data
            img.putdata(new_data)

            # Save the modified image with transparency
            new_image_path = os.path.splitext(image_path)[0] + "_transparent.png"
            img.save(new_image_path)

            print(f"Transparency added to {image_path} and saved as {new_image_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main():
    current_directory = os.getcwd()
    for filename in os.listdir(current_directory):
        if filename.lower().endswith(".png"):
            image_path = os.path.join(current_directory, filename)
            replace_white_with_transparency(image_path, threshold=10)

if __name__ == "__main__":
    main()

