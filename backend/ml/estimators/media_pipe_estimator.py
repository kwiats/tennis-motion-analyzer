import base64
import time

import cv2
import mediapipe as mp

from ml.estimators.pose_estimator_interface import PoseEstimatorInterface


class MediaPipePoseEstimator(PoseEstimatorInterface):
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )

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
        fourcc = cv2.VideoWriter_fourcc(*"avc1")
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
        results = self.pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(
                image, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS
            )

        return image

    def draw_pose(self, image, result):
        # This method is not needed for MediaPipe
        pass
