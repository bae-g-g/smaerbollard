import cv2
from flask import Flask, Response

app = Flask(__name__)

# 웹캠 비디오 캡처
def generate_frames():
    cap = cv2.VideoCapture(0)  # 0은 기본 웹캠을 의미
    while True:
        success, frame = cap.read()  # 웹캠에서 프레임을 읽음
        if not success:
            break
        else:
            # MJPEG 스트림을 위한 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # 프레임을 클라이언트에 전달
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# 비디오 스트리밍을 위한 라우트
@app.route('/video')
def video():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 서버 실행
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5958)  # 포트 5958에서 서버 실행
#집 와이파이 http://192.168.123.102:5958/video