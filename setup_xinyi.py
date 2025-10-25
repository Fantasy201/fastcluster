#!/usr/bin/env python3
"""
xinyi_fastcluster 的 setup.py 配置文件
这是优化版的 fastcluster，包含 SIMD 和并行计算优化
"""

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import numpy
import os
import sys
import platform
import subprocess

# 检测 CPU 特性和编译器优化
def get_optimization_flags():
    """获取优化编译标志"""
    flags = []
    
    # 基础优化
    flags.extend(['-O3', '-DNDEBUG', '-funroll-loops', '-ffast-math'])
    
    # 架构优化
    flags.extend(['-march=native', '-mtune=native'])
    
    # 检测 SIMD 支持
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
        print("⚠ 使用保守的 SIMD 优化")
    
    # 检查 OpenMP 支持
    try:
        result = subprocess.run(['pkg-config', '--exists', 'omp'], 
                              capture_output=True, check=False)
        if result.returncode == 0:
            flags.append('-fopenmp')
            print("✓ OpenMP 支持已启用")
        else:
            print("⚠ OpenMP 未找到，将禁用并行化")
    except:
        print("⚠ 无法检测 OpenMP 支持")
    
    # 链接时优化
    flags.append('-flto')
    
    return flags

class OptimizedBuildExt(build_ext):
    """自定义构建扩展，添加优化标志"""
    
    def build_extensions(self):
        # 获取优化标志
        opt_flags = get_optimization_flags()
        
        # 应用到所有扩展
        for ext in self.extensions:
            ext.extra_compile_args.extend(opt_flags)
            ext.extra_link_args.extend(opt_flags)
        
        # 调用父类方法
        super().build_extensions()

# 获取 NumPy 包含目录
numpy_include = numpy.get_include()

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
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

# 读取版本信息
def get_version():
    with open('fastcluster.py', 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip("'\"")
    return '1.3.0'

setup(
    name='xinyi_fastcluster',
    version=get_version(),
    author='Xinyi',
    author_email='xinyi@example.com',
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
