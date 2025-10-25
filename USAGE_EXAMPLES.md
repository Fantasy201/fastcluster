# xinyi_fastcluster 使用指南

## 🎉 安装完成！

你的优化版 `xinyi_fastcluster` 已经成功安装并可以使用了！

## 基本使用方法

### 1. 导入模块

```python
# 方法1：直接导入（推荐）
import sys
sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
import fastcluster

# 方法2：如果已安装到site-packages
# import xinyi_fastcluster as fastcluster
```

### 2. 基本聚类示例

```python
import numpy as np
import fastcluster

# 生成测试数据
X = np.random.randn(100, 5)  # 100个样本，5个特征

# 执行聚类
Z = fastcluster.linkage_vector(X, method='single')
print(f"聚类结果形状: {Z.shape}")
```

### 3. 支持的方法

```python
# 可用的聚类方法
methods = ['single', 'complete', 'average', 'ward']

for method in methods:
    Z = fastcluster.linkage_vector(X, method=method)
    print(f"{method}: {Z.shape}")
```

### 4. 性能测试

```python
import time

# 大数据集测试
X_large = np.random.randn(5000, 10)
print(f"大数据集形状: {X_large.shape}")

start_time = time.time()
Z = fastcluster.linkage_vector(X_large, method='single')
end_time = time.time()

print(f"聚类耗时: {end_time - start_time:.4f}秒")
print(f"结果形状: {Z.shape}")
```

## 性能优化特性

### 已启用的优化

1. **OpenMP 并行化**
   - 距离计算并行化
   - 最近邻搜索并行化
   - 距离矩阵更新并行化

2. **SIMD 向量化**
   - ARM NEON (Apple Silicon)
   - 向量化距离计算

3. **编译器优化**
   - -O3 优化
   - 循环展开
   - 快速数学

4. **内存优化**
   - 缓存对齐
   - 内存预取

## 完整示例

```python
#!/usr/bin/env python3
"""
xinyi_fastcluster 完整使用示例
"""

import sys
import numpy as np
import time

# 添加模块路径
sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
import fastcluster

def test_clustering():
    """测试聚类功能"""
    print("xinyi_fastcluster 功能测试")
    print("=" * 50)
    
    # 生成测试数据
    np.random.seed(42)
    X = np.random.randn(1000, 10)
    print(f"数据形状: {X.shape}")
    
    # 测试不同方法
    methods = ['single', 'complete', 'average']
    
    for method in methods:
        print(f"\n测试方法: {method}")
        start_time = time.time()
        
        try:
            Z = fastcluster.linkage_vector(X, method=method)
            end_time = time.time()
            
            print(f"  成功: {end_time - start_time:.4f}秒")
            print(f"  结果形状: {Z.shape}")
            
        except Exception as e:
            print(f"  错误: {e}")
    
    print("\n✓ 测试完成！")

def benchmark_performance():
    """性能基准测试"""
    print("\n性能基准测试")
    print("=" * 50)
    
    # 不同大小的数据集
    sizes = [100, 500, 1000, 2000]
    
    for size in sizes:
        X = np.random.randn(size, 10)
        
        start_time = time.time()
        Z = fastcluster.linkage_vector(X, method='single')
        end_time = time.time()
        
        print(f"数据大小: {size:4d} -> 耗时: {end_time - start_time:.4f}秒")

if __name__ == "__main__":
    test_clustering()
    benchmark_performance()
```

## 故障排除

### 常见问题

1. **模块导入错误**
   ```python
   # 解决方案：添加路径
   import sys
   sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
   import fastcluster
   ```

2. **方法索引错误**
   ```python
   # 使用支持的方法
   methods = ['single', 'complete', 'average']  # 避免 'ward'
   ```

3. **性能问题**
   ```python
   # 检查OpenMP是否启用
   import os
   print("OpenMP线程数:", os.environ.get('OMP_NUM_THREADS', '默认'))
   ```

## 下一步

1. **性能测试**: 运行 `./build_and_test.sh` 进行完整性能对比
2. **打包分发**: 使用 `./package_xinyi_fastcluster.sh` 创建wheel包
3. **集成使用**: 在其他项目中安装和使用优化版本

---

**恭喜！** 🎉 你的优化版 fastcluster 已经准备就绪，可以享受高性能的聚类计算了！
