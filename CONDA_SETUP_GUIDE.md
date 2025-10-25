# Conda环境配置指南

## 概述

本指南将帮助你在conda环境中配置和构建优化的`xinyi_fastcluster`包。

## 环境要求

- macOS (ARM64/Apple Silicon) 或 Linux
- Conda (Miniforge/Anaconda/Miniconda)
- Python 3.10+

## 快速开始

### 1. 激活conda

```bash
# 如果conda不在PATH中，先初始化
~/miniforge3/bin/conda init zsh  # 或 bash
source ~/.zshrc  # 重新加载shell配置
```

### 2. 创建开发环境

```bash
# 创建专用环境
conda create -n fastcluster_dev python=3.10 -y
conda activate fastcluster_dev

# 安装基础依赖
conda install numpy scipy -y
```

### 3. 构建优化版本

```bash
# 进入项目目录
cd /Users/xinyi/Projects/fastcluster

# 运行简化构建（禁用OpenMP和快速数学，确保兼容性）
./simple_build.sh
```

## 构建选项

### 简化构建（推荐）

```bash
# 禁用OpenMP和快速数学，确保最大兼容性
export DISABLE_OPENMP=1
export DISABLE_FAST_MATH=1
./simple_build.sh
```

### 完整优化构建

```bash
# 启用所有优化（需要OpenMP支持）
./test_build.sh
```

## 环境配置详情

### 检测到的优化

构建脚本会自动检测并启用以下优化：

- **架构优化**: Apple Silicon (ARM64) 或 x86_64
- **编译器优化**: -O3, -funroll-loops
- **SIMD支持**: ARM NEON (ARM64) 或 AVX2/SSE2 (x86_64)
- **OpenMP并行化**: 如果可用

### 编译器设置

- **Conda环境**: 自动使用conda的编译器
- **系统环境**: 使用系统默认编译器
- **OpenMP**: 优先使用conda的llvm-openmp

## 故障排除

### 1. conda命令未找到

```bash
# 查找conda安装位置
ls -la ~/miniforge3/bin/conda
ls -la ~/anaconda3/bin/conda
ls -la ~/miniconda3/bin/conda

# 初始化conda
~/miniforge3/bin/conda init zsh
source ~/.zshrc
```

### 2. OpenMP编译错误

```bash
# 禁用OpenMP
export DISABLE_OPENMP=1
./simple_build.sh
```

### 3. 快速数学编译错误

```bash
# 禁用快速数学
export DISABLE_FAST_MATH=1
./simple_build.sh
```

### 4. 模块导入错误

确保：
- 使用正确的Python环境
- 构建成功完成
- 模块名称匹配

## 性能测试

### 基本功能测试

```python
import fastcluster
import numpy as np

# 测试数据
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], dtype=np.float64)

# 执行聚类
Z = fastcluster.linkage_vector(X, method='single')
print(f"聚类结果形状: {Z.shape}")
```

### 性能基准测试

```bash
# 运行完整性能测试
./build_and_test.sh
```

## 打包分发

### 创建wheel包

```bash
# 构建分发包
./package_xinyi_fastcluster.sh
```

### 安装到其他项目

```bash
# 安装本地wheel
pip install dist/xinyi_fastcluster-1.3.0-*.whl

# 或在其他项目中使用
pip install /path/to/xinyi_fastcluster-1.3.0-*.whl
```

## 环境信息

### 检查当前环境

```bash
# 激活环境
conda activate fastcluster_dev

# 检查环境信息
python --version
gcc --version
g++ --version

# 检查OpenMP
python -c "import os; print('OpenMP:', os.path.exists(os.environ.get('CONDA_PREFIX', '') + '/include/omp.h'))"
```

### 环境变量

- `CONDA_PREFIX`: conda环境路径
- `DISABLE_OPENMP`: 禁用OpenMP并行化
- `DISABLE_FAST_MATH`: 禁用快速数学优化

## 下一步

1. **性能测试**: 运行`./build_and_test.sh`进行完整测试
2. **打包分发**: 使用`./package_xinyi_fastcluster.sh`创建wheel包
3. **集成使用**: 在其他项目中安装和使用优化版本

## 支持

如果遇到问题：

1. 检查conda环境是否正确激活
2. 确认所有依赖已安装
3. 查看构建日志中的错误信息
4. 尝试简化构建选项（禁用OpenMP/快速数学）

---

**注意**: 本指南针对macOS ARM64 (Apple Silicon) 优化，其他平台可能需要调整编译器选项。
