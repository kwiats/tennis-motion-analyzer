class PoseEstimatorInterface:
    def stream(self):
        raise NotImplementedError

    def process_frame(self, frame):
        raise NotImplementedError

    def draw_pose(self, image, result):
        raise NotImplementedError

    def process_video(self, input_path, output_path):
        pass
