from django.http import StreamingHttpResponse
import face_recognition as fr
import numpy as np
import cv2
import requests


def generate_frames(camera):
    print("Iniciando o loop de geração de frames...")
    # Load the stored image from URL
    imagem_armazenada_url = "http://127.0.0.1:8000/media/media/imagem-armazenada.png"
    response = requests.get(imagem_armazenada_url)

    if response.status_code == 200:
        imagem_armazenada_bytes = response.content
        imagem_armazenada_array = np.frombuffer(imagem_armazenada_bytes, np.uint8)
        imagem_armazenada = cv2.imdecode(imagem_armazenada_array, cv2.IMREAD_COLOR)
        imagem_armazenada_rgb = cv2.cvtColor(imagem_armazenada, cv2.COLOR_BGR2RGB)
        encondings_imagem_armazenada = fr.face_encodings(imagem_armazenada_rgb)[0]
    else:
        # Trate o caso em que a imagem armazenada não pode ser carregada
        # Aqui você pode optar por retornar uma resposta de erro ou fazer outra ação adequada
        raise Exception("Erro ao carregar a imagem armazenada")

    autenticado = False  # Variável para controlar o status de autenticação

    while True:
        print("Capturando frame...")
        success, frame = camera.read()
        if not success:
            print("Não foi possível capturar o frame. Saindo do loop.")
            break
        else:
            print("Frame capturado. Processando...")

            # Detecte as localizações dos rostos no frame
            face_locations = fr.face_locations(frame)

            # Desenha retângulos ao redor das faces encontradas
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                print('criou moldura')

                # Faz encoding do frame da câmera
                encondings_camera = fr.face_encodings(frame, face_locations)[0]
                print('passou pelo encondings')

                # Faz a comparação de faces
                comparacao = fr.face_distance([encondings_imagem_armazenada], encondings_camera)
                print('A comparação é = ', comparacao)
                if comparacao < [0.6]:
                    autenticado = True
                    print('Liberado')
                    break
                if comparacao > [0.6]:
                    autenticado = False
                    print('Recusado')

            # Converta o frame de volta para o formato BGR para exibição correta com OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            ret, buffer = cv2.imencode('.png', frame)
            frame = buffer.tobytes()
            if ret:
                print("Enviando frame...")
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            if autenticado:
                print("Usuário autenticado. Saindo do loop.")
                return  # Retorna se estiver autenticado


def index(request):
    # Captura o video da cam
    cap = cv2.VideoCapture(0)
    # Definindo o tamanho do frame
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    return StreamingHttpResponse(generate_frames(cap), content_type='multipart/x-mixed-replace; boundary=frame')
