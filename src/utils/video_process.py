import cv2
import os

def extract_frames(video_path, output_dir, interval=10):
    """
    从视频中抽取关键帧
    :param video_path: 视频文件路径
    :param output_dir: 输出图片文件夹
    :param interval: 抽帧间隔（每多少帧存一张）
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    saved_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % interval == 0:
            # 命名为 00001.jpg, 00002.jpg ...
            filename = os.path.join(output_dir, f"{saved_count:05d}.jpg")
            cv2.imwrite(filename, frame)
            saved_count += 1
            
        frame_count += 1
        
    cap.release()
    print(f"提取完成：共 {saved_count} 帧，保存在 {output_dir}")

# 使用示例
if __name__ == "__main__":
    # extract_frames("test_video.mp4", "data/frames", interval=30)
    pass
