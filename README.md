# 启动
## 环境要求：
- Python 3.10 或更高版本
- Node.js 16.0 或更高版本
- npm 8.0 或更高版本
## 获取 API 密钥：
你需要准备以下 API 密钥：
- LLM 的 API(OpenAI、DeepSeek 等)
- 高德地图 Web 服务 Key：访问 https://console.amap.com/ 注册并创建应用
- Unsplash Access Key：访问 https://unsplash.com/developers 注册并创建应用

将所有 API 密钥放入.env文件。 

启动后端：
```text
# 1. 进入后端目录
cd trip-planner/backend

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑.env文件，填入你的API密钥

# 4. 启动后端服务
uvicorn app.api.main:app --reload
# 或者
python run.py
```
成功启动后，访问 http://localhost:8000/docs 可以看到 API 文档

启动前端：

```text
# 1. 进入前端目录
cd trip-planner/frontend

# 2. 安装依赖
npm install

# 3. 启动前端服务
npm run dev
```
成功启动后，访问 http://localhost:5173 即可使用应用。

# 说明
项目参照开源项目[hello-agents](https://github.com/RainbowYv/hello-agents)第13实战项目进行改进
原开源代码使用hello-agents自构建框架实现，本人参照其源码使用langchain框架在其基础上进行修改。

# 项目结构

```text
trip-planner/
├── backend/                    # 后端代码
│   ├── agents/            # 智能体实现
│   ├── api/               # API路由
│   ├── models/            # 数据模型
│   ├── services/          # 服务层
│   ├── config.py          # 配置文件
│   └── requirements.txt       # Python依赖
│
└── frontend/                   # 前端代码
    ├── src/
    │   ├── views/             # 页面组件
    │   ├── services/          # API服务
    │   ├── types/             # 类型定义
    │   └── router/            # 路由配置
    └── package.json           # npm依赖
```


