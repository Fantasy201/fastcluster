#!/usr/bin/env python3
"""
xinyi_fastcluster 的 setup.py 配置文件
这是优化版的 fastcluster，包含 SIMD 和并行计算优化
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import os
import sys
import platform
import subprocess

# 延迟导入numpy，避免在setup.py执行时导入失败
def get_numpy_include():
    try:
        import numpy
        return numpy.get_include()
    except ImportError:
        # 如果numpy不可用，返回默认路径
        return '/usr/include'

# 检测 CPU 特性和编译器优化
def get_optimization_flags():
    """获取优化编译标志"""
    flags = []
    
    # 基础优化
    flags.extend(['-O3', '-DNDEBUG', '-funroll-loops'])
    
    # 检查是否禁用快速数学
    import os
    if not os.environ.get('DISABLE_FAST_MATH', ''):
        flags.append('-ffast-math')
        print("✓ 快速数学优化已启用")
    else:
        print("⚠ 快速数学优化已禁用")
    
    # 检测架构
    import platform
    machine = platform.machine().lower()
    system = platform.system().lower()
    
    print(f"检测到架构: {machine} ({system})")
    
    # 架构特定的优化
    if machine == 'arm64' or machine == 'aarch64':
        # ARM64 架构 (Apple Silicon, ARM服务器)
        if system == 'darwin':
            # macOS ARM64 - 使用Apple Silicon优化
            flags.extend(['-mcpu=native', '-mtune=native'])
            print("✓ Apple Silicon 优化已启用")
        else:
            # Linux ARM64
            flags.extend(['-mcpu=native', '-mtune=native'])
            flags.append('-mfpu=neon')
            print("✓ ARM64 NEON 优化已启用")
        
    elif machine == 'x86_64' or machine == 'amd64':
        # x86_64 架构
        flags.extend(['-march=native', '-mtune=native'])
        print("✓ x86_64 优化已启用")
        
        # 检测 x86 SIMD 支持
        try:
            # 检查 AVX2 支持
            result = subprocess.run(['grep', '-q', 'avx2', '/proc/cpuinfo'], 
                                  capture_output=True, check=False)
            if result.returncode == 0:
                flags.extend(['-mavx2', '-mfma'])
                print("✓ AVX2 支持已启用")
            
            # 检查 AVX 支持
            result = subprocess.run(['grep', '-q', 'avx', '/proc/cpuinfo'], 
                                  capture_output=True, check=False)
            if result.returncode == 0:
                flags.append('-mavx')
                print("✓ AVX 支持已启用")
            
            # SSE2 通常都支持
            flags.append('-msse2')
            print("✓ SSE2 支持已启用")
            
        except:
            # 如果检测失败，使用保守的优化
            flags.extend(['-msse2'])
            print("⚠ 使用保守的 x86 SIMD 优化")
    else:
        # 其他架构，使用通用优化
        print(f"⚠ 未知架构 {machine}，使用通用优化")
    
    # 检查是否禁用OpenMP
    import os
    if os.environ.get('DISABLE_OPENMP', ''):
        print("⚠ OpenMP 已被禁用")
        openmp_found = False
    else:
        # 检查 OpenMP 支持
        openmp_found = False
    
        # 方法1: 检查 Homebrew 的 libomp (macOS 优先)
        if system == 'darwin':
            try:
                import os
                # 检查 Apple Silicon Homebrew
                if os.path.exists('/opt/homebrew/opt/libomp/include/omp.h'):
                    flags.extend(['-fopenmp', '-I/opt/homebrew/opt/libomp/include', '-L/opt/homebrew/opt/libomp/lib'])
                    openmp_found = True
                    print("✓ OpenMP 支持已启用 (Homebrew libomp - Apple Silicon)")
                # 检查 Intel Mac Homebrew
                elif os.path.exists('/usr/local/opt/libomp/include/omp.h'):
                    flags.extend(['-fopenmp', '-I/usr/local/opt/libomp/include', '-L/usr/local/opt/libomp/lib'])
                    openmp_found = True
                    print("✓ OpenMP 支持已启用 (Homebrew libomp - Intel Mac)")
            except:
                pass
        
        # 方法2: 检查 conda 的 openmp
        if not openmp_found:
            try:
                import os
                conda_prefix = os.environ.get('CONDA_PREFIX', '')
                if conda_prefix and os.path.exists(f'{conda_prefix}/include/omp.h'):
                    flags.extend(['-fopenmp', f'-I{conda_prefix}/include', f'-L{conda_prefix}/lib'])
                    openmp_found = True
                    print("✓ OpenMP 支持已启用 (Conda)")
                    # 设置编译器环境变量
                    os.environ['CC'] = 'gcc'
                    os.environ['CXX'] = 'g++'
            except:
                pass
        
        # 方法3: 检查 pkg-config (Linux/Windows)
        if not openmp_found:
            try:
                result = subprocess.run(['pkg-config', '--exists', 'omp'], 
                                      capture_output=True, check=False)
                if result.returncode == 0:
                    flags.append('-fopenmp')
                    openmp_found = True
                    print("✓ OpenMP 支持已启用 (pkg-config)")
            except:
                pass
        
        # 方法4: 检查系统默认 OpenMP (Linux)
        if not openmp_found and system == 'linux':
            try:
                result = subprocess.run(['gcc', '-fopenmp', '--version'], 
                                      capture_output=True, check=False)
                if result.returncode == 0:
                    flags.append('-fopenmp')
                    openmp_found = True
                    print("✓ OpenMP 支持已启用 (系统 GCC)")
            except:
                pass
        
        if not openmp_found:
            print("⚠ OpenMP 未找到，将禁用并行化")
    
    # 链接时优化
    flags.append('-flto')
    
    return flags

class OptimizedBuildExt(build_ext):
    """自定义构建扩展，添加优化标志"""
    
    def build_extensions(self):
        import os
        import platform
        
        # 获取优化标志
        opt_flags = get_optimization_flags()
        
        # 检查是否在conda环境中
        conda_prefix = os.environ.get('CONDA_PREFIX', '')
        if conda_prefix:
            print(f"检测到Conda环境: {conda_prefix}")
            # 设置环境变量以使用conda的编译器
            os.environ['CC'] = 'gcc'
            os.environ['CXX'] = 'g++'
        
        # 检查是否有Homebrew libomp (macOS)
        system = platform.system().lower()
        if system == 'darwin':
            if os.path.exists('/opt/homebrew/opt/libomp/include/omp.h') or os.path.exists('/usr/local/opt/libomp/include/omp.h'):
                print("检测到Homebrew libomp，将使用Homebrew GCC")
                # 使用Homebrew的GCC而不是系统clang++
                if os.path.exists('/opt/homebrew/bin/gcc-15'):
                    os.environ['CC'] = '/opt/homebrew/bin/gcc-15'
                    os.environ['CXX'] = '/opt/homebrew/bin/g++-15'
                    print("使用Homebrew GCC-15")
                    # 强制设置编译器
                    import distutils.sysconfig
                    distutils.sysconfig.get_config_vars()['CC'] = '/opt/homebrew/bin/gcc-15'
                    distutils.sysconfig.get_config_vars()['CXX'] = '/opt/homebrew/bin/g++-15'
                elif os.path.exists('/usr/local/bin/gcc-15'):
                    os.environ['CC'] = '/usr/local/bin/gcc-15'
                    os.environ['CXX'] = '/usr/local/bin/g++-15'
                    print("使用Homebrew GCC-15 (Intel Mac)")
                    # 强制设置编译器
                    import distutils.sysconfig
                    distutils.sysconfig.get_config_vars()['CC'] = '/usr/local/bin/gcc-15'
                    distutils.sysconfig.get_config_vars()['CXX'] = '/usr/local/bin/g++-15'
                else:
                    print("未找到Homebrew GCC，将使用系统编译器")
        
        # 应用到所有扩展
        for ext in self.extensions:
            ext.extra_compile_args.extend(opt_flags)
            ext.extra_link_args.extend(opt_flags)
        
        # 调用父类方法
        super().build_extensions()

# 获取 NumPy 包含目录
numpy_include = get_numpy_include()

# 定义扩展模块
ext_modules = [
    Extension(
        name='_xinyi_fastcluster',
        sources=['src/fastcluster_python.cpp'],
        include_dirs=[numpy_include],
        language='c++',
        extra_compile_args=['-std=c++11'],
        extra_link_args=[],
    )
]

# 读取 README
def read_readme():
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return "Optimized fast hierarchical clustering with SIMD and parallelization"

# 读取版本信息
def get_version():
    try:
        with open('fastcluster.py', 'r') as f:
            for line in f:
                if line.startswith('__version__'):
                    version = line.split('=')[1].strip().strip("'\"")
                    return version
    except:
        pass
    return '1.3.0'

setup(
    name='xinyi_fastcluster',
    version=get_version(),
    author='Xinyi',
    author_email='1836724126@qq.com',
    description='Optimized fast hierarchical clustering with SIMD and parallelization',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/xinyi/fastcluster',
    py_modules=['fastcluster'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': OptimizedBuildExt},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: C++',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.7',
    install_requires=[
        'numpy>=1.7.0',
        'scipy>=0.9.0',
    ],
    extras_require={
        'dev': [
            'pytest>=3.0.0',
            'pytest-benchmark',
        ],
    },
    keywords='clustering, hierarchical, fast, simd, parallel, optimization',
    project_urls={
        'Bug Reports': 'https://github.com/xinyi/fastcluster/issues',
        'Source': 'https://github.com/xinyi/fastcluster',
        'Documentation': 'https://github.com/xinyi/fastcluster/blob/main/OPTIMIZATION_README.md',
    },
)
