#!/usr/bin/env python3
"""
xinyi_fastcluster 测试脚本
"""

import sys
import numpy as np
import time

# 添加模块路径
sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
import fastcluster

def test_basic_functionality():
    """测试基本功能"""
    print("xinyi_fastcluster 基本功能测试")
    print("=" * 50)
    
    # 生成测试数据
    np.random.seed(42)
    X = np.random.randn(100, 5)
    print(f"数据形状: {X.shape}")
    
    # 测试支持的方法
    methods = ['single', 'complete', 'average']
    
    for method in methods:
        print(f"\n测试方法: {method}")
        start_time = time.time()
        
        try:
            Z = fastcluster.linkage_vector(X, method=method)
            end_time = time.time()
            
            print(f"  ✓ 成功: {end_time - start_time:.4f}秒")
            print(f"  结果形状: {Z.shape}")
            
        except Exception as e:
            print(f"  ✗ 错误: {e}")
    
    print("\n✓ 基本功能测试完成！")

def test_performance():
    """性能测试"""
    print("\n性能测试")
    print("=" * 50)
    
    # 不同大小的数据集
    sizes = [100, 500, 1000]
    
    for size in sizes:
        X = np.random.randn(size, 10)
        
        start_time = time.time()
        Z = fastcluster.linkage_vector(X, method='single')
        end_time = time.time()
        
        print(f"数据大小: {size:4d} -> 耗时: {end_time - start_time:.4f}秒")

def test_optimization_features():
    """测试优化特性"""
    print("\n优化特性测试")
    print("=" * 50)
    
    # 检查OpenMP支持
    import os
    omp_threads = os.environ.get('OMP_NUM_THREADS', '默认')
    print(f"OpenMP线程数: {omp_threads}")
    
    # 大数据集测试
    X_large = np.random.randn(2000, 10)
    print(f"大数据集测试: {X_large.shape}")
    
    start_time = time.time()
    Z = fastcluster.linkage_vector(X_large, method='single')
    end_time = time.time()
    
    print(f"大数据集聚类耗时: {end_time - start_time:.4f}秒")
    print(f"结果形状: {Z.shape}")

if __name__ == "__main__":
    test_basic_functionality()
    test_performance()
    test_optimization_features()
    
    print("\n🎉 所有测试完成！")
    print("你的 xinyi_fastcluster 已经准备就绪！")
