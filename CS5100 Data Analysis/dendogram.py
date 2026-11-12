import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram

# Each row is one observation.
X = np.array([
    [6,  5,  4],   # x1
    [0,  0,  0],   # x2
    [1,  1, -2],   # x3
    [7,  3, -1],   # x4
    [2, -1, -1],   # x5
    [4,  4,  4]    # x6
], dtype=float)

labels = ["x1", "x2", "x3", "x4", "x5", "x6"]
n = len(X)

# 1. Perform complete-linkage clustering.
# Use the original coordinates, not the rounded distance table.
Z = linkage(X, method="complete", metric="euclidean")

# Track which observations belong to each cluster.
# Python index 0 means x1, index 1 means x2, etc.
members = {i: [i] for i in range(n)}

def cluster_name(indices):
    return "{" + ", ".join(labels[i] for i in sorted(indices)) + "}"

# 2. Print the merge sequence.
print("MERGE SEQUENCE")

for step, row in enumerate(Z):
    left_id, right_id = int(row[0]), int(row[1])
    height = row[2]

    left_members = members[left_id]
    right_members = members[right_id]

    print(
        f"Step {step + 1}: "
        f"{cluster_name(left_members)} + "
        f"{cluster_name(right_members)} "
        f"at height {height:.3f}"
    )

    # SciPy gives the new cluster ID n + step.
    members[n + step] = left_members + right_members

# 3. Read the height of the final merge.
root_height = Z[-1, 2]

# 4. Identify the root's two child clusters.
left_child_id = int(Z[-1, 0])
right_child_id = int(Z[-1, 1])

left_child = members[left_child_id]
right_child = members[right_child_id]

# Select the child cluster containing x1 (index 0).
target_cluster = left_child if 0 in left_child else right_child

# 5. Average the coordinates of that cluster.
centroid = X[target_cluster].mean(axis=0)
a, b, c = centroid

print("\nREQUESTED RESULTS")
print(f"Root height: {root_height:.3f}")
print(f"Root's child containing x1: {cluster_name(target_cluster)}")
print(f"a = {a:.3f}")
print(f"b = {b:.3f}")
print(f"c = {c:.3f}")

# 6. Draw the dendrogram.
fig, ax = plt.subplots(figsize=(9, 6))

dendrogram(
    Z,
    labels=labels,
    leaf_font_size=12,
    ax=ax
)

# Label every merge with its height.
for line in ax.collections:
    for segment in line.get_segments():
        if len(segment) == 4:
            x_mid = (segment[1, 0] + segment[2, 0]) / 2
            height = segment[1, 1]
            ax.annotate(
                f"{height:.3f}",
                (x_mid, height),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center",
                fontsize=9
            )

ax.set_title("Complete-linkage dendrogram")
ax.set_xlabel("Observation")
ax.set_ylabel("Euclidean merge distance")
ax.set_ylim(0, root_height * 1.15)

plt.tight_layout()
plt.show()