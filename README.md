# DownloadHub

<div align="center">

<img src="https://raw.githubusercontent.com/yourusername/downloadhub/main/assets/logo.png" alt="DownloadHub Logo" width="120" height="120">

# ⚡ DownloadHub

**智能搜索全网最快下载源**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

告别慢速下载，一键找到最快镜像站

[在线演示](#) · [快速开始](#-快速开始) · [文档](ARCHITECTURE.md) · [贡献指南](CONTRIBUTING.md)

</div>

---

## 📖 目录

- [特性](#-特性)
- [支持的下载源](#-支持的下载源)
- [快速开始](#-快速开始)
- [使用方法](#-使用方法)
- [项目结构](#-项目结构)
- [技术栈](#️-技术栈)
- [性能指标](#-性能指标)
- [路线图](#️-路线图)
- [贡献](#-贡献)
- [许可证](#-许可证)

---

## ✨ 特性

- 🚀 **智能搜索** - 自动搜索全网镜像站（GitHub、NPM、PyPI、PyTorch等）
- ⚡ **并发测速** - 10线程并发，快速找到最快源
- 💾 **智���缓存** - 1小时缓存，避免重复测速
- 📊 **双重测速** - HEAD快速测速 + Range精确测速
- 🎨 **现代UI** - 响应式设计，支持移动端
- 📝 **完整日志** - 记录所有请求和错误
- 🔌 **API化** - RESTful API，易于集成
- 🐳 **Docker支持** - 一键部署

---

## 🎯 支持的下载源

<table>
<tr>
<td align="center"><b>类型</b></td>
<td align="center"><b>镜像站</b></td>
<td align="center"><b>状态</b></td>
</tr>
<tr>
<td>GitHub</td>
<td>ghproxy, mirror.ghproxy</td>
<td>✅</td>
</tr>
<tr>
<td>Node.js</td>
<td>npmmirror, 清华镜像</td>
<td>✅</td>
</tr>
<tr>
<td>PyTorch</td>
<td>清华镜像, 阿里镜像</td>
<td>✅</td>
</tr>
<tr>
<td>PyPI</td>
<td>清华镜像, 阿里镜像</td>
<td>✅</td>
</tr>
<tr>
<td>通用</td>
<td>清华/阿里/中科大/腾讯</td>
<td>✅</td>
</tr>
</table>

---

## 🚀 快速开始

### 方式一：一键启动（推荐）

**Windows:**
```bash
双击 start.bat
```

**Mac/Linux:**
```bash
chmod +x start.sh
./start.sh
```

### 方式二：手动启动

```bash
# 克隆仓库
git clone https://github.com/yourusername/downloadhub.git
cd downloadhub

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
```

访问 http://localhost:5000

### 方式三：Docker 部署

```bash
# 使用 docker-compose
docker-compose up -d

# 或使用 docker
docker build -t downloadhub .
docker run -p 5000:5000 downloadhub
```

---

## 📖 使用方法

### Web UI

1. 打开浏览器访问 http://localhost:5000
2. 粘贴下载链接
3. 选择测速方式（快速/精确）
4. 查看推荐的最快源

### API 调用

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://nodejs.org/dist/v20.0.0/node-v20.0.0-win-x64.zip",
    "method": "head"
  }'
```

**响应示例：**
```json
{
  "filename": "node-v20.0.0-win-x64.zip",
  "results": [...],
  "fastest": {...},
  "total": 6,
  "available": 3,
  "elapsed": "2.34s"
}
```

---

## 📁 项目结构

```
downloadhub/
├── backend/           # 后端代码
│   ├── services/      # 业务服务（搜索、测速）
│   ├── cache/         # 缓存管理
│   ├── config/        # 配置管理
│   └── utils/         # 工具函数
├── frontend/          # 前端代码
│   ├── templates/     # HTML 模板
│   └── static/        # 静态资源
├── tests/             # 测试代码
├── logs/              # 日志文件
├── data/              # 数据目录
├── run.py             # 启动入口
├── Dockerfile         # Docker 配置
└── docker-compose.yml # Docker Compose 配置
```

---

## 🛠️ 技术栈

<table>
<tr>
<td align="center"><b>后端</b></td>
<td align="center"><b>前端</b></td>
<td align="center"><b>部署</b></td>
</tr>
<tr>
<td>Python 3.12</td>
<td>HTML5 + CSS3</td>
<td>Docker</td>
</tr>
<tr>
<td>Flask 3.0</td>
<td>Vanilla JavaScript</td>
<td>Docker Compose</td>
</tr>
<tr>
<td>ThreadPoolExecutor</td>
<td>Responsive Design</td>
<td>本地文件缓存</td>
</tr>
</table>

---

## 📊 性能指标

<div align="center">

| 指标 | 数值 |
|------|------|
| 成功率 | 100% |
| 平均响应 | 4.44秒 |
| 并发线程 | 10个 |
| 缓存TTL | 1小时 |
| 最快镜像 | 清华 0.65s |

</div>

---

## 🗺️ 路线图

查看 [ROADMAP.md](ROADMAP.md) 了解详细规划。

**v0.6 计划：**
- [ ] Redis 缓存
- [ ] 用户评分系统
- [ ] 批量测速
- [ ] 多地区测速

**未来计划：**
- [ ] 微信小程序
- [ ] Electron 客户端
- [ ] 浏览器插件
- [ ] API 服务商业化

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

查看 [贡献指南](CONTRIBUTING.md) 了解详情。

**贡献者：**

<a href="https://github.com/yourusername/downloadhub/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=yourusername/downloadhub" />
</a>

---

## 📄 许可证

[MIT License](LICENSE)

---

## 🙏 致谢

感谢以下镜像站提供服务：
- [清华大学开源软件镜像站](https://mirrors.tuna.tsinghua.edu.cn/)
- [阿里云开源镜像站](https://mirrors.aliyun.com/)
- [中国科学技术大学开源镜像站](https://mirrors.ustc.edu.cn/)
- [腾讯云开源镜像站](https://mirrors.cloud.tencent.com/)

---

## 📮 联系方式

- GitHub Issues: [提交问题](https://github.com/yourusername/downloadhub/issues)
- Email: your@email.com

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/downloadhub&type=Date)](https://star-history.com/#yourusername/downloadhub&Date)

---

<div align="center">

**如果这个项目对你有帮助，请给个 ⭐ Star 支持一下！**

Made with ❤️ by [Your Name]

</div>
