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

# Generated range proof, elapsed time: 24488 [ms]
# encrypt 90s
# range 3171084
# Prove times: [185.3590745, 96.33660292857144, 49.24739589166666, 27.85581397777778, 18.242110341111108, 11.97984247638889, 9.179191519047619, 9.600347827777776, 13.704928312244897, 14.117198407738096, 23.948108084444442, 25.756783725000002, 34.98453304166667, 46.75756940833333, 496.56952175, 539.0759845, 641.9243975, 814.94483, 1212.111492, 1994.6507145]
# Verify times: [14.031960473015873, 26.47698427222222, 32.06951591666667, 38.909525091666666, 46.78778227857143, 76.24852664583334, 140.30290805, 270.978584, 530.359108, 1053.6836585, 2214.4763845, 4417.865706, 8837.4587455, 17921.112061, 35442.012703, 70805.020974, 141743.7794955, 283081.6781005, 566311.361211, 1125801.959599]