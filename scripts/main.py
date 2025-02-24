import threading
import cv2
import queue
from src.reid_tracker import ReidTracker
from src.utils import draw_reid_tracking_results
import yaml
from src.bird_eye_view import BirdEyeView

reset_queue = queue.Queue()


# 加载配置文件
def load_config(config_path:str):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def wait_for_input():
    while True:
        user_input = input("Please enter the person needs to be reset:")
        reset_queue.put(user_input)

config = load_config("/Volumes/Disk_1/ApplicationData/PythonProject/ReID-Tracker/configs/config.yaml")

if __name__ == '__main__':
    reid_tracker = ReidTracker(config['yolo']['model_path'],config['deepsort']['deepsort_cfg_path'],
        '/Volumes/Disk_1/ApplicationData/PythonProject/ReID-Tracker/data/input/Athlete/',config, reset_queue, 'cpu')
    video_capture = cv2.VideoCapture(
        '/Volumes/Disk_1/ApplicationData/PythonProject/ReID-Tracker/data/input/short_version/Camera3.mp4')
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    output_video_path = '/Volumes/Disk_1/ApplicationData/PythonProject/ReID-Tracker/data/output/tracked_video.mp4'
    bird_view = BirdEyeView()
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_video_path, fourcc, 30, (frame_width, frame_height))
    input_thread = threading.Thread(target=wait_for_input, daemon=True)
    input_thread.start()
    ret = True
    while True:
        frames = []
        for i in range(10):
            ret, frame = video_capture.read()
            if not ret:
                break
            frames.append(frame)
        if not ret:
            break
        tracking_resultses = reid_tracker.multi_frame_update(frames)
        if bird_view.matrix is None:
            bird_view.matrix = reid_tracker.matrix
        for idx,(tracking_results,frame) in enumerate(zip(tracking_resultses,frames)):
            draw_reid_tracking_results(tracking_results, frame)
            field = bird_view.draw_bird_view(tracking_results)
            # 缩小 field 图像
            scale_factor = 0.55  # 缩放比例
            field_resized = cv2.resize(field, (0, 0), fx=scale_factor, fy=scale_factor)

            # 获取 frame 和 field_resized 的尺寸
            fh, fw, _ = frame.shape  # frame 高度和宽度
            th, tw, _ = field_resized.shape  # 缩小后 field 的高度和宽度

            # 计算左下角的粘贴位置
            x_offset = 10  # 左侧边距
            y_offset = fh - th - 10  # 底部边距

            # 获取 frame 上对应区域
            roi = frame[y_offset:y_offset + th, x_offset:x_offset + tw]  # 感兴趣区域 (Region of Interest)

            # 透明度设置（alpha 越小，field_resized 越透明）
            alpha = 0.8  # 透明度，可调节（0.0 完全透明，1.0 完全不透明）

            # 进行透明融合
            blended = cv2.addWeighted(field_resized, alpha, roi, 1 - alpha, 0)

            # 把融合后的图像放回 frame
            frame[y_offset:y_offset + th, x_offset:x_offset + tw] = blended

            cv2.imshow("Monitor", frame)
            video_writer.write(frame)
            cv2.waitKey(1)

    video_capture.release()
    video_writer.release()
    cv2.destroyAllWindows()
    print(f"Processing complete, video has been saved as: {output_video_path}")