import os
from docx import Document
from PIL import Image
import io

def get_images(docx_path, output_folder):
    print("Obtendo imagens do world e salvando em: " + output_folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = Document(docx_path)
    image_counter = 1

    for rel in doc.part.rels.values():
        if "image" in rel.target_ref:
            
            image_blob = rel.target_part.blob
            image_format = rel.target_part.content_type.split('/')[1] 
            image_temp = io.BytesIO(image_blob)
            image_name = f"imagem_{image_counter}.png"
            image_path = os.path.join(output_folder, image_name)

            try:
                with Image.open(image_temp) as img:
                    img.save(image_path, 'PNG')
                print(f"Imagem salva em: {image_path}")
                image_counter += 1
            except Exception as e:
                print(f"Erro ao salvar a imagem: {e}")
