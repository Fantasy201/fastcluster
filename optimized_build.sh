#!/bin/bash

# Optimized build script for fastcluster with SIMD and parallelization support

# Detect CPU features and set appropriate compiler flags
CPU_FLAGS=""
if command -v lscpu &> /dev/null; then
    # Check for AVX2 support
    if lscpu | grep -q "avx2"; then
        CPU_FLAGS="$CPU_FLAGS -mavx2 -mfma"
    fi
    # Check for AVX support
    if lscpu | grep -q "avx"; then
        CPU_FLAGS="$CPU_FLAGS -mavx"
    fi
    # Check for SSE2 support (most modern CPUs have this)
    CPU_FLAGS="$CPU_FLAGS -msse2"
fi

# Set optimization flags
OPT_FLAGS="-O3 -DNDEBUG -funroll-loops -ffast-math -flto"

# Enable OpenMP if available
OMP_FLAGS=""
if pkg-config --exists omp; then
    OMP_FLAGS="-fopenmp"
    echo "OpenMP support detected and enabled"
else
    echo "OpenMP not found, building without parallelization"
fi

# Set architecture-specific flags
ARCH_FLAGS="-march=native -mtune=native"

# Combine all flags
ALL_FLAGS="$OPT_FLAGS $CPU_FLAGS $OMP_FLAGS $ARCH_FLAGS"

echo "Building fastcluster with optimization flags: $ALL_FLAGS"

# Build the extension
python setup.py build_ext --inplace \
    --define=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION \
    --compiler-flags="$ALL_FLAGS"

echo "Build completed successfully!"
echo "To use the optimized version, make sure to set:"
echo "export OMP_NUM_THREADS=<number_of_cores>"
echo "export OMP_PROC_BIND=true"
echo "export OMP_PLACES=cores"
