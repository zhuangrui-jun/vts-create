# Live2D Viewer（AI 角色对话）
基于 **Vue 3 + Vite + Pixi.js / Live2D** 的前端，与 **FastAPI + LangGraph + SQLite** 的后端组成的本地对话应用。
## 功能概览
- Live2D 模型展示与对话界面
- 会话列表、流式消息、角色人设（可通过环境变量覆盖）
- 可选联网搜索等能力（依赖对应 API 配置）
## 环境要求
| 组件 | 要求 |
|------|------|
| Node.js | 建议 **18+** |
| Python | 建议 **3.10+** |
| 包管理 | `npm` / `pnpm` / `yarn`（文档以 npm 为例） |

## 配置（`.env`）
OPENAI_API_KEY需要小米的模型
或者自己调整供应商的api模型

## 本地启动
需要**两个终端**：一个跑前端，一个跑后端。
### 1. 前端
```bash
npm install
npm run dev
浏览器访问：http://localhost:5173

2. 后端
cd backend
python -m venv .venv
Windows PowerShell 激活虚拟环境：

.\.venv\Scripts\Activate.ps1
安装依赖并启动：


pip install -r requirements.txt
uvicorn app.main:app --reload --host localhost --port 8000


特别鸣谢bilibili @雪熊企划的live2d 模型
