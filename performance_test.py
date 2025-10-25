#!/usr/bin/env python3
"""
Performance test script for optimized fastcluster
"""

import numpy as np
import time
import sys
import os

# Add current directory to path to import fastcluster
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import fastcluster
    print("✓ fastcluster imported successfully")
except ImportError as e:
    print(f"✗ Failed to import fastcluster: {e}")
    sys.exit(1)

def generate_test_data(n_points, n_dimensions, data_type='float64'):
    """Generate test data for clustering"""
    np.random.seed(42)  # For reproducible results
    if data_type == 'float64':
        return np.random.randn(n_points, n_dimensions).astype(np.float64)
    elif data_type == 'float32':
        return np.random.randn(n_points, n_dimensions).astype(np.float32)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")

def test_linkage_vector_performance():
    """Test linkage_vector performance with different data sizes"""
    print("\n=== Testing linkage_vector Performance ===")
    
    test_cases = [
        (100, 10, 'float64'),
        (500, 20, 'float64'),
        (1000, 50, 'float64'),
        (2000, 100, 'float64'),
    ]
    
    methods = ['single', 'ward', 'centroid']
    
    for n_points, n_dim, dtype in test_cases:
        print(f"\nTesting with {n_points} points, {n_dim} dimensions, {dtype}")
        X = generate_test_data(n_points, n_dim, dtype)
        
        for method in methods:
            try:
                start_time = time.time()
                Z = fastcluster.linkage_vector(X, method=method)
                end_time = time.time()
                
                duration = end_time - start_time
                print(f"  {method:>10}: {duration:.4f}s")
                
            except Exception as e:
                print(f"  {method:>10}: ERROR - {e}")

def test_linkage_performance():
    """Test linkage performance with distance matrices"""
    print("\n=== Testing linkage Performance ===")
    
    from scipy.spatial.distance import pdist
    
    test_cases = [
        (100, 10),
        (500, 20),
        (1000, 50),
    ]
    
    methods = ['single', 'complete', 'average', 'ward']
    
    for n_points, n_dim in test_cases:
        print(f"\nTesting with {n_points} points, {n_dim} dimensions")
        X = generate_test_data(n_points, n_dim)
        D = pdist(X)
        
        for method in methods:
            try:
                start_time = time.time()
                Z = fastcluster.linkage(D, method=method)
                end_time = time.time()
                
                duration = end_time - start_time
                print(f"  {method:>10}: {duration:.4f}s")
                
            except Exception as e:
                print(f"  {method:>10}: ERROR - {e}")

def test_simd_optimization():
    """Test SIMD optimization by comparing different vector sizes"""
    print("\n=== Testing SIMD Optimization ===")
    
    # Test with different vector sizes to see SIMD benefits
    n_points = 1000
    vector_sizes = [4, 8, 16, 32, 64, 128]
    
    print(f"Testing with {n_points} points, varying vector dimensions")
    
    for n_dim in vector_sizes:
        X = generate_test_data(n_points, n_dim)
        
        try:
            start_time = time.time()
            Z = fastcluster.linkage_vector(X, method='single')
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"  {n_dim:>3} dimensions: {duration:.4f}s")
            
        except Exception as e:
            print(f"  {n_dim:>3} dimensions: ERROR - {e}")

def test_parallel_scaling():
    """Test parallel scaling if OpenMP is available"""
    print("\n=== Testing Parallel Scaling ===")
    
    # Check if OpenMP is available
    omp_threads = os.environ.get('OMP_NUM_THREADS', '1')
    print(f"OMP_NUM_THREADS: {omp_threads}")
    
    n_points, n_dim = 2000, 100
    X = generate_test_data(n_points, n_dim)
    
    methods = ['single', 'ward']
    
    for method in methods:
        try:
            start_time = time.time()
            Z = fastcluster.linkage_vector(X, method=method)
            end_time = time.time()
            
            duration = end_time - start_time
            print(f"  {method:>10}: {duration:.4f}s (threads: {omp_threads})")
            
        except Exception as e:
            print(f"  {method:>10}: ERROR - {e}")

def main():
    """Run all performance tests"""
    print("FastCluster Performance Test")
    print("=" * 50)
    
    # Check if we're using the optimized version
    print(f"Python version: {sys.version}")
    print(f"NumPy version: {np.__version__}")
    
    # Run tests
    test_linkage_vector_performance()
    test_linkage_performance()
    test_simd_optimization()
    test_parallel_scaling()
    
    print("\n" + "=" * 50)
    print("Performance test completed!")

if __name__ == "__main__":
    main()
