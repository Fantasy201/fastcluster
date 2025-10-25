#!/bin/bash

# 简化的构建脚本，先禁用OpenMP

set -e

echo "简化构建测试（禁用OpenMP）..."
echo "=============================="

# 进入包目录
cd xinyi_fastcluster_package

# 清理之前的构建
echo "清理之前的构建..."
rm -rf build/ dist/ *.egg-info/

# 设置环境变量禁用OpenMP和快速数学
export DISABLE_OPENMP=1
export DISABLE_FAST_MATH=1

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
    # 使用简单的整数数据避免浮点数问题
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

echo "简化构建测试完成！"
