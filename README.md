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


