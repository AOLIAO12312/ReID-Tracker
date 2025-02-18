
---

# 高效人物跟踪与识别

## 项目概述
本项目结合了 **DeepSORT** 和 **TorchReID** 实现了高效的多人物跟踪与身份识别系统，特别适用于复杂环境中，如遮挡严重或跟踪丢失后的快速恢复身份。通过整合 **YOLOv11** 进行目标检测和 **DeepSORT** 进行多帧目标跟踪，本系统可以实时追踪运动场上的运动员，并在DeepSORT跟踪失败后，使用TorchReID进行重新识别，保证身份一致性。

## 核心功能
- **YOLOv11**：进行实时目标检测，快速识别和定位运动员。
- **DeepSORT**：高效的目标跟踪，确保每个运动员的连续跟踪，并提供唯一身份ID。
- **TorchReID**：在DeepSORT丢失目标时，利用ReID进行快速身份恢复，确保跟踪过程中的身份一致性。
- **多帧融合跟踪**：增强跟踪的鲁棒性，在复杂环境中保持高准确度，即使在遮挡或目标快速变换位置时也能有效跟踪。

## 适用场景
- **运动场景**：运动员的实时识别和跟踪，支持快速身份恢复和一致性维护。
- **复杂环境**：适用于遮挡严重、光线变化等复杂场景下的多目标跟踪和识别。
- **高密度人群**：在人员密集、快速移动的环境下保持高效准确的目标跟踪。

## 安装与使用

### 环境要求
- Python 3.x
- 依赖库：
  - `YOLO`（用于目标检测）
  - `DeepSORT`（用于目标跟踪）
  - `TorchReID`（用于身份识别）

### 安装依赖
```bash
pip install -r requirements.txt
```

---
