#!/bin/bash

# 设置conda环境用于构建fastcluster

set -e

echo "设置Conda环境用于fastcluster开发"
echo "================================="

# 检查conda是否可用
if ! command -v conda &> /dev/null; then
    echo "错误: conda未找到"
    echo "请确保conda已安装并添加到PATH"
    exit 1
fi

echo "✓ Conda已找到"

# 创建或激活环境
ENV_NAME="fastcluster_dev"

if conda env list | grep -q $ENV_NAME; then
    echo "环境 $ENV_NAME 已存在，正在激活..."
    conda activate $ENV_NAME
else
    echo "创建新环境 $ENV_NAME..."
    conda create -n $ENV_NAME python=3.10 -y
    conda activate $ENV_NAME
fi

echo "✓ 环境已激活: $ENV_NAME"

# 安装基础依赖
echo "安装基础依赖..."
conda install numpy scipy -y

# 安装构建工具
echo "安装构建工具..."
conda install gcc_osx-64 gxx_osx-64 -y  # macOS
# conda install gcc_linux-64 gxx_linux-64 -y  # Linux

# 安装OpenMP
echo "安装OpenMP..."
conda install openmp -y

# 安装其他有用的工具
echo "安装其他工具..."
conda install setuptools wheel -y

echo ""
echo "环境设置完成！"
echo ""
echo "使用方法："
echo "1. 激活环境: conda activate $ENV_NAME"
echo "2. 运行构建: ./test_build.sh"
echo "3. 运行完整测试: ./build_and_test.sh"
echo ""
echo "当前环境信息："
echo "Python: $(python --version)"
echo "GCC: $(gcc --version | head -1)"
echo "G++: $(g++ --version | head -1)"
echo "OpenMP: $(python -c 'import os; print(os.path.exists(os.environ.get("CONDA_PREFIX", "") + "/include/omp.h"))')"
