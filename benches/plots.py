import json
import os
import re
import matplotlib.pyplot as plt

dir = "../target/criterion/kzg-elgamal/"
folders = [name for name in os.listdir(dir) if os.path.isdir(os.path.join(dir, name))]

prove_pattern = re.compile(r"^proof-gen-(\d+)")
verify_pattern = re.compile(r"^proof-vfy-(\d+)")

def append_bench_data(folder_map):
    folder_name = folder_map['name']
    estimates_path = os.path.join(dir, folder_name, "base", "estimates.json")
    if os.path.exists(estimates_path):
        with open(estimates_path, "r") as f:
            try:
                estimates = json.load(f)
                # Only keep the 'point_estimate' in the 'median'
                folder_map['bench'] = estimates.get('median', {}).get('point_estimate') / 1000000
            except Exception as e:
                print(f"Failed to load {estimates_path}: {e}")

prove_time = []
verify_time = []

for folder in folders:
    m = prove_pattern.match(folder)
    if m:
        l = m.groups()[0]
        entry = {'name': folder, 'l': l}
        append_bench_data(entry)
        prove_time.append(entry)
        continue
    m = verify_pattern.match(folder)
    if m:
        l = m.groups()[0]
        entry = {'name': folder, 'l': l}
        append_bench_data(entry)
        verify_time.append(entry)
        continue

prove_time = sorted(prove_time, key=lambda x: int(x['l']))
verify_time = sorted(verify_time, key=lambda x: int(x['l']))
pt = list(map(lambda x: x['bench'], prove_time))
vt = list(map(lambda x: x['bench'], verify_time))
print("Prove times: {}".format(pt))
print("Verify times: {}".format(vt))

# Generated range proof, elapsed time: 23423 [ms]
# Prove times: [160.17436817777778, 82.7790933888889, 44.76020196666667, 26.010704875, 16.298256791666667, 11.091688894179894, 8.891683441919193, 10.043410994949495, 13.561843208333334, 12.519060857142858, 23.241042314999998, 20.561196535714284, 24.976779883333332]
# Verify times: [12.021436956250001, 16.864447766666665, 18.835436711111115, 25.352385533333333, 25.219340613095238, 25.779682208333337, 30.25220851388889, 23.362898041666664, 29.9995043, 33.10691138988095, 55.70703651666667, 104.84860387777779, 200.5871435]
