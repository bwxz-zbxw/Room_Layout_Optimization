import subprocess
import sys
import os

def install():
    """
    将 requirements.txt 中的依赖安装到项目目录下的 site-packages 文件夹
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(project_root, 'site-packages')
    req_file = os.path.join(project_root, 'requirements.txt')
    
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        print(f"📂 创建本地依赖目录: {target_dir}")
        
    print(f"🚀 开始安装依赖到持久化目录: {target_dir} ...")
    print(f"📦 读取依赖文件: {req_file}")

    # 构造 pip 命令
    # --target 指定安装目录
    # --upgrade 确保更新
    # --no-user 避免安装到用户目录
    cmd = [
        sys.executable, '-m', 'pip', 'install', 
        '--target', target_dir, 
        '-r', req_file,
    ]
    
    try:
        # 实时输出日志
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace' # 防止编码错误
        )
        
        for line in process.stdout:
            print(line, end='')
            
        process.wait()
        
        if process.returncode == 0:
            print("\n✅ 所有依赖安装完成！")
            print(f"💡 提示：在 Notebook 中请先运行 `import init_env` 即可使用这些库。")
        else:
            print(f"\n❌ 安装过程出现错误，退出码: {process.returncode}")
            
    except Exception as e:
        print(f"\n❌ 执行安装脚本失败: {e}")

if __name__ == "__main__":
    install()
