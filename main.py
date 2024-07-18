import cv2
import numpy as np
import os

#_________________________ Calcula a Normalized Cross-Correlation (NCC) entre duas imagens. ________________________#

def calculate_ncc(imagem1, imagem2):

    imagem1_gray = cv2.cvtColor(imagem1, cv2.COLOR_BGR2GRAY)
    imagem2_gray = cv2.cvtColor(imagem2, cv2.COLOR_BGR2GRAY)

    if imagem1_gray.shape != imagem2_gray.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")

    mean1, stddev1 = cv2.meanStdDev(imagem1_gray)
    mean2, stddev2 = cv2.meanStdDev(imagem2_gray)

    mean1, stddev1 = mean1[0][0], stddev1[0][0]
    mean2, stddev2 = mean2[0][0], stddev2[0][0]

    imagem1_normalized = (imagem1_gray - mean1) / stddev1 if stddev1 != 0 else imagem1_gray - mean1
    imagem2_normalized = (imagem2_gray - mean2) / stddev2 if stddev2 != 0 else imagem2_gray - mean2

    ncc = np.mean(imagem1_normalized * imagem2_normalized)
    return ncc

#___________________________________________ Calcula a velocidade média. ___________________________________________#

def calcular_velocidade_media(distancia, tempo):

    if tempo <= 0:
        raise ValueError("O tempo precisa ser maior que zero")
    velocidade_media_m_s = distancia / tempo
    velocidade_media_km_h = velocidade_media_m_s * 3.6

    return velocidade_media_m_s, velocidade_media_km_h

#______________________________________ Função para receber arquivo de vídeo. ______________________________________#

def load_video(video_path):
    
    # Verifica se o arquivo de video existe.
    if not os.path.exists(video_path):
        raise ValueError("O arquivo de vídeo não existe. Verifique o caminho do arquivo.")
    
    cap = cv2.VideoCapture(video_path)

    # Verifica se o video foi aberto corretamente.
    if not cap.isOpened():  
        raise ValueError("Erro ao abrir o vídeo. Verifique o caminho do arquivo.")
    return cap

#_________________________________ Função para extrair metadados básicos do vídeo. _________________________________#

def get_video_metadata(video_cap):

    fps = video_cap.get(cv2.CAP_PROP_FPS)
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    return {
        "FPS": fps,
        "Resolução": (width, height),
        "Duração (s)": duration,
        "Total de quadros": frame_count
    }

#________________________________ Função para extrair frames específicos do vídeo. _________________________________#

def extract_frame(video_cap, frame_number):

    total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if frame_number < 0 or frame_number >= total_frames:
        raise ValueError(f"O número do quadro deve estar entre 0 e {total_frames - 1}")

    video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    ret, frame = video_cap.read()
    if not ret:
        raise ValueError("Erro ao ler o quadro do vídeo. Verifique o número do quadro.")
    return frame

#_________________________________ Função para sobrepor dois quadros em uma imagem._________________________________#

def overlay_images(imagemA, transparencyA, imagemB, transparencyB):

    if imagemA.shape != imagemB.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")
    overlay = cv2.addWeighted(imagemA, transparencyA, imagemB, transparencyB, 0)
    return overlay

#_____________________________________ Função para salvar a imagem sobreposta. _____________________________________#

def save_image(image, output_path):

    cv2.imwrite(output_path, image)
    print(f"Imagem salva em: {output_path}")

#______________________________________ Função para adicionar texto à imagem. ______________________________________#

def add_text_to_image(image, text, position, font_scale=0.5, font_color=(0, 255, 255), font_thickness=1):

    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

#___________________________ Função de callback para capturar clique de mouse na imagem. ___________________________#

def mouse_click(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Clique detectado nas coordenadas (x, y): ({x}, {y})")
        param['clicked_point'] = (x, y)

#_______________________________ Função para calcular distância euclidiana em pixels._______________________________#

def calculate_distance(x1, y1, x2, y2):

    distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

# Função para sobrepor dois quadros em uma imagem
def overlay_images(imagemA, transparencyA, imagemB, transparencyB):
    if imagemA.shape != imagemB.shape:
        raise ValueError("As imagens possuem tamanhos diferentes")
    overlay = cv2.addWeighted(imagemA, transparencyA, imagemB, transparencyB, 0)
    return overlay

# Função para salvar a imagem sobreposta
def save_image(image, output_path):
    cv2.imwrite(output_path, image)
    print(f"Imagem salva em: {output_path}")

# Função para adicionar texto à imagem
def add_text_to_image(image, text, position, font_scale=0.5, font_color=(0, 255, 255), font_thickness=1):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)
# Função de callback para capturar clique de mouse na imagem

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 'image_name' in param and param['image_name'] == 'Imagem Sobreposta':
            print(f"Clique detectado nas coordenadas (x, y): ({x}, {y})")
            param['marked_points'].append((x, y))
            cv2.circle(param['image'], (x, y), 5, (0, 255, 255), -1)

# Função para pintar na imagem

def paint_on_image(image, image_name):
    cv2.imshow(image_name, image)
    print("Pinte círculos vermelhos nos pontos desejados. Pressione 'Esc' para terminar e continuar.")
    marked_points = []
    mouse_params = {'image_name': image_name, 'image': image, 'marked_points': marked_points}
    cv2.setMouseCallback(image_name, mouse_click, mouse_params)
    while True:
        cv2.imshow(image_name, image)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # Pressione 'Esc' para sair
            break
    cv2.destroyAllWindows()
    return marked_points

#________________________________________________ Função principal ________________________________________________#

def main():

    # Carregar as imagens
    imagem1 = cv2.imread("C:/Users/Plugify/Documents/Edson_Estagiario/Pericia/Razao_Cruzada/Midia/IMAGEM_A.jpeg")
    imagem2 = cv2.imread("C:/Users/Plugify/Documents/Edson_Estagiario/Pericia/Razao_Cruzada/Midia/IMAGEM_B.jpeg")

    if imagem1 is None or imagem2 is None:
        raise ValueError("Erro ao carregar as imagens. Verifique os caminhos dos arquivos.")

    # Calcular o NCC entre as imagens
    ncc_value = calculate_ncc(imagem1, imagem2)
    print(f"Cross-Correlation: {ncc_value}")

    distancia_percorrida = float(input("Digite a distância percorrida em metros: "))
    tempo_gasto = float(input("Digite o tempo gasto em segundos: "))

    try:
        velocidade_media_m_s, velocidade_media_km_h = calcular_velocidade_media(distancia_percorrida, tempo_gasto)
        print(f"Velocidade média: {velocidade_media_m_s} metros por segundo")
        print(f"Velocidade média: {velocidade_media_km_h} quilômetros por hora")
    except ValueError as e:
        print(f"Erro ao calcular velocidade média: {e}")

    # Configurar callback para captura de clique de mouse
    cv2.namedWindow('Imagem Sobreposta')  # Cria uma janela com o nome 'Imagem Sobreposta'
    mouse_params = {'clicked_point': None}  # Parâmetros que serão passados para a função de callback
    cv2.setMouseCallback('Imagem Sobreposta', mouse_click, mouse_params)  # Define a função de callback

    # Caminho do video
    video_path = 'C:/Users/Plugify/Documents/Edson_Estagiario/Pericia/Razao_Cruzada/Midia/VIDEO.mp4'
    print(f"Verificando o caminho do vídeo: {video_path}")
    print(f"O arquivo existe? {os.path.exists(video_path)}")

    # Carregar o video
    try:
        video_cap = load_video(video_path)
    except ValueError as e:
        print(e)
        return

    # Obter metadados do video
    metadata = get_video_metadata(video_cap)
    print("Metadados do vídeo:", metadata)

    # Extrair frames especificos
    frame_number1 = 17
    frame_number2 = 20

    try:
        frame1 = extract_frame(video_cap, frame_number1)
        frame2 = extract_frame(video_cap, frame_number2)
    except ValueError as e:
        print(e)
        return

    # Sobrepor os frames
    overlay_image = overlay_images(frame1, 0.5, frame2, 0.5)

    # Adicionar texto à imagem sobreposta
    metadata_text = f"FPS: {metadata['FPS']}, Resolução: {metadata['Resolução'][0]}x{metadata['Resolução'][1]}, Duração: {metadata['Duração (s)']:.2f}s, Total de quadros: {metadata['Total de quadros']}"
    results_text = f"NCC: {ncc_value:.2f}, Velocidade média: {velocidade_media_m_s:.2f} m/s ({velocidade_media_km_h:.2f} km/h)"
    combined_text = metadata_text + " | " + results_text

    # Posição do texto na parte inferior da imagem
    text_position = (10, overlay_image.shape[0] - 10)

    # Adicionar texto à imagem
    combined_text = "Exemplo de texto combinado"
    add_text_to_image(overlay_image, combined_text, (10, overlay_image.shape[0] - 10))

    # Pintar na imagem
    marked_points = paint_on_image(overlay_image.copy(), 'Imagem Sobreposta')

    # Mostrar a imagem sobreposta
    cv2.imshow('Imagem Sobreposta', overlay_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Salvar a imagem sobreposta
    output_path = 'overlay_output.png'
    save_image(overlay_image, output_path)
    print(f"Imagem sobreposta salva em: {output_path}")

      # Mostrar os pontos marcados
    if marked_points:
        print("Pontos marcados (x, y):", marked_points)
    else:
        print("Nenhum ponto marcado.")

    # Capturar e mostrar o clique do mouse na imagem sobreposta
    clicked_point = mouse_params['clicked_point']
    if clicked_point:
        print(f"Clique do mouse na imagem sobreposta nas coordenadas (x, y): {clicked_point}")

    # Exemplo de cálculo de distância entre dois pontos
    x1, y1 = 100, 50
    x2, y2 = 200, 150
    distance_pixels = calculate_distance(x1, y1, x2, y2)
    print(f"Distância euclidiana entre pontos em pixels: {distance_pixels}")

if __name__ == "__main__":
    main()
