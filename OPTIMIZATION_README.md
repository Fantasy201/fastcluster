# FastCluster 性能优化指南

本文档描述了为 fastcluster 库实施的性能优化措施。

## 优化概述

我们按照以下优先级实施了多项优化：

1. **SIMD 向量化优化** - 跨平台支持 (AVX2, SSE2, ARM NEON)
2. **并行计算优化** - OpenMP 多线程支持
3. **内存访问优化** - 缓存友好的数据布局和访问模式
4. **算法优化** - 改进的核心聚类算法
5. **编译器优化** - 高级编译器优化和分支预测

## 构建优化版本

### 自动构建脚本

使用提供的构建脚本自动检测 CPU 特性并启用相应优化：

```bash
./optimized_build.sh
```

### 手动构建

如果需要手动控制构建选项：

```bash
# 启用所有优化
python setup.py build_ext --inplace \
    --define=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION \
    --compiler-flags="-O3 -mavx2 -mfma -fopenmp -march=native -funroll-loops -ffast-math -flto"
```

### 编译器标志说明

- `-O3`: 最高级别优化
- `-mavx2 -mfma`: 启用 AVX2 和 FMA 指令集
- `-fopenmp`: 启用 OpenMP 并行化
- `-march=native`: 针对当前 CPU 优化
- `-funroll-loops`: 循环展开
- `-ffast-math`: 快速数学运算
- `-flto`: 链接时优化

## 运行时优化

### 设置 OpenMP 环境变量

```bash
# 设置线程数（通常等于 CPU 核心数）
export OMP_NUM_THREADS=8

# 绑定线程到 CPU 核心
export OMP_PROC_BIND=true
export OMP_PLACES=cores

# 设置线程调度策略
export OMP_SCHEDULE=dynamic
```

### Python 中使用

```python
import os
import fastcluster
import numpy as np

# 设置线程数
os.environ['OMP_NUM_THREADS'] = '8'

# 生成测试数据
X = np.random.randn(1000, 100)

# 使用优化的聚类算法
Z = fastcluster.linkage_vector(X, method='single')
```

## 性能测试

运行性能测试脚本：

```bash
python performance_test.py
```

该脚本将测试：
- 不同数据大小的性能
- SIMD 优化效果
- 并行扩展性
- 不同聚类方法的性能

## 优化详情

### 1. SIMD 向量化

- **AVX2**: 支持 256 位向量操作，4 个 double 同时处理
- **SSE2**: 支持 128 位向量操作，2 个 double 同时处理  
- **ARM NEON**: ARM 平台的向量化支持
- **自动检测**: 运行时自动检测可用的 SIMD 特性

### 2. 并行计算

- **OpenMP**: 多线程并行化距离计算和最近邻搜索
- **动态调度**: 使用 `schedule(dynamic)` 平衡负载
- **线程安全**: 确保多线程环境下的正确性

### 3. 内存优化

- **缓存对齐**: 关键数据结构按缓存行对齐
- **数据预取**: 使用 `__builtin_prefetch` 预取数据
- **访问模式**: 优化内存访问模式以提高缓存命中率

### 4. 编译器优化

- **分支预测**: 使用 `__builtin_expect` 优化分支预测
- **限制指针**: 使用 `__restrict__` 帮助编译器优化
- **循环展开**: 自动展开关键循环

## 性能提升预期

根据优化类型，预期性能提升：

- **SIMD 优化**: 2-4x 提升（取决于向量大小）
- **并行优化**: 2-8x 提升（取决于 CPU 核心数）
- **内存优化**: 10-30% 提升
- **编译器优化**: 5-15% 提升

总体预期提升：**3-10x**（取决于硬件和数据特征）

## 兼容性

### 支持的平台

- **x86_64**: Linux, macOS, Windows
- **ARM64**: Linux (支持 NEON)
- **编译器**: GCC 4.9+, Clang 3.5+, MSVC 2015+

### 依赖项

- **OpenMP**: 可选，用于并行化
- **NumPy**: 必需
- **SciPy**: 用于某些距离计算

## 故障排除

### 常见问题

1. **编译错误**: 确保编译器支持所需的指令集
2. **运行时错误**: 检查 OpenMP 库是否正确安装
3. **性能未提升**: 验证 SIMD 指令集是否被正确检测

### 调试模式

禁用优化进行调试：

```bash
python setup.py build_ext --inplace \
    --compiler-flags="-O0 -g -DDEBUG"
```

## 贡献

欢迎提交性能改进建议和 bug 报告。在提交前请确保：

1. 运行完整的测试套件
2. 进行性能基准测试
3. 验证跨平台兼容性
