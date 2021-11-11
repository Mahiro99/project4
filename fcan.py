import math
import random
# variables
max_rd = 40
alpha = 6
#utility methods
def euclidian_distance(x1,x2):
    sum_ = 0
    for i in range(0, len(x1)):
        sum_ += math.pow(x1[i]-x2[i], 2)
    return math.sqrt(sum_)

def return_closest_cluster_index(clusters, pattern):
    min_ed = float("inf")
    min_index = 0
    for index, cluster in enumerate(clusters):
        ed = euclidian_distance(cluster["value"], pattern)
        if ed < min_ed:
            min_ed = ed
            min_index = index
    return min_index
# Read TDM
patterns = []
with open("tdm.csv", "r") as f:
    lines = f.readlines()
    for line in lines[1:]:
        patterns.append([int(x) for x in line.split(",")[1:]])

# TEST DATA FROM SLIDES
# max_rd = 3
# alpha = 1
# patterns = [
#     [5.9630, 0.7258],
#     [4.1168, 2.9694],
#     [1.8184, 6.0148],
#     [6.2139, 2.4288],
#     [6.1290, 1.3876],
#     [1.0562, 5.8288],
#     [4.3185, 2.3792],
#     [2.6108, 5.4870],
#     [1.5999, 4.1317],
#     [1.1046, 4.1969]
#     ]

# FCAN Algorithm
# Intialized with first datapoint
clusters = [{"value": patterns[0], "included_patterns":[0]}]
for index in range(1, len(patterns)):
    pattern = patterns[index]
    # Sort clusters by ED
    closest_cluster_index = return_closest_cluster_index(clusters, pattern)
    closest_cluster = clusters[closest_cluster_index]
    if euclidian_distance(closest_cluster["value"], pattern) > max_rd:
        clusters.append({"value": pattern, "m": 1, "included_patterns": [index]})
        continue

    new_value = []
    for i in range(0, len(closest_cluster["value"])):
        m = len(closest_cluster["included_patterns"])
        new_value.append( ((m * closest_cluster["value"][i]) + (alpha * pattern[i])) / (m +1))
    clusters[closest_cluster_index] = {"value":new_value, "included_patterns": clusters[closest_cluster_index]["included_patterns"] + [index]}

print(len(clusters), len(patterns))

for cluster in clusters:
    print(cluster["included_patterns"])