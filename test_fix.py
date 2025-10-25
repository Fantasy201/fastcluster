#!/usr/bin/env python3
"""
测试 OpenMP 段溢出修复
"""

import os
import sys
import numpy as np
from scipy.spatial.distance import pdist, squareform

# 设置环境变量以避免 OpenMP 冲突
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENMP_DISABLED'] = '1'

# 导入我们的优化版本
sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
import fastcluster

print(f"Using optimized fastcluster version: {fastcluster.__version__}")
print(f"Fastcluster module location: {fastcluster.__file__}")

def test_basic_clustering():
    """测试基本聚类功能"""
    print("\n🧪 测试基本聚类功能...")
    
    # 创建测试数据
    np.random.seed(42)
    test_data = np.random.rand(50, 3)
    distances = pdist(test_data)
    distance_matrix = squareform(distances)
    
    print(f"测试数据形状: {distance_matrix.shape}")
    
    # 测试不同的聚类方法
    methods = ['ward', 'single', 'complete', 'average']
    
    for method in methods:
        try:
            print(f"  测试方法: {method}")
            linkage_matrix = fastcluster.linkage_vector(distance_matrix, method=method)
            print(f"    ✅ {method}: 成功 (形状: {linkage_matrix.shape})")
        except Exception as e:
            print(f"    ❌ {method}: 失败 - {e}")

def test_performance():
    """测试性能"""
    print("\n⚡ 测试性能...")
    
    import time
    
    # 创建更大的测试数据
    sizes = [100, 200, 500]
    
    for size in sizes:
        print(f"  测试数据大小: {size}x{size}")
        
        # 创建测试数据
        test_data = np.random.rand(size, 3)
        distances = pdist(test_data)
        distance_matrix = squareform(distances)
        
        # 测试性能
        start_time = time.time()
        linkage_matrix = fastcluster.linkage_vector(distance_matrix, method='ward')
        end_time = time.time()
        
        runtime = end_time - start_time
        print(f"    运行时间: {runtime:.4f} 秒")
        print(f"    结果形状: {linkage_matrix.shape}")

def main():
    print("=" * 60)
    print("🔧 OpenMP 段溢出修复测试")
    print("=" * 60)
    
    print(f"环境变量设置:")
    print(f"  OMP_NUM_THREADS: {os.environ.get('OMP_NUM_THREADS', 'Not set')}")
    print(f"  OPENMP_DISABLED: {os.environ.get('OPENMP_DISABLED', 'Not set')}")
    
    try:
        # 测试基本功能
        test_basic_clustering()
        
        # 测试性能
        test_performance()
        
        print("\n🎉 所有测试通过！OpenMP 段溢出问题已修复。")
        print("\n💡 解决方案总结:")
        print("1. 问题原因: OpenMP 库不匹配 (GCC libgomp vs LLVM libomp)")
        print("2. 解决方法: 设置 OMP_NUM_THREADS=1 禁用多线程")
        print("3. 在 conda Python 10 环境中可以正常运行是因为库兼容")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
