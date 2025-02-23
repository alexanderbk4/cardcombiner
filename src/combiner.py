import os
from PIL import Image, ExifTags

def get_exif_orientation(image):
    """Get the EXIF orientation tag from an image if it exists."""
    try:
        # Find the orientation tag
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        
        exif = image._getexif()
        if exif is not None:
            return exif.get(orientation)
    except (AttributeError, KeyError, IndexError):
        pass
    return None

def correct_image_orientation(image):
    """Correct image orientation based on EXIF data."""
    orientation = get_exif_orientation(image)
    
    if orientation is None:
        return image
    
    # Orientation values and their corresponding operations
    # 1: Normal (no rotation needed)
    # 3: 180 degree rotation
    # 6: 90 degree rotation
    # 8: 270 degree rotation
    
    if orientation == 3:
        return image.rotate(180, expand=True)
    elif orientation == 6:
        return image.rotate(270, expand=True)
    elif orientation == 8:
        return image.rotate(90, expand=True)
    return image

def move_images(output_filename, pair):
    os.rename(pair['front'], os.path.join('processed-source', pair['front']))
    os.rename(pair['back'], os.path.join('processed-source', pair['back']))
    os.rename(output_filename, os.path.join('processed-combined', output_filename))
    

def combine_images(folder_path):
    """
    Combines matching front and back images from a folder into side-by-side images.
    Front images end with 'F' and back images end with 'B'.
    Handles image orientation correctly using EXIF data.
    """
    # Get all image files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    # Create a dictionary to store matching pairs
    pairs = {}
    
    # Group matching files
    for file in files:
        base = file[:-6]  # Remove last letter and extension
        if file.endswith('F.jpg'):
            if base not in pairs:
                pairs[base] = {'front': None, 'back': None}
            pairs[base]['front'] = file
        elif file.endswith('B.jpg'):
            if base not in pairs:
                pairs[base] = {'front': None, 'back': None}
            pairs[base]['back'] = file

    # Process each pair
    for base, pair in pairs.items():
        if pair['front'] and pair['back']:
            print(pair['front'])
            print(pair['back'])
            print(base)
            # Open and correct orientation for both images
            front_img = Image.open(os.path.join(folder_path, pair['front']))
            front_img = correct_image_orientation(front_img)
            
            back_img = Image.open(os.path.join(folder_path, pair['back']))
            back_img = correct_image_orientation(back_img)
            
            # Ensure both images are the same size (3000x4000)
            front_img = front_img.resize((3000, 4000), Image.Resampling.LANCZOS)
            back_img = back_img.resize((3000, 4000), Image.Resampling.LANCZOS)
            
            # Create a new blank image with double width
            combined = Image.new('RGB', (6000, 4000))
            
            # Paste the images side by side
            combined.paste(front_img, (0, 0))
            combined.paste(back_img, (3000, 0))
            
            # Save the combined image
            output_filename = f"{base}.jpg"
            combined.save(os.path.join(folder_path, output_filename), 
                        'JPEG', 
                        quality=95, 
                        dpi=(72, 72))
            
            print(f"Created combined image: {output_filename}")
            move_images(output_filename, pair)
        else:
            print(f"Warning: Missing matching pair for {base}")

def main():
    # Replace with your folder path
    folder_path = os.getcwd()
    
    if not os.path.exists(folder_path):
        print(f"Error: Folder {folder_path} does not exist")
        return
        
    combine_images(folder_path)
    print("Processing complete!")

if __name__ == "__main__":
    main()