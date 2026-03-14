import sys
import os

"""
环境初始化脚本
在 ModelScope 的 Notebook 中，只要 `import init_env`，
就会自动把项目目录下的 `site-packages` 添加到 sys.path 的最前面。
这样可以确保优先加载安装在持久化目录中的库。
"""

# 获取项目根目录 (假设此脚本在根目录下)
project_root = os.path.dirname(os.path.abspath(__file__))

# 定义本地依赖库路径
local_libs = os.path.join(project_root, 'site-packages')

# 将 src 目录也加入路径，方便导入内部模块
src_dir = os.path.join(project_root, 'src')

# 1. 加载本地依赖库 (site-packages)
if os.path.exists(local_libs):
    if local_libs not in sys.path:
        sys.path.insert(0, local_libs)
        print(f"✅ [init_env] 已加载本地依赖库: {local_libs}")
else:
    print(f"⚠️ [init_env] 未找到本地依赖库: {local_libs}。请运行 python install_deps.py 安装。")

# 2. 加载源码目录 (src)
if os.path.exists(src_dir):
    if src_dir not in sys.path:
        sys.path.append(src_dir)
        print(f"✅ [init_env] 已加载源码目录: {src_dir}")
