# 我帮你下载 - 架构文档

## 系统架构图

```
┌─────────────────────────────────────────────────────────────┐
│                         前端层                               │
├─────────────────────────────────────────────────────────────┤
│  Web UI          │  微信小程序    │  Electron   │  浏览器插件 │
│  (Vue/React)     │  (WeChat)     │  (Desktop)  │  (Extension)│
└────────┬─────────┴───────┬───────┴──────┬──────┴──────┬──────┘
         │                 │              │             │
         └─────────────────┴──────────────┴─────────────┘
                              │
                         REST API
                              │
┌─────────────────────────────┴───────────────────────────────┐
│                        API 网关层                            │
├─────────────────────────────────────────────────────────────┤
│  路由 │ 认证 │ 限流 │ 日志 │ 监控 │ 缓存                     │
└────────┬────────────────────────────────────────────────────┘
         │
┌────────┴────────────────────────────────────────────────────┐
│                       业务逻辑层                             │
├─────────────────────────────────────────────────────────────┤
│  SearchService  │  SpeedTestService  │  CacheService        │
│  (搜索服务)      │  (测速服务)         │  (缓存服务)          │
└────────┬────────┴──────────┬─────────┴──────────┬───────────┘
         │                   │                    │
┌────────┴───────────────────┴────────────────────┴───────────┐
│                       数据访问层                             │
├─────────────────────────────────────────────────────────────┤
│  Cache Manager  │  Database  │  External APIs               │
│  (本地/Redis)    │  (SQLite)  │  (镜像站API)                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
download-helper/
├── backend/                    # 后端代码
│   ├── app.py                 # Flask 主应用
│   ├── config/                # 配置模块
│   │   └── settings.py        # 配置管理
│   ├── services/              # 业务服务
│   │   ├── search.py          # 搜索服务
│   │   └── speed_test.py      # 测速服务
│   ├── cache/                 # 缓存模块
│   │   └── manager.py         # 缓存管理
│   └── utils/                 # 工具函数
│       └── logger.py          # 日志工具
│
├── frontend/                   # 前端代码
│   ├── templates/             # HTML 模板
│   │   └── index.html
│   └── static/                # 静态资源
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── app.js
│
├── tests/                      # 测试代码
│   ├── test_search.py
│   ├── test_speed.py
│   └── test_cache.py
│
├── logs/                       # 日志文件
│   └── 20260524.log
│
├── data/                       # 数据目录
│   └── cache/                 # 缓存文件
│
├── .env                        # 环境变量
├── requirements.txt            # Python 依赖
├── README.md                   # 项目说明
├── ROADMAP.md                  # 路线图
└── ARCHITECTURE.md             # 本文档
```

---

## 核心模块说明

### 1. SearchService (搜索服务)

**职责：**
- 提取文件名
- 搜索镜像站
- 生成替代下载源

**核心方法：**
```python
extract_filename(url)           # 提取文件名
search_alternatives(url)        # 搜索替代源
```

**镜像站白名单：**
- GitHub: ghproxy, mirror.ghproxy, gh.api.99988866.xyz
- Node.js: npmmirror, tuna, ustc
- PyTorch: tuna, aliyun
- PyPI: tuna, aliyun
- 通用: tuna, aliyun, ustc, tencent

---

### 2. SpeedTestService (测速服务)

**职责：**
- HEAD 测速（快速）
- Range 测速（精确）
- 批量并发测速

**核心方法：**
```python
test_head(url)                  # HEAD 请求测速
test_range(url, chunk_size)     # Range 分片测速
test_batch(urls, method)        # 批量测速
```

**测速策略：**
- HEAD: 仅请求头，速度快，精度低
- Range: 下载 1MB 数据，速度慢，精度高
- 并发: 10 线程并发，5 秒超时

---

### 3. CacheManager (缓存管理)

**职责：**
- 结果缓存
- TTL 管理
- 缓存清理

**核心方法：**
```python
get(url)                        # 获取缓存
set(url, results)               # 设置缓存
clear()                         # 清空缓存
```

**缓存策略：**
- 存储: 本地 JSON 文件（后续迁移 Redis）
- TTL: 1 小时
- Key: MD5(url)

---

### 4. Logger (日志系统)

**职责：**
- 请求日志
- 错误日志
- 性能日志

**日志级别：**
- DEBUG: 调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息

**日志格式：**
```
2026-05-24 16:30:45 [api] INFO: Search request: https://example.com
2026-05-24 16:30:46 [speed_test] INFO: HEAD test: https://example.com - 0.45s - 200
2026-05-24 16:30:47 [cache] INFO: Cache saved: https://example.com
```

---

## API 接口设计

### 1. 搜索接口

**请求：**
```http
POST /api/search
Content-Type: application/json

{
  "url": "https://nodejs.org/dist/v20.0.0/node-v20.0.0-win-x64.zip",
  "method": "head"  // 可选: head | range
}
```

**响应：**
```json
{
  "filename": "node-v20.0.0-win-x64.zip",
  "results": [
    {
      "url": "https://npmmirror.com/mirrors/node/v20.0.0/node-v20.0.0-win-x64.zip",
      "method": "HEAD",
      "speed": "0.45s",
      "speed_ms": 450,
      "size": "28.5 MB",
      "status": 200,
      "available": true,
      "source": "npmmirror.com"
    }
  ],
  "fastest": { /* 最快源 */ },
  "total": 6,
  "available": 3,
  "elapsed": "2.34s"
}
```

### 2. 清除缓存

**请求：**
```http
POST /api/cache/clear
```

**响应：**
```json
{
  "message": "Cache cleared"
}
```

### 3. 健康检查

**请求：**
```http
GET /api/health
```

**响应：**
```json
{
  "status": "ok",
  "cache_enabled": true,
  "workers": 10
}
```

---

## 配置说明

### 环境变量 (.env)

```bash
# Flask 配置
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=5000

# 缓存配置
CACHE_ENABLED=True
CACHE_TTL=3600
CACHE_DIR=./data/cache

# 日志配置
LOG_LEVEL=INFO
LOG_DIR=./logs

# 测速配置
SPEED_TEST_TIMEOUT=5
SPEED_TEST_WORKERS=10
SEARCH_MAX_RESULTS=15

# API 配置
ENABLE_API_KEY=False
API_RATE_LIMIT=100
```

---

## 部署方案

### 开发环境

```bash
cd ~/Desktop/download-helper
pip install -r requirements.txt
python backend/app.py
```

### 生产环境

**方案 1: Docker**
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "backend.app:app"]
```

**方案 2: Systemd**
```ini
[Unit]
Description=Download Helper Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/var/www/download-helper
ExecStart=/usr/bin/python3 backend/app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**方案 3: Vercel (Serverless)**
```json
{
  "builds": [
    { "src": "backend/app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/(.*)", "dest": "backend/app.py" }
  ]
}
```

---

## 性能优化

### 1. 缓存策略
- 本地缓存 → Redis 缓存
- CDN 加速静态资源
- 结果预加载

### 2. 并发优化
- 异步任务队列 (Celery)
- 连接池复用
- 批量请求合并

### 3. 数据库优化
- 索引优化
- 查询缓存
- 读写分离

---

## 安全考虑

### 1. 输入验证
- URL 格式校验
- 参数类型检查
- SQL 注入防护

### 2. 速率限制
- IP 限流
- API Key 限流
- 防 DDoS

### 3. 数据安全
- HTTPS 强制
- 敏感信息加密
- 日志脱敏

---

## 监控告警

### 1. 性能监控
- 响应时间
- 成功率
- 并发数

### 2. 错误监控
- 异常捕获
- 错误日志
- 告警通知

### 3. 业务监控
- 搜索量
- 缓存命中率
- 镜像站可用性

---

## 扩展性设计

### 1. 水平扩展
- 无状态设计
- 负载均衡
- 分布式缓存

### 2. 垂直扩展
- 多核并发
- 内存优化
- 数据库优化

### 3. 功能扩展
- 插件系统
- Webhook 支持
- 自定义镜像站
