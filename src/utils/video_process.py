import cv2
import os
import numpy as np

def calculate_blur_score(image):
    """
    使用拉普拉斯算子计算图片的模糊程度
    分数越低越模糊
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var()

def extract_frames(video_path, output_dir, interval=10, min_blur_score=100.0):
    """
    从视频中抽取清晰的关键帧
    :param video_path: 视频文件路径
    :param output_dir: 输出图片文件夹
    :param interval: 基础抽帧间隔（每多少帧尝试抽取）
    :param min_blur_score: 模糊阈值，低于此分数的图片会被丢弃
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"📂 创建输出目录: {output_dir}")
        
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"❌ 无法打开视频文件: {video_path}")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"🎬 开始处理视频，共 {total_frames} 帧...")
    
    frame_idx = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # 1. 间隔筛选
        if frame_idx % interval == 0:
            # 2. 模糊检测
            score = calculate_blur_score(frame)
            if score > min_blur_score:
                # 命名为 00001.jpg, 00002.jpg ...
                filename = os.path.join(output_dir, f"{saved_count:05d}.jpg")
                cv2.imwrite(filename, frame)
                saved_count += 1
                if saved_count % 10 == 0:
                    print(f"  -> 已提取 {saved_count} 帧 (当前帧模糊分: {score:.1f})")
            else:
                # 如果太模糊，虽然没存，但打印一下日志方便调试（可选）
                pass
            
        frame_idx += 1
        
    cap.release()
    print(f"✅ 提取完成：共保存 {saved_count} 张清晰关键帧到 {output_dir}")

# 使用示例
if __name__ == "__main__":
    # 请手动修改这里的路径进行测试
    # extract_frames("my_room_video.mp4", "data/test_frames", interval=15, min_blur_score=60.0)
    pass
