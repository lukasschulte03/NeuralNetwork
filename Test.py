import numpy as np

def min_angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    ans1 = np.rad2deg((ang1 - ang2) % (2 * np.pi))
    ans2 = np.rad2deg((ang2 - ang1) % (2 * np.pi))
    return min(ans1, ans2)

A = (5, 65)
B = (1, 0.01)

print(min_angle_between(A, B))



print(min_angle_between(B, A))

# 315.