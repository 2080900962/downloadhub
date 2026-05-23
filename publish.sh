#!/bin/bash

echo "🚀 DownloadHub 一键发布脚本"
echo "================================"
echo ""

# 检查是否在正确的目录
if [ ! -f "run.py" ]; then
    echo "❌ 错误：请在项目根目录运行此脚本"
    exit 1
fi

# 检查 git 是否已初始化
if [ ! -d ".git" ]; then
    echo "📦 初始化 Git 仓库..."
    git init
fi

# 清理缓存文件
echo "🧹 清理缓存文件..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.log" -delete 2>/dev/null

# 添加所有文件
echo "📝 添加文件到 Git..."
git add .

# 提交代码
echo "💾 提交代码..."
git commit -m "🎉 Initial release v0.5.0

✨ Features:
- Smart search for fastest download sources
- Concurrent speed testing (10 threads)
- Intelligent caching (1 hour TTL)
- Modern responsive UI
- Docker deployment support
- Complete documentation

🎯 Supported sources:
- GitHub (ghproxy)
- Node.js (npmmirror, tuna)
- PyTorch (tuna, aliyun)
- PyPI (tuna, aliyun)
- Common mirrors (tuna, aliyun, ustc, tencent)

📊 Performance:
- Success rate: 100%
- Average response: 4.44s
- Concurrent threads: 10
- Fastest mirror: 0.65s (tuna)

🛠️ Tech stack:
- Python 3.12 + Flask 3.0
- Vanilla JavaScript
- Docker + Docker Compose

📝 Documentation:
- Complete README
- Architecture docs
- Roadmap
- Contributing guide
- Changelog"

# 提示用户输入 GitHub 仓库地址
echo ""
echo "📮 请输入你的 GitHub 仓库地址："
echo "格式：https://github.com/yourusername/downloadhub.git"
read -p "仓库地址: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ 错误：仓库地址不能为空"
    exit 1
fi

# 添加远程仓库
echo "🔗 添加远程仓库..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"

# 推送到 GitHub
echo "⬆️  推送到 GitHub..."
git branch -M main
git push -u origin main

# 创建标签
echo "🏷️  创建版本标签..."
git tag -a v0.5.0 -m "Release v0.5.0 - Production ready"
git push origin v0.5.0

echo ""
echo "✅ 发布完成！"
echo ""
echo "📋 下一步："
echo "1. 访问你的 GitHub 仓库"
echo "2. 点击 'Releases' → 'Create a new release'"
echo "3. 选择标签 v0.5.0"
echo "4. 复制 GitHub发布指南.md 中的 Release 描述"
echo "5. 发布！"
echo ""
echo "🎉 恭喜！你的项目已成功发布到 GitHub！"
