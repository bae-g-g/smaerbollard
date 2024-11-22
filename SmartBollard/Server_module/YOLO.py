import cv2
from ultralytics import YOLO

# YOLO 모델 로드 (사전 학습된 모델 사용)
model = YOLO('yolov8n.pt')  # Nano 모델, 필요에 따라 변경 가능

# 실시간 스트리밍 URL
stream_url = "http://127.0.0.1:8000/video"

# 비디오 캡처 객체 생성
cap = cv2.VideoCapture(stream_url)

if not cap.isOpened():
    print("스트리밍 URL에 연결할 수 없습니다.")
    exit()

# 영상 처리 루프
while True:
    ret, frame = cap.read()
    if not ret:
        print("프레임을 읽을 수 없습니다. 스트리밍이 중단되었을 수 있습니다.")
        break

    # YOLO로 객체 감지
    results = model(frame)

    # 결과를 OpenCV에서 그려줌
    annotated_frame = results[0].plot()

    # 결과 영상 출력
    cv2.imshow("YOLO Real-Time Detection", annotated_frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()
