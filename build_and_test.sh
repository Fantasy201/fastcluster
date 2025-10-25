#!/bin/bash

# 构建和测试脚本：原版 vs 优化版 fastcluster

set -e  # 遇到错误时退出

echo "FastCluster 构建和性能对比测试"
echo "================================="

# 检查依赖
echo "检查依赖..."
python -c "import numpy, scipy" || {
    echo "错误: 需要安装 numpy 和 scipy"
    exit 1
}

# 1. 安装原版 fastcluster
echo ""
echo "1. 安装原版 fastcluster..."
pip install fastcluster --force-reinstall

# 2. 构建优化版 xinyi_fastcluster
echo ""
echo "2. 构建优化版 xinyi_fastcluster..."

# 检查 OpenMP 支持
echo "检查 OpenMP 支持..."
if [ -f "/opt/homebrew/opt/libomp/include/omp.h" ]; then
    echo "✓ 检测到 Homebrew libomp (Apple Silicon)"
    export OPENMP_AVAILABLE=1
elif [ -f "/usr/local/opt/libomp/include/omp.h" ]; then
    echo "✓ 检测到 Homebrew libomp (Intel Mac)"
    export OPENMP_AVAILABLE=1
elif python -c "import os; print('Conda OpenMP:', os.path.exists(os.environ.get('CONDA_PREFIX', '') + '/include/omp.h'))" | grep -q "True"; then
    echo "✓ 检测到 Conda OpenMP"
    export OPENMP_AVAILABLE=1
else
    echo "⚠ 未检测到 OpenMP 支持，将禁用并行化"
    export DISABLE_OPENMP=1
fi

cd xinyi_fastcluster_package

# 清理之前的构建
rm -rf build/ dist/ *.egg-info/

# 构建包
python setup.py build_ext --inplace

# 安装到开发环境
pip install -e . --force-reinstall

cd ..

# 3. 运行性能对比测试
echo ""
echo "3. 运行性能对比测试..."
python benchmark_comparison.py

echo ""
echo "构建和测试完成！"
echo ""
echo "使用方法："
echo "  import xinyi_fastcluster as fastcluster"
echo "  Z = fastcluster.linkage_vector(X, method='single')"
