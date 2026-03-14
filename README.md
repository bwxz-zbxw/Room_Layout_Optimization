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

## 3. 开发计划 (Roadmap)
- [ ] **Phase 1: 基础设施**
  - [ ] 配置 ModelScope 环境
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
