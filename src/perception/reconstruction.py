import sys
import os

# 将项目根目录添加到 python 路径
# 确保可以 import init_env
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path:
    sys.path.append(project_root)

import init_env  # 自动处理依赖路径
import torch
import glob
import argparse
from dust3r.inference import inference
from dust3r.model import AsymmetricCroCo3DStereo
from dust3r.utils.image import load_images
from dust3r.image_pairs import make_pairs
from dust3r.cloud_opt import global_aligner, GlobalAlignerMode

def download_weights(model_dir="checkpoints"):
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
    pass
    # 暂时禁用自动下载，改为手动指导
    # weight_path = os.path.join(model_dir, "DUSt3R_ViTLarge_BaseDecoder_512_dpt.pth")
    # if not os.path.exists(weight_path):
    #     print(f"⏳ Downloading model weights to {weight_path}...")
    #     os.system(f"wget https://download.europe.naverlabs.com/ComputerVision/DUSt3R/DUSt3R_ViTLarge_BaseDecoder_512_dpt.pth -O {weight_path}")
    #     print("✅ Download complete.")
    # return weight_path
    
    # 强制在魔搭环境寻找已下载的权重
    # 魔搭环境中，通常建议用户手动下载或者使用 modelscope 的 hub
    # 这里我们假设用户已经手动下载好了
    
    weight_path = os.path.join(model_dir, "DUSt3R_ViTLarge_BaseDecoder_512_dpt.pth")
    if not os.path.exists(weight_path):
        # 尝试备用下载源 (HuggingFace 镜像)
        print("⚠️ 官方源太慢，正在尝试从 Hugging Face 镜像下载...")
        hf_url = "https://huggingface.co/naver/DUSt3R_ViTLarge_BaseDecoder_512_dpt/resolve/main/DUSt3R_ViTLarge_BaseDecoder_512_dpt.pth"
        # 使用 HF 镜像通常快得多
        cmd = f"wget {hf_url} -O {weight_path}"
        os.system(cmd)
        
        if not os.path.exists(weight_path) or os.path.getsize(weight_path) < 1000:
             raise FileNotFoundError(f"❌ 下载失败！请尝试手动下载该文件并上传到 {weight_path}")

    return weight_path

def run_reconstruction(input_dir, output_file, num_images=5, device='cuda'):
    # 1. 准备模型
    weight_path = download_weights()
    print(f"🚀 Loading model on {device}...")
    try:
        model = AsymmetricCroCo3DStereo.from_pretrained(weight_path).to(device)
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return

    # 2. 加载图片
    filelist = sorted(glob.glob(os.path.join(input_dir, "*.jpg"))) 
    print(f"📸 Found {len(filelist)} images in {input_dir}")
    
    if len(filelist) < 2:
        print("❌ Not enough images! Need at least 2.")
        return

    # 截取前 N 张用于测试
    test_files = filelist[:num_images]
    print(f"🔬 Processing first {len(test_files)} images...")

    images = load_images(test_files, size=512)
    pairs = make_pairs(images, scene_graph='complete', prefilter=None, symmetrize=True)

    # 3. 运行推理
    print("⚡ Running inference...")
    output = inference(pairs, model, device, batch_size=1)

    # 4. 全局对齐
    print("🔗 Global alignment...")
    scene = global_aligner(output, device=device, mode=GlobalAlignerMode.PointCloudOptimizer)
    loss = scene.compute_global_alignment(init='mst', niter=300, schedule='linear', lr=0.01)

    # 5. 保存结果
    # 确保存储目录存在
    out_dir = os.path.dirname(output_file)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)

    scene.min_conf_thr = float(3.0)
    scene.clean_pointcloud()
    scene.save_ply(output_file)
    print(f"🎉 Success! Point cloud saved to {output_file}")

    # 清理显存
    del model, scene, output
    torch.cuda.empty_cache()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dust3R Reconstruction Script")
    parser.add_argument("--input_dir", type=str, default="data/test_frames", help="Directory containing input images")
    parser.add_argument("--output_file", type=str, default="output/room.ply", help="Path to save the output .ply file")
    parser.add_argument("--num_images", type=int, default=5, help="Number of images to process (careful with VRAM!)")
    
    args = parser.parse_args()
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    run_reconstruction(args.input_dir, args.output_file, args.num_images, device)
