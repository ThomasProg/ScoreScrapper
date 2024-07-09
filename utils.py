import os
import requests
from pdf2image import convert_from_path
import pdf2image
from tqdm import tqdm

# Function to download a file from a URL
def download_file(url, directory='downloads'):
    if not os.path.exists(directory):
        os.makedirs(directory)
    local_filename = os.path.join(directory, url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def pdf_to_png(pdf_path, output_folder, dpi=300):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    poppler_path="C:/Users/Utilisateur/Downloads/Poppler/poppler-24.02.0/Library/bin"

    # # Convert PDF to a list of images
    # images = convert_from_path(pdf_path, dpi=dpi, poppler_path="C:/Users/Utilisateur/Downloads/Poppler/poppler-24.02.0/Library/bin")

    # # Save each image as PNG
    # for i, image in enumerate(images):
    #     output_path = os.path.join(output_folder, f'page_{i + 1}.png')
    #     image.save(output_path, 'PNG')
    #     print(f'Saved {output_path}')

    # Get the total number of pages in the PDF
    pdf_info = pdf2image.pdfinfo_from_path(pdf_path, poppler_path=poppler_path)
    total_pages = pdf_info["Pages"]

    print(f"Total pages: {total_pages}")
    print("Output folder: ", output_folder)
    print("Converting PDF to images...")

    # Convert each page individually with progress indication
    for page_number in tqdm(range(1, total_pages + 1), desc="Converting pages"):
        images = convert_from_path(pdf_path, dpi=dpi, first_page=page_number, last_page=page_number, poppler_path=poppler_path)
        for i, image in enumerate(images):
            output_path = os.path.join(output_folder, f'page_{page_number}.png')
            image.save(output_path, 'PNG')

from music21 import converter, midi

def convert_musicxml_to_midi(mxl_path, midi_path):
    # Load the MusicXML file
    score = converter.parse(mxl_path)

    # Convert to MIDI
    midi_file = midi.translate.music21ObjectToMidiFile(score)

    # Save MIDI file
    midi_file.open(midi_path, 'wb')
    midi_file.write()
    midi_file.close()

    print(f"Converted {mxl_path} to {midi_path}")

