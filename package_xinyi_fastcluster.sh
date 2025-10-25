#!/bin/bash

# 打包 xinyi_fastcluster 为可分发的轮子

set -e

echo "打包 xinyi_fastcluster..."
echo "========================="

cd xinyi_fastcluster_package

# 清理之前的构建
echo "清理之前的构建..."
rm -rf build/ dist/ *.egg-info/

# 构建轮子
echo "构建轮子..."
python setup.py bdist_wheel

# 构建源码分发
echo "构建源码分发..."
python setup.py sdist

# 显示结果
echo ""
echo "构建完成！生成的文件："
ls -la dist/

echo ""
echo "安装轮子："
echo "  pip install dist/xinyi_fastcluster-*.whl"
echo ""
echo "或者从源码安装："
echo "  pip install dist/xinyi_fastcluster-*.tar.gz"
echo ""
echo "或者直接安装到其他项目："
echo "  pip install /path/to/xinyi_fastcluster_package/"

cd ..
