import subprocess
import os

def process_images_with_audiveris(audiveris_path, images_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    # List all image files
    image_files = [os.path.join(images_dir, f) for f in os.listdir(images_dir) if f.endswith('.png')]
    
    # Generate command for batch processing
    command = [audiveris_path, '-batch', '-export']
    command.extend(image_files)  # Add all image files to the command
    command.extend(['-output', output_dir])

    # Run the command
    subprocess.run(command, check=True)

# Paths
audiveris_path = 'C:/Program Files/Audiveris/bin/Audiveris.bat'
images_dir = 'downloads/pngs2'
output_dir = 'downloads/score2'

# Process images with Audiveris
process_images_with_audiveris(audiveris_path, images_dir, output_dir)