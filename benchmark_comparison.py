#!/usr/bin/env python3
"""
性能对比测试：原版 vs 优化版 fastcluster
"""

import numpy as np
import time
import sys
import os
import subprocess
import tempfile
import shutil
from pathlib import Path

def install_package(package_name, package_path=None):
    """安装指定的包"""
    if package_path:
        cmd = [sys.executable, '-m', 'pip', 'install', package_path, '--force-reinstall']
    else:
        cmd = [sys.executable, '-m', 'pip', 'install', package_name, '--force-reinstall']
    
    print(f"Installing: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Installation failed: {result.stderr}")
        return False
    return True

def benchmark_clustering(data, method, package_name, iterations=3):
    """对指定包进行聚类性能测试"""
    try:
        if package_name == 'fastcluster':
            import fastcluster
            func = fastcluster.linkage_vector
        elif package_name == 'xinyi_fastcluster':
            import xinyi_fastcluster as fastcluster
            func = fastcluster.linkage_vector
        else:
            raise ImportError(f"Unknown package: {package_name}")
        
        times = []
        for i in range(iterations):
            start_time = time.time()
            Z = func(data, method=method)
            end_time = time.time()
            times.append(end_time - start_time)
        
        return {
            'mean_time': np.mean(times),
            'std_time': np.std(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'times': times
        }
    except Exception as e:
        print(f"Error benchmarking {package_name}: {e}")
        return None

def run_comparison():
    """运行完整的性能对比测试"""
    print("FastCluster 性能对比测试")
    print("=" * 60)
    
    # 测试配置
    test_cases = [
        (100, 10, "小数据集"),
        (500, 20, "中等数据集"),
        (1000, 50, "大数据集"),
        (2000, 100, "超大数据集"),
    ]
    
    methods = ['single', 'ward', 'centroid']
    
    # 设置OpenMP环境变量
    os.environ['OMP_NUM_THREADS'] = str(os.cpu_count())
    os.environ['OMP_PROC_BIND'] = 'true'
    os.environ['OMP_PLACES'] = 'cores'
    
    print(f"使用 {os.cpu_count()} 个CPU核心")
    print(f"OMP_NUM_THREADS = {os.environ['OMP_NUM_THREADS']}")
    print()
    
    results = {}
    
    for n_points, n_dim, description in test_cases:
        print(f"\n{description} ({n_points} 点, {n_dim} 维)")
        print("-" * 40)
        
        # 生成测试数据
        np.random.seed(42)
        X = np.random.randn(n_points, n_dim).astype(np.float64)
        
        results[description] = {}
        
        for method in methods:
            print(f"\n方法: {method}")
            
            # 测试原版
            print("  测试原版 fastcluster...")
            original_result = benchmark_clustering(X, method, 'fastcluster')
            
            # 测试优化版
            print("  测试优化版 xinyi_fastcluster...")
            optimized_result = benchmark_clustering(X, method, 'xinyi_fastcluster')
            
            if original_result and optimized_result:
                speedup = original_result['mean_time'] / optimized_result['mean_time']
                
                print(f"    原版时间:    {original_result['mean_time']:.4f}s ± {original_result['std_time']:.4f}s")
                print(f"    优化版时间:  {optimized_result['mean_time']:.4f}s ± {optimized_result['std_time']:.4f}s")
                print(f"    加速比:      {speedup:.2f}x")
                
                results[description][method] = {
                    'original': original_result,
                    'optimized': optimized_result,
                    'speedup': speedup
                }
            else:
                print("    测试失败")
    
    # 生成总结报告
    print("\n" + "=" * 60)
    print("性能对比总结")
    print("=" * 60)
    
    total_speedups = []
    for description, methods_data in results.items():
        print(f"\n{description}:")
        for method, data in methods_data.items():
            speedup = data['speedup']
            total_speedups.append(speedup)
            print(f"  {method:>10}: {speedup:.2f}x 加速")
    
    if total_speedups:
        avg_speedup = np.mean(total_speedups)
        max_speedup = np.max(total_speedups)
        min_speedup = np.min(total_speedups)
        
        print(f"\n总体统计:")
        print(f"  平均加速比: {avg_speedup:.2f}x")
        print(f"  最大加速比: {max_speedup:.2f}x")
        print(f"  最小加速比: {min_speedup:.2f}x")
    
    return results

def main():
    """主函数"""
    print("开始性能对比测试...")
    
    # 检查是否已安装两个版本
    try:
        import fastcluster
        print("✓ 原版 fastcluster 已安装")
    except ImportError:
        print("✗ 原版 fastcluster 未安装，正在安装...")
        if not install_package('fastcluster'):
            print("无法安装原版 fastcluster，退出测试")
            return
    
    try:
        import xinyi_fastcluster
        print("✓ 优化版 xinyi_fastcluster 已安装")
    except ImportError:
        print("✗ 优化版 xinyi_fastcluster 未安装")
        print("请先运行: pip install -e .")
        return
    
    # 运行对比测试
    results = run_comparison()
    
    print("\n测试完成！")

if __name__ == "__main__":
    main()
