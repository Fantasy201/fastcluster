#!/usr/bin/env python3
"""
修复 OpenMP 段溢出问题的脚本
"""

import os
import sys
import subprocess

def fix_openmp_segfault():
    """修复 OpenMP 段溢出问题"""
    print("🔧 修复 OpenMP 段溢出问题...")
    
    # 设置环境变量以避免 OpenMP 冲突
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['OPENMP_DISABLED'] = '1'
    
    print("✅ 已设置 OMP_NUM_THREADS=1 和 OPENMP_DISABLED=1")
    
    # 测试导入
    try:
        sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
        import fastcluster
        print(f"✅ 成功导入 fastcluster: {fastcluster.__version__}")
        print(f"📁 模块位置: {fastcluster.__file__}")
        
        # 测试基本功能
        import numpy as np
        from scipy.spatial.distance import pdist
        
        # 创建测试数据
        test_data = np.random.rand(10, 3)
        distances = pdist(test_data)
        
        # 测试聚类
        linkage_matrix = fastcluster.linkage_vector(distances, method='ward')
        print("✅ 基本聚类功能测试通过")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def create_wrapper_script():
    """创建包装脚本以避免 OpenMP 冲突"""
    wrapper_content = '''#!/bin/bash
# 修复 OpenMP 段溢出的包装脚本

# 设置环境变量
export OMP_NUM_THREADS=1
export OPENMP_DISABLED=1

# 运行原始命令
exec "$@"
'''
    
    with open('/Users/xinyi/Projects/fastcluster/run_without_openmp.sh', 'w') as f:
        f.write(wrapper_content)
    
    os.chmod('/Users/xinyi/Projects/fastcluster/run_without_openmp.sh', 0o755)
    print("✅ 创建了包装脚本: run_without_openmp.sh")

def main():
    print("=" * 60)
    print("🔧 OpenMP 段溢出修复工具")
    print("=" * 60)
    
    # 修复问题
    success = fix_openmp_segfault()
    
    if success:
        print("\n🎉 修复成功！")
        print("\n📋 使用方法:")
        print("1. 设置环境变量:")
        print("   export OMP_NUM_THREADS=1")
        print("   export OPENMP_DISABLED=1")
        print("\n2. 或者使用包装脚本:")
        print("   ./run_without_openmp.sh python tests/test_time.py")
        
        # 创建包装脚本
        create_wrapper_script()
        
        print("\n💡 说明:")
        print("- 段溢出是由于 OpenMP 库不匹配造成的")
        print("- 当前环境使用 LLVM OpenMP，但模块用 GCC OpenMP 编译")
        print("- 设置 OMP_NUM_THREADS=1 可以避免多线程冲突")
        print("- 在 conda Python 10 环境中可以正常运行是因为库兼容")
        
    else:
        print("\n❌ 修复失败，请检查环境配置")

if __name__ == '__main__':
    main()
