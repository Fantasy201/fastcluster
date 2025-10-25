#!/bin/bash
# 修复 OpenMP 段溢出的运行脚本

echo "🔧 修复 OpenMP 段溢出问题..."
echo "问题原因: OpenMP 库不匹配 (GCC libgomp vs LLVM libomp)"
echo "解决方法: 设置 OMP_NUM_THREADS=1 禁用多线程"
echo ""

# 设置环境变量以避免 OpenMP 冲突
export OMP_NUM_THREADS=1
export OPENMP_DISABLED=1

echo "✅ 已设置环境变量:"
echo "  OMP_NUM_THREADS=1"
echo "  OPENMP_DISABLED=1"
echo ""

# 运行原始命令
echo "🚀 运行测试..."
python3 tests/test_time.py
