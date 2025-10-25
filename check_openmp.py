#!/usr/bin/env python3
"""
跨平台 OpenMP 检测脚本
支持 macOS (Apple Silicon/Intel), Linux, Windows
"""

import os
import platform
import subprocess
import sys

def check_homebrew_libomp():
    """检查 Homebrew libomp (macOS)"""
    system = platform.system().lower()
    if system != 'darwin':
        return False, None
    
    # Apple Silicon Homebrew
    apple_silicon_path = '/opt/homebrew/opt/libomp/include/omp.h'
    if os.path.exists(apple_silicon_path):
        return True, {
            'type': 'Homebrew libomp (Apple Silicon)',
            'include': '/opt/homebrew/opt/libomp/include',
            'lib': '/opt/homebrew/opt/libomp/lib'
        }
    
    # Intel Mac Homebrew
    intel_mac_path = '/usr/local/opt/libomp/include/omp.h'
    if os.path.exists(intel_mac_path):
        return True, {
            'type': 'Homebrew libomp (Intel Mac)',
            'include': '/usr/local/opt/libomp/include',
            'lib': '/usr/local/opt/libomp/lib'
        }
    
    return False, None

def check_conda_openmp():
    """检查 Conda OpenMP"""
    conda_prefix = os.environ.get('CONDA_PREFIX', '')
    if not conda_prefix:
        return False, None
    
    omp_header = os.path.join(conda_prefix, 'include', 'omp.h')
    if os.path.exists(omp_header):
        return True, {
            'type': 'Conda OpenMP',
            'include': os.path.join(conda_prefix, 'include'),
            'lib': os.path.join(conda_prefix, 'lib')
        }
    
    return False, None

def check_pkg_config():
    """检查 pkg-config OpenMP (Linux/Windows)"""
    try:
        result = subprocess.run(['pkg-config', '--exists', 'omp'], 
                              capture_output=True, check=False)
        if result.returncode == 0:
            # 获取编译和链接标志
            cflags = subprocess.run(['pkg-config', '--cflags', 'omp'], 
                                 capture_output=True, text=True, check=False)
            libs = subprocess.run(['pkg-config', '--libs', 'omp'], 
                                capture_output=True, text=True, check=False)
            
            return True, {
                'type': 'pkg-config OpenMP',
                'cflags': cflags.stdout.strip(),
                'libs': libs.stdout.strip()
            }
    except:
        pass
    
    return False, None

def check_system_gcc():
    """检查系统 GCC OpenMP (Linux)"""
    system = platform.system().lower()
    if system != 'linux':
        return False, None
    
    try:
        result = subprocess.run(['gcc', '-fopenmp', '--version'], 
                              capture_output=True, check=False)
        if result.returncode == 0:
            return True, {
                'type': '系统 GCC OpenMP',
                'cflags': '-fopenmp',
                'libs': '-fopenmp'
            }
    except:
        pass
    
    return False, None

def check_msvc_openmp():
    """检查 MSVC OpenMP (Windows)"""
    system = platform.system().lower()
    if system != 'windows':
        return False, None
    
    try:
        # 检查是否有 MSVC 编译器
        result = subprocess.run(['cl', '/?'], capture_output=True, check=False)
        if result.returncode == 0:
            return True, {
                'type': 'MSVC OpenMP',
                'cflags': '/openmp',
                'libs': ''
            }
    except:
        pass
    
    return False, None

def main():
    """主函数：检测所有可能的 OpenMP 实现"""
    print("OpenMP 检测工具")
    print("=" * 50)
    print(f"平台: {platform.system()} {platform.machine()}")
    print(f"Python: {sys.version}")
    print()
    
    # 检测顺序：Homebrew > Conda > pkg-config > 系统GCC > MSVC
    detectors = [
        ("Homebrew libomp", check_homebrew_libomp),
        ("Conda OpenMP", check_conda_openmp),
        ("pkg-config", check_pkg_config),
        ("系统 GCC", check_system_gcc),
        ("MSVC", check_msvc_openmp),
    ]
    
    found_any = False
    
    for name, detector in detectors:
        try:
            found, info = detector()
            if found:
                print(f"✓ {name}: {info['type']}")
                if 'include' in info:
                    print(f"  包含目录: {info['include']}")
                if 'lib' in info:
                    print(f"  库目录: {info['lib']}")
                if 'cflags' in info:
                    print(f"  编译标志: {info['cflags']}")
                if 'libs' in info:
                    print(f"  链接标志: {info['libs']}")
                print()
                found_any = True
            else:
                print(f"✗ {name}: 未找到")
        except Exception as e:
            print(f"✗ {name}: 检测失败 ({e})")
    
    if not found_any:
        print("⚠ 未找到任何 OpenMP 实现")
        print()
        print("安装建议:")
        print("- macOS: brew install libomp")
        print("- Linux: sudo apt-get install libomp-dev (Ubuntu/Debian)")
        print("- Windows: 安装 Visual Studio 或使用 conda install openmp")
        return False
    else:
        print("✓ 找到可用的 OpenMP 实现")
        return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
