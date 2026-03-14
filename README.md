# 毕设项目：基于视频感知的室内布局优化系统 (GCA架构)

## 0. 项目简介
本项目通过用户拍摄的室内视频，利用 Dust3R 进行三维重建，结合 SAM 2 进行语义分割，构建无幻觉的 3D 语义地图。通过 LLM 解析用户自然语言指令，并在几何层进行物理约束计算，最终生成可解释的布局优化建议。

## 1. 核心流程
1. **输入**：室内视频 (.mp4) + 用户提问 (Text)
2. **感知层**：
   - 视频抽帧 (Keyframe Extraction)
   - Dust3R 多视图重建 -> 全局点云 P_all
   - SAM 2 视频对象跟踪 -> 物体掩码 Mask_obj
   - 2D-3D 投影与清洗 -> 独立物体点云 Cloud_obj
3. **几何层**：
   - Open3D 计算包围盒 (AABB/OBB)
   - 物理属性提取 (尺寸、位置、朝向)
   - 空间关系计算 (距离、重叠、通道宽度)
4. **推理层**：
   - LLM 解析用户意图 -> 生成约束 JSON
   - 几何引擎校验约束 -> 生成 Fact JSON
   - LLM 基于 Fact 生成建议 -> 自然语言回复

## 2. 文件夹结构说明
- `src/perception/`: 视觉感知模块 (Dust3R, SAM 2)
  - `video_process.py`: 视频抽帧与预处理
  - `reconstruction.py`: 调用 Dust3R 生成点云
  - `segmentation.py`: 调用 SAM 2 获取语义掩码
  - `fusion.py`: 2D-3D 融合生成语义点云
- `src/geometry/`: 几何计算模块 (Open3D)
  - `analyzer.py`: 空间关系计算 (碰撞、距离)
  - `rules.py`: 硬规则定义
- `src/reasoning/`: 推理模块 (LLM)
  - `parser.py`: 自然语言转约束 JSON
  - `advisor.py`: 约束结果转优化建议
- `src/utils/`: 工具类
  - `visualizer.py`: 结果可视化
- `site-packages/`: **(自动生成)** 本地依赖库目录，用于魔搭持久化
- `init_env.py`: **(关键)** 环境初始化脚本，在 Notebook 开头导入
- `install_deps.py`: **(关键)** 依赖安装脚本，用于安装到 site-packages

## 3. 魔搭(ModelScope)环境配置指南

由于魔搭的系统环境重启后会重置，我们需要将依赖安装到项目目录下的 `site-packages` 文件夹中。

### 步骤 1：安装依赖 (首次运行或依赖变更时)
在魔搭终端中运行：
```bash
python install_deps.py
```
这不仅会安装 `requirements.txt` 中的依赖，还会自动处理系统路径。

### 步骤 2：在 Notebook 中使用
在你的 `.ipynb` 文件的**第一个代码块**中，务必加入以下代码：
```python
import init_env  # 自动加载 site-packages 到 sys.path
import sys
print(sys.path)  # 验证 site-packages 是否在最前
```

## 4. 开发计划 (Roadmap)
- [ ] **Phase 1: 基础设施**
  - [x] 配置 ModelScope 环境依赖持久化
  - [ ] 跑通 Dust3R 和 SAM 2 的 Demo
- [ ] **Phase 2: 感知层 (最难点)**
  - [ ] 实现视频抽帧策略 (每隔N帧或基于运动模糊筛选)
  - [ ] Dust3R `GlobalAlignment` 模式跑通
  - [ ] SAM 2 视频跟踪跑通
  - [ ] **关键**: 坐标系对齐与点云清洗
- [ ] **Phase 3: 几何与推理**
  - [ ] 定义 JSON 交互协议
  - [ ] 实现基础几何算子 (Distance, Volume)
  - [ ] 接入 Qwen-2.5-7B
