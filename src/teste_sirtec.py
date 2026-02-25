import fitz  # PyMuPDF
from PIL import Image, ImageChops
import os


def pdf_to_images(page_name, pdf_path, output_folder, format_choice, zoom=2.0):
    try:
        # Abrir o arquivo PDF
        doc = fitz.open(pdf_path)
        
        # Criar a pasta de saída, se não existir
        os.makedirs(output_folder, exist_ok=True)
        
        # Verificar o formato escolhido
        format_map = {1: "PNG", 2: "JPEG"}
        output_format = format_map.get(format_choice, "PNG")
        
        print(f"Convertendo PDF para imagens no formato {output_format}...")

        for page_num in range(len(doc)):
            page = doc[page_num]  # Carregar página
            
            # Ajustar resolução da renderização
            mat = fitz.Matrix(zoom, zoom)  # Aumenta a qualidade em múltiplos de zoom
            pix = page.get_pixmap(matrix=mat, alpha=False)  # Renderizar com alta qualidade
            
            # Salvar a imagem no formato escolhido
            #output_path = os.path.join(output_folder, f"{page_name}_page_{page_num + 1}.{output_format.lower()}")
            output_path = os.path.join(output_folder, f"{page_name}.{output_format.lower()}")
            pix.save(output_path)
            
            print(f"Página {page_num + 1} salva em {output_path}")
            
            # Recortar bordas da imagem
            crop_image(output_path, output_format)
        
        print("Processo concluído!")
    except Exception as e:
        print(f"Erro: {e}")


def crop_image(image_path, output_format):
    try:
        # Abrir a imagem com Pillow
        img = Image.open(image_path)
        
        # Criar uma imagem branca do mesmo tamanho
        bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
        
        # Subtrair a imagem de fundo para detectar áreas não brancas
        diff = ImageChops.difference(img, bg)
        bbox = diff.getbbox()
        
        if bbox:
            img_cropped = img.crop(bbox)  # Recortar as bordas
            # Salvar a imagem recortada em alta qualidade
            if output_format == "JPEG":
                img_cropped.save(image_path, format=output_format, quality=95)  # JPEG com alta qualidade
            else:
                img_cropped.save(image_path, format=output_format)  # PNG sem compressão
            print(f"Bordas recortadas: {image_path}")
    except Exception as e:
        print(f"Erro ao recortar bordas: {e}")


if __name__ == "__main__":
    pdf_to_images("grafico_geral", 'G:/Drives compartilhados/PCP/Time Inovação/Soluções/BI - Painel RH/Bases/E-mail/Gerador/BAR/grafico_geral.pdf', 'ponto_mais/analysis/BAR', 1, zoom=3.0)
