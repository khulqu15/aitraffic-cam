import cv2
cap = cv2.VideoCapture(0)
out = cv2.VideoWriter('/dev/video10', cv2.VideoWriter_fourcc(*'MJPG'), 30.0, (640, 480))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    out.write(frame)
