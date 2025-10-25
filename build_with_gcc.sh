#!/bin/bash

# 使用 Homebrew GCC 构建 xinyi_fastcluster

set -e

echo "使用 Homebrew GCC 构建 xinyi_fastcluster"
echo "========================================"

# 设置编译器环境变量
export CC=/opt/homebrew/bin/gcc-15
export CXX=/opt/homebrew/bin/g++-15

echo "编译器设置:"
echo "CC: $CC"
echo "CXX: $CXX"

# 检查编译器是否可用
if [ ! -f "$CC" ]; then
    echo "错误: 找不到 GCC 编译器: $CC"
    echo "请运行: brew install gcc"
    exit 1
fi

if [ ! -f "$CXX" ]; then
    echo "错误: 找不到 G++ 编译器: $CXX"
    echo "请运行: brew install gcc"
    exit 1
fi

# 检查 OpenMP 支持
if [ ! -f "/opt/homebrew/opt/libomp/include/omp.h" ]; then
    echo "错误: 找不到 OpenMP 头文件"
    echo "请运行: brew install libomp"
    exit 1
fi

echo "✓ 编译器检查通过"
echo "✓ OpenMP 支持检查通过"

# 进入包目录
cd xinyi_fastcluster_package

# 清理之前的构建
echo "清理之前的构建..."
rm -rf build/ dist/ *.egg-info/

# 构建包
echo "构建包..."
python setup.py build_ext --inplace

echo "构建完成！"

# 测试导入
echo "测试导入..."
python -c "
try:
    import fastcluster
    print('✓ fastcluster 导入成功')
    print(f'版本: {fastcluster.__version__}')
    
    # 简单测试
    import numpy as np
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], dtype=np.float64)
    Z = fastcluster.linkage_vector(X, method='single')
    print('✓ 简单聚类测试通过')
    print(f'结果形状: {Z.shape}')
    
except Exception as e:
    print(f'✗ 测试失败: {e}')
    import traceback
    traceback.print_exc()
"

cd ..

echo "构建和测试完成！"
