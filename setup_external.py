import os
import subprocess
import sys

def run_cmd(cmd, cwd=None):
    try:
        print(f"执行命令: {cmd}")
        subprocess.check_call(cmd, shell=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ 命令执行失败: {e}")
        return False
    return True

def setup_external_tools():
    project_root = os.path.dirname(os.path.abspath(__file__))
    external_dir = os.path.join(project_root, 'external')
    
    if not os.path.exists(external_dir):
        os.makedirs(external_dir)
        print(f"📂 创建 external 目录: {external_dir}")

    # 定义需要克隆的仓库列表 (目录名, Git地址)
    repos = [
        ("dust3r", "https://github.com/naver/dust3r.git"),
        ("sam2", "https://github.com/facebookresearch/sam2.git"),
        ("gca", "https://github.com/gca-spatial-reasoning/gca.git")
    ]

    for name, url in repos:
        repo_path = os.path.join(external_dir, name)
        if not os.path.exists(repo_path):
            print(f"🚀 正在克隆 {name} ({url})...")
            if run_cmd(f"git clone {url} {repo_path}"):
                print(f"✅ {name} 克隆成功")
                
                # 特殊处理: SAM 2 需要安装
                if name == "sam2":
                    print("⚙️ 安装 SAM 2 依赖...")
                    # 注意：这里使用 --target 安装到 site-packages 以便持久化
                    site_packages = os.path.join(project_root, 'site-packages')
                    # SAM 2 的安装可能需要 cuda 编译，如果出错可以去掉 -e
                    run_cmd(f"{sys.executable} -m pip install --target {site_packages} -e .", cwd=repo_path)
            else:
                print(f"❌ {name} 克隆失败")
        else:
            print(f"✅ {name} 已存在，跳过克隆")

    print("\n🎉 外部模型库设置完成！")
    print("请手动下载模型权重并在 Notebook 中进行测试。")

if __name__ == "__main__":
    setup_external_tools()
