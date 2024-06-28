import base64
import time

import cv2
from ultralytics import YOLO

import config
from ml.estimators.pose_estimator_interface import PoseEstimatorInterface


class YOLOPoseEstimator(PoseEstimatorInterface):
    def __init__(self):
        self.yolo_model = YOLO(config.YOLO_MODEL)

    def stream(self, capture, send):
        while capture.isOpened():
            ret, frame = capture.read()
            if ret:
                processed_frame = self.process_frame(frame)
                _, buffer = cv2.imencode(".jpg", processed_frame)
                frame_base64 = base64.b64encode(buffer).decode("utf-8")
                send(text_data=frame_base64)
            time.sleep(0.1)

    def process_video(self, input_path, output_path):
        cap = cv2.VideoCapture(input_path)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(
            output_path,
            fourcc,
            cap.get(cv2.CAP_PROP_FPS),
            (int(cap.get(3)), int(cap.get(4))),
        )

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)
            out.write(processed_frame)

        cap.release()
        out.release()

    def process_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.yolo_model(image, device="mps", verbose=False)

        for result in results:
            self.draw_pose(image, result)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return image

    def draw_pose(self, image, result):
        keypoints = result.keypoints.xy.cpu().numpy().astype(int)

        for keypoint in keypoints:
            for x, y in keypoint:
                cv2.circle(image, (x, y), 10, (0, 255, 0), -1)
