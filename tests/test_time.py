import pandas as pd
import time
import os
import sys

# 确保在导入其他包之前先设置路径并导入我们的优化版本
sys.path.insert(0, '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package')
import fastcluster as xinyi_fastcluster

# 验证我们使用的是优化版本
print(f"Using optimized fastcluster version: {xinyi_fastcluster.__version__}")
print(f"Fastcluster module location: {xinyi_fastcluster.__file__}")

# 检查模块路径是否指向我们的优化版本
expected_path = '/Users/xinyi/Projects/fastcluster/xinyi_fastcluster_package'
if expected_path in xinyi_fastcluster.__file__:
    print("✅ 确认：正在使用你的优化版本 fastcluster")
else:
    print("❌ 警告：可能在使用原生 fastcluster，请检查路径设置")

# 检查是否有我们的优化标识
if hasattr(xinyi_fastcluster, '__doc__') and 'Optimized fast hierarchical clustering' in xinyi_fastcluster.__doc__:
    print("✅ 确认：检测到优化版本的文档标识")
else:
    print("❌ 警告：未检测到优化版本的文档标识")

# 检查可用的函数
print(f"Available functions: {[attr for attr in dir(xinyi_fastcluster) if not attr.startswith('_')]}")

# 检查底层 C++ 扩展模块
try:
    import _xinyi_fastcluster
    print(f"✅ 底层 C++ 扩展模块: {_xinyi_fastcluster.__file__}")
    if 'xinyi_fastcluster_package' in _xinyi_fastcluster.__file__:
        print("✅ 确认：底层扩展模块也是优化版本")
    else:
        print("❌ 警告：底层扩展模块可能不是优化版本")
except ImportError as e:
    print(f"❌ 无法导入底层扩展模块: {e}")

print("=" * 60)

from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import dendrogram
from scipy.spatial.distance import squareform

from sequenzo import Cluster
from sequenzo.define_sequence_data import SequenceData
from sequenzo.dissimilarity_measures.get_distance_matrix import get_distance_matrix

U_files = [
    # 'synthetic_detailed_U5_N500.csv',
    # 'synthetic_detailed_U5_N1000.csv',
    # 'synthetic_detailed_U5_N1500.csv',
    # 'synthetic_detailed_U5_N2000.csv',
    # 'synthetic_detailed_U5_N2500.csv',
    # 'synthetic_detailed_U5_N3000.csv',
    # 'synthetic_detailed_U5_N3500.csv',
    # 'synthetic_detailed_U5_N4000.csv',
    # 'synthetic_detailed_U5_N4500.csv',
    # 'synthetic_detailed_U5_N5000.csv',
    # 'synthetic_detailed_U5_N10000.csv',
    # 'synthetic_detailed_U5_N15000.csv',
    # 'synthetic_detailed_U5_N20000.csv',
    # 'synthetic_detailed_U5_N25000.csv',
    # 'synthetic_detailed_U5_N30000.csv',
    # 'synthetic_detailed_U5_N35000.csv',
    # 'synthetic_detailed_U5_N40000.csv',
    # 'synthetic_detailed_U5_N45000.csv',
    'synthetic_detailed_U5_N50000.csv',

    # 'synthetic_detailed_U25_N500.csv',
    # 'synthetic_detailed_U25_N1000.csv',
    # 'synthetic_detailed_U25_N1500.csv',
    # 'synthetic_detailed_U25_N2000.csv',
    # 'synthetic_detailed_U25_N2500.csv',
    # 'synthetic_detailed_U25_N3000.csv',
    # 'synthetic_detailed_U25_N3500.csv',
    # 'synthetic_detailed_U25_N4000.csv',
    # 'synthetic_detailed_U25_N4500.csv',
    # 'synthetic_detailed_U25_N5000.csv',
    # 'synthetic_detailed_U25_N10000.csv',
    # 'synthetic_detailed_U25_N15000.csv',
    # 'synthetic_detailed_U25_N20000.csv',
    # 'synthetic_detailed_U25_N25000.csv',
    # 'synthetic_detailed_U25_N30000.csv',
    # 'synthetic_detailed_U25_N35000.csv',
    # 'synthetic_detailed_U25_N40000.csv',
    # 'synthetic_detailed_U25_N45000.csv',
    # 'synthetic_detailed_U25_N50000.csv',

    # 'synthetic_detailed_U50_N500.csv',
    # 'synthetic_detailed_U50_N1000.csv',
    # 'synthetic_detailed_U50_N1500.csv',
    # 'synthetic_detailed_U50_N2000.csv',
    # 'synthetic_detailed_U50_N2500.csv',
    # 'synthetic_detailed_U50_N3000.csv',
    # 'synthetic_detailed_U50_N3500.csv',
    # 'synthetic_detailed_U50_N4000.csv',
    # 'synthetic_detailed_U50_N4500.csv',
    # 'synthetic_detailed_U50_N5000.csv',
    # 'synthetic_detailed_U50_N10000.csv',
    # 'synthetic_detailed_U50_N15000.csv',
    # 'synthetic_detailed_U50_N20000.csv',
    # 'synthetic_detailed_U50_N25000.csv',
    # 'synthetic_detailed_U50_N30000.csv',
    # 'synthetic_detailed_U50_N35000.csv',
    # 'synthetic_detailed_U50_N40000.csv',
    # 'synthetic_detailed_U50_N45000.csv',
    # 'synthetic_detailed_U50_N50000.csv',

    # 'synthetic_detailed_U85_N500.csv',
    # 'synthetic_detailed_U85_N1000.csv',
    # 'synthetic_detailed_U85_N1500.csv',
    # 'synthetic_detailed_U85_N2000.csv',
    # 'synthetic_detailed_U85_N2500.csv',
    # 'synthetic_detailed_U85_N3000.csv',
    # 'synthetic_detailed_U85_N3500.csv',
    # 'synthetic_detailed_U85_N4000.csv',
    # 'synthetic_detailed_U85_N4500.csv',
    # 'synthetic_detailed_U85_N5000.csv',
    # 'synthetic_detailed_U85_N10000.csv',
    # 'synthetic_detailed_U85_N15000.csv',
    # 'synthetic_detailed_U85_N20000.csv',
    # 'synthetic_detailed_U85_N25000.csv',
    # 'synthetic_detailed_U85_N30000.csv',
    # 'synthetic_detailed_U85_N35000.csv',
    # 'synthetic_detailed_U85_N40000.csv',
    # 'synthetic_detailed_U85_N45000.csv',
    # 'synthetic_detailed_U85_N50000.csv',
]

# data_dir = '/home/xinyi_test/data/detailed_data'
# data_dir = 'D:/college/research/QiQi/sequenzo/files/detialed_transposed.csv'
# data_dir = 'D:\\college\\research\\QiQi\\sequenzo\\data_and_output\\sampled_data_sets\\broad_data'
# data_dir = 'D:\\college\\research\\QiQi\\sequenzo\\data_and_output\\sampled_data_sets\\detailed_data'
data_dir = '/Users/xinyi/Projects/sequenzo/sequenzo/data_and_output/orignal data/not_real_detailed_data'

# 存储运行时间和文件名的列表
runtimes = []
filenames = []

# 循环读取每个 CSV 文件并计算运行时间
for filename in U_files:
    file_path = os.path.join(data_dir, filename)
    df = pd.read_csv(file_path)
    # df = pd.read_csv(data_dir)

    # _time = list(df.columns)[4:]
    # states = ['data', 'data & intensive math', 'hardware', 'research', 'software', 'software & hardware', 'support & test']
    # df = df[['worker_id', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10']]
    #
    _time = list(df.columns)[2:]
    states = ["Data", "Data science", "Hardware", "Research", "Software", "Support & test", "Systems & infrastructure"]
    df = df[['id', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']]

    # _time = list(df.columns)[4:]
    # states = ['Non-computing', 'Non-technical computing', 'Technical computing']
    # df = df[['worker_id', 'C1', 'C2', 'C3', 'C4', 'C5']]
    # df = df.drop_duplicates(subset=['worker_id'])

    # _time = list(df.columns)[1:]
    # states = ['Very Low', 'Low', 'Middle', 'High', 'Very High']

    # data = SequenceData(df, time=_time, time_type="age", id_col="worker_id", states=states)
    data = SequenceData(df, time=_time, id_col="id", states=states)
    # data = SequenceData(df, time=_time, time_type="year", id_col="country", states=states)

    diss = get_distance_matrix(seqdata=data, method="OM", sm="CONSTANT", indel=1).to_numpy()

    # Cluster(diss, data.ids, clustering_method='ward_d2')
    # diss = pdist(diss, metric='euclidean')
    # diss = squareform(diss, checks=False)

    start = time.time()
    linkage_matrix = xinyi_fastcluster.linkage_vector(diss, method='ward')
    end = time.time()

    runtime = end - start
    runtimes.append(runtime)
    filenames.append(filename)

    print(f"File: {filename}, Runtime: {runtime:.4f} seconds")

print(runtimes)