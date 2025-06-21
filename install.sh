#!/bin/bash

# iOS Migration MCP Server 安装脚本

set -e

echo "🚀 开始安装 iOS Migration MCP Server..."

# 检查Python版本
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ 错误: 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 创建虚拟环境（可选）
if [ "$1" = "--venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ 虚拟环境已激活"
fi

# 安装依赖
echo "📦 安装依赖包..."
pip install -r requirements.txt

# 安装包
echo "📦 安装iOS Migration MCP Server..."
pip install -e .

echo "✅ 安装完成！"
echo ""
echo "🎯 使用方法:"
echo "1. 启动服务器: python main.py"
echo "2. 在Cursor中配置MCP服务器"
echo "3. 使用工具: ios_scan_project() 和 ios_optimize_file()"
echo ""
echo "�� 更多信息请查看 README.md" 