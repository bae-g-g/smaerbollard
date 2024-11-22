from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import cv2

app = FastAPI()

# 카메라 및 설정 초기화
def get_camera():
    cap = cv2.VideoCapture(0)  # 0은 기본 웹캠
    cap.set(cv2.CAP_PROP_FPS, 30)  # 30 FPS 설정
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # 버퍼 최소화
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 가로 해상도 설정
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # 세로 해상도 설정
    return cap

# 프레임 생성기
def generate_frames():
    cap = get_camera()
    while True:
        success, frame = cap.read()
        if not success:
            break

        # 해상도 줄이기 (필요시 사용)
        # frame = cv2.resize(frame, (640, 480)) 

        # 프레임을 H.264 압축 (MJPEG보다 효율적)
        _, buffer = cv2.imencode('.jpg', frame)

        # 클라이언트로 전송
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n\r\n')

    cap.release()

# 스트리밍 엔드포인트
@app.get("/video")
async def video_stream():
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")

# FastAPI 서버 실행
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=554, log_level="info")
# uvicorn webcam:app --reload 터미널에 입력해서 실행
