"""ЛР 9, вариант 4. Дерево, BFS/DFS и проверка двудольности."""
from collections import deque
import random, time, tracemalloc
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def make_tree(n, seed=42):
    rng = random.Random(seed)
    adj = [[] for _ in range(n)]
    for v in range(1, n):
        p = rng.randrange(v)
        adj[v].append(p); adj[p].append(v)
    return adj

def bfs(adj, start=0):
    dist = [-1]*len(adj); parent = [-1]*len(adj)
    q = deque([start]); dist[start] = 0; order = []
    while q:
        v = q.popleft(); order.append(v)
        for u in adj[v]:
            if dist[u] == -1:
                dist[u] = dist[v]+1; parent[u] = v; q.append(u)
    return order, dist, parent

def dfs(adj, start=0):
    seen = [False]*len(adj); stack = [start]; order = []
    while stack:
        v = stack.pop()
        if seen[v]: continue
        seen[v] = True; order.append(v)
        for u in reversed(adj[v]):
            if not seen[u]: stack.append(u)
    return order

def bipartite(adj):
    color = [-1]*len(adj)
    for s in range(len(adj)):
        if color[s] != -1: continue
        color[s] = 0; q = deque([s])
        while q:
            v = q.popleft()
            for u in adj[v]:
                if color[u] == -1:
                    color[u] = 1-color[v]; q.append(u)
                elif color[u] == color[v]:
                    return False, None
    return True, color

def matrix_from_adj(adj):
    n = len(adj); matrix = [[0]*n for _ in range(n)]
    for v, row in enumerate(adj):
        for u in row: matrix[v][u] = 1
    return matrix

def bfs_matrix(matrix, start=0):
    n = len(matrix); seen = [False]*n; q = deque([start]); seen[start] = True; count = 0
    while q:
        v = q.popleft(); count += 1
        for u, edge in enumerate(matrix[v]):
            if edge and not seen[u]: seen[u] = True; q.append(u)
    return count

if __name__ == "__main__":
    print("ЛР 9. Булова Екатерина, БИ 2-1, вариант 4")
    print("n     высота   листья   BFS, с      DFS, с")
    ns, bfs_times, dfs_times = [], [], []
    for n in (1000, 5000, 10000):
        adj = make_tree(n, seed=100+n)
        t0 = time.perf_counter(); order, dist, parent = bfs(adj); tb = time.perf_counter()-t0
        t0 = time.perf_counter(); dorder = dfs(adj); td = time.perf_counter()-t0
        leaves = sum(1 for row in adj if len(row) == 1) if n > 1 else 1
        height = max(dist)
        assert len(order) == n and len(dorder) == n
        print(f"{n:<6}{height:<10}{leaves:<9}{tb:<12.6f}{td:.6f}")
        ns.append(n); bfs_times.append(tb); dfs_times.append(td)

    # Доп. И4: двухцветная раскраска BFS.
    sample = make_tree(12, seed=4)
    ok, colors = bipartite(sample)
    assert ok and all(colors[v] != colors[u] for v,row in enumerate(sample) for u in row)
    triangle = [[1,2],[0,2],[0,1]]
    assert bipartite(triangle)[0] is False
    print("\\nИ4. Дерево двудольно:", ok)
    print("Группа 1:", [i for i,c in enumerate(colors) if c == 0])
    print("Группа 2:", [i for i,c in enumerate(colors) if c == 1])
    print("Контрольный треугольник двудольный:", bipartite(triangle)[0])

    # Сравнение матрицы и списков на небольшом дереве; для n=10000
    # матрица требует 100 млн ячеек, поэтому не создаётся.
    small = make_tree(300, seed=7)
    mat = matrix_from_adj(small)
    assert bfs_matrix(mat) == len(bfs(small)[0])
    print("Проверка матрицы и списков на n=300: результаты совпадают.")

    plt.figure()
    plt.plot(ns, bfs_times, marker="o", label="BFS")
    plt.plot(ns, dfs_times, marker="s", label="DFS")
    plt.xlabel("Число вершин n"); plt.ylabel("Время, с")
    plt.title("ЛР 9. Время обхода дерева"); plt.grid(True); plt.legend()
    plt.tight_layout(); plt.savefig("results/traversal_time.png", dpi=160)
