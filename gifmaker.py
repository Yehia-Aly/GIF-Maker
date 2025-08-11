from PIL import Image
import argparse
import os

def make_gif(input_folder, output_file, duration=200, loop=0):
    images = []
    # Load all images from the folder
    for filename in sorted(os.listdir(input_folder)):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_folder, filename)
            images.append(Image.open(img_path))
    
    # Save as GIF
    images[0].save(
        output_file,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop
    )
    print(f"✅ GIF saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="📸 Create GIF from images")
    parser.add_argument("input_folder", help="Folder containing images")
    parser.add_argument("output_file", help="Output GIF filename (e.g., 'output.gif')")
    parser.add_argument("--duration", type=int, default=200, help="Time per frame (ms)")
    parser.add_argument("--loop", type=int, default=0, help="Loop count (0 = infinite)")
    
    args = parser.parse_args()
    make_gif(args.input_folder, args.output_file, args.duration, args.loop)