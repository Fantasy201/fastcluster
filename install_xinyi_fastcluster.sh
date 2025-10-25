#!/bin/bash

# 简化的 xinyi_fastcluster 安装脚本

set -e

echo "安装 xinyi_fastcluster"
echo "======================"

# 设置编译器环境变量
export CC=/opt/homebrew/bin/gcc-15
export CXX=/opt/homebrew/bin/g++-15

echo "编译器设置:"
echo "CC: $CC"
echo "CXX: $CXX"

# 进入包目录
cd xinyi_fastcluster_package

# 清理之前的构建
echo "清理之前的构建..."
rm -rf build/ dist/ *.egg-info/

# 只构建，不安装
echo "构建模块..."
python setup.py build_ext --inplace

echo "构建完成！"

# 测试模块
echo "测试模块..."
python -c "
import sys
sys.path.insert(0, '.')
import fastcluster
print('✓ fastcluster 导入成功')
print(f'版本: {fastcluster.__version__}')

# 简单测试
import numpy as np
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], dtype=np.float64)
Z = fastcluster.linkage_vector(X, method='single')
print('✓ 简单聚类测试通过')
print(f'结果形状: {Z.shape}')
"

# 创建符号链接到site-packages
echo "创建符号链接..."
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")
echo "site-packages: $SITE_PACKAGES"

# 创建xinyi_fastcluster目录
mkdir -p "$SITE_PACKAGES/xinyi_fastcluster"

# 复制文件
cp fastcluster.py "$SITE_PACKAGES/xinyi_fastcluster/"
cp _xinyi_fastcluster*.so "$SITE_PACKAGES/xinyi_fastcluster/"

# 创建__init__.py
cat > "$SITE_PACKAGES/xinyi_fastcluster/__init__.py" << 'EOF'
from .fastcluster import *
__version__ = "1.3.0"
EOF

echo "安装完成！"
echo ""
echo "使用方法："
echo "  import xinyi_fastcluster as fastcluster"
echo "  Z = fastcluster.linkage_vector(X, method='single')"

cd ..

echo "安装完成！"
