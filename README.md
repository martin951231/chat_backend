# AI Character Platform Backend

一个基于 FastAPI 的 AI 角色互动平台后端骨架，当前版本提供：

- FastAPI + Pydantic v2 + SQLAlchemy 2.0
- 分层结构：`api / service / repository / model / schema / provider / core`
- 默认 `mock provider`，为后续接入 OpenAI / DeepSeek / Qwen 预留扩展位
- 默认支持 SQLite 本地开发，也支持切换到 MySQL
- 统一响应结构与统一异常处理

## 目录结构

```text
chat_backend/
├─ app/
│  ├─ api/
│  │  ├─ router.py
│  │  └─ v1/
│  │     ├─ health.py
│  │     ├─ character.py
│  │     ├─ session.py
│  │     └─ chat.py
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ database.py
│  │  ├─ exceptions.py
│  │  ├─ response.py
│  │  └─ logger.py
│  ├─ models/
│  │  ├─ base.py
│  │  ├─ character.py
│  │  ├─ chat_session.py
│  │  └─ message.py
│  ├─ providers/
│  │  ├─ base.py
│  │  ├─ mock_provider.py
│  │  └─ provider_factory.py
│  ├─ repositories/
│  │  ├─ character_repository.py
│  │  ├─ session_repository.py
│  │  └─ message_repository.py
│  ├─ schemas/
│  │  ├─ character.py
│  │  ├─ session.py
│  │  └─ chat.py
│  ├─ services/
│  │  ├─ character_service.py
│  │  ├─ session_service.py
│  │  ├─ chat_service.py
│  │  └─ llm_service.py
│  └─ main.py
├─ scripts/
│  ├─ init_db.py
│  └─ mysql_schema.sql
├─ .env.example
├─ requirements.txt
├─ run.py
└─ README.md
```

## 启动步骤

建议使用 Python 3.12 或 3.13；如果使用 Python 3.14，请确保依赖已升级到当前 `requirements.txt` 中的版本。
其中 SQLAlchemy 需要至少 `2.0.41+`，否则在 Python 3.14 下可能因为 ORM 注解扫描兼容问题导致应用启动时报错。

### 1. 创建虚拟环境并安装依赖

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，按需修改：

```bash
copy .env.example .env
```

默认使用 SQLite：

```env
DATABASE_URL=sqlite:///./data/ai_character.db
```

如果你要切到 MySQL，把 `.env` 改成类似：

```env
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/ai_character_platform?charset=utf8mb4
```

### 3. 初始化数据表

#### 方案 A：本地 SQLite / 当前 `DATABASE_URL`

```bash
python scripts/init_db.py
```

#### 方案 B：MySQL 手动建表

先创建数据库，然后执行：

```sql
SOURCE scripts/mysql_schema.sql;
```

或直接把 `scripts/mysql_schema.sql` 内容复制到你的 MySQL 客户端执行。

注意：应用启动时不会自动建表，建表动作只在脚本里。

### 4. 启动服务

```bash
python run.py
```

启动后访问：

- Swagger: `http://127.0.0.1:8000/docs`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## 已提供接口

- `GET /api/v1/health`
- `GET /api/v1/characters`
- `POST /api/v1/characters`
- `GET /api/v1/sessions/{character_id}`
- `POST /api/v1/sessions`
- `POST /api/v1/chat`

## Chat 接口说明

`POST /api/v1/chat` 的业务链路：

1. 根据 `character_id` 查询角色
2. 如果传入 `session_id`，则读取对应会话
3. 如果没有传入 `session_id`，则自动创建新会话
4. 保存用户消息
5. 调用 `mock provider`
6. 保存 assistant 消息
7. 返回统一结构响应

## 后续扩展建议

- 在 `app/providers/` 下增加 `OpenAIProvider`、`DeepSeekProvider`、`QwenProvider`
- 在 `app/services/llm_service.py` 中增加 provider 选择逻辑
- 在 `messages` 表里扩展更多模型侧字段，例如 token 使用量、finish_reason、原始响应 JSON
