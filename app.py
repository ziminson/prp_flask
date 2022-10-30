# save this as app.py
# подключаем всякое-разное
from flask import Flask, render_template, Response, request
import cv2
import time

# создаем объект-сервер
app = Flask(__name__)

# создаем объект-камеру
camera = cv2.VideoCapture(0)  # веб камера

# это всякие переменные, значения которых я передавал в браузер, можно бахнуть
user = {'username': 'Miguel'}
test_var = "Anton"

# декораторы, связывают с функцией ниже
# Когда веб-браузер запрашивает один из этих двух URL-адресов, 
# Flask будет вызывать эту функцию и передавать возвращаемое 
# значение обратно в браузер в качестве ответа.
@app.route("/")
@app.route("/index")
def index():
    #возвращаем шаблон и (опционально) какую-то инфу
    return render_template('video_joy.html')

# роут для теста джойстиков
@app.route("/joy")
def joy():
    return render_template('joy.html')

def hello():
    return "Hello, World!"

@app.route("/test")
def test():
    return render_template('index.html', title='Home', user=user, test_v = test_var)

# роут видеофид, который дергает страничка
@app.route('/video_feed')
def video_feed():
    #с помощью команды респонс отдает кадры, которые получает с помощью генератора ген_фреймс
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# генератор, который получает кадр из камеры, что-то с ним делает,
# превращает в джипег-картинку и отдает
def gen_frames():  
    while True: #camera.isOpened(): #или True
        time.sleep(0.01)    # ограничение fps (если видео тупит, можно убрать)
        success, frame = camera.read()  # Получаем фрейм с камеры
        if not success: # если не удалось получить картинку - выход из цикла
            break
        else:

            # иначе работаем с картинкой, что-то там распознаем

            #frame = cv2.resize(frame, (320, 240), interpolation=cv2.INTER_AREA)  # уменьшаем разрешение кадров (если видео тупит, можно уменьшить еще больше)
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # перевод изображения в градации серого
            #_, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)  # бинаризуем изображение

            # затем превращаем ее в картинку джипег
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # и отдаем ее 
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

# роут контрол - его каждые нцать секунд дергает джаваскрипт из браузера
# и пересылает какие-то данные
@app.route('/control')
def control():

    # Пришел запрос на управления роботом
    # выводим значения на экран
    print (request.args.get('x'), ' ', request.args.get('y'))  

    # возвращаем 200 скрипту на страничке, дескать, все ОК, получили
    return '', 200, {'Content-Type': 'text/plain'}  
                   

# flask run