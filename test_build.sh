#!/bin/bash

# 简化的构建测试脚本

set -e

echo "测试构建 xinyi_fastcluster..."
echo "=============================="

# 检查Python环境
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
else
    echo "错误: 未找到Python"
    exit 1
fi

echo "使用Python: $($PYTHON_CMD --version)"

# 进入包目录
cd xinyi_fastcluster_package

# 清理之前的构建
echo "清理之前的构建..."
rm -rf build/ dist/ *.egg-info/

# 构建包
echo "构建包..."
$PYTHON_CMD setup.py build_ext --inplace

echo "构建完成！"

# 测试导入
echo "测试导入..."
$PYTHON_CMD -c "
try:
    import fastcluster
    print('✓ fastcluster 导入成功')
    print(f'版本: {fastcluster.__version__}')
    
    # 简单测试
    import numpy as np
    X = np.random.randn(10, 5)
    Z = fastcluster.linkage_vector(X, method='single')
    print('✓ 简单聚类测试通过')
    print(f'结果形状: {Z.shape}')
    
except Exception as e:
    print(f'✗ 测试失败: {e}')
    import traceback
    traceback.print_exc()
"

cd ..

echo "测试完成！"
