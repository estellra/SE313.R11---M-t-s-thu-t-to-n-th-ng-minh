import os
import tempfile
import unittest
import random
import subprocess
import sys
from collections import deque

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..") + os.sep
CWD = tempfile.gettempdir()
N = 100


def run(script, text):
    p = subprocess.run(
        [sys.executable, "-I", ROOT + script],
        input=text, capture_output=True, text=True, timeout=10, cwd=CWD,
    )
    return p.returncode, p.stdout, p.stderr


def gen_graph(rng):
    n = rng.randint(2, 10)
    names = [chr(65 + i) for i in range(n)]
    h = {v: rng.randint(0, 12) for v in names}
    edges = []
    for _ in range(rng.randint(0, n * 2)):
        u, v = rng.choice(names), rng.choice(names)
        edges.append((u, v, rng.randint(1, 9)))
    start, goal = rng.choice(names), rng.choice(names)
    return names, h, edges, start, goal


def to_text(names, h, edges, start, goal):
    t = "".join(f"{v} {h[v]}\n" for v in names) + "\n"
    t += "".join(f"{u} {v} {c}\n" for u, v, c in edges) + "\n"
    return t + f"{start}\n{goal}\n"


def reachable(names, edges, start, goal):
    adj = {v: [] for v in names}
    for u, v, _ in edges:
        adj[u].append(v)
    seen, q = {start}, deque([start])
    while q:
        u = q.popleft()
        if u == goal:
            return True
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                q.append(v)
    return False


def valid_path(path, edges, start):
    es = {(u, v) for u, v, _ in edges}
    return path[0] == start and all((a, b) in es for a, b in zip(path, path[1:]))


def test_bfs():
    rng = random.Random(2)
    fails = []
    for i in range(N):
        names, h, edges, start, goal = gen_graph(rng)
        text = to_text(names, h, edges, start, goal)
        rc, out, err = run("BestFirstSearch.py", text)
        if rc != 0:
            fails.append((i, "crash", err.strip().splitlines()[-1], text))
            continue
        line = out.strip().splitlines()[-1]
        reach = reachable(names, edges, start, goal)
        if line == "None":
            if reach:
                fails.append((i, "returned None but goal is reachable", line, text))
            continue
        path = line.split(":", 1)[1].strip().split(" -> ")
        if not reach:
            fails.append((i, "path printed but goal unreachable", line, text))
        elif not valid_path(path, edges, start) or path[-1] != goal:
            fails.append((i, "invalid path", line, text))
    return fails


def test_steepest():
    rng = random.Random(3)
    fails = []
    for i in range(N):
        names, h, edges, start, goal = gen_graph(rng)
        text = to_text(names, h, edges, start, goal)
        rc, out, err = run("SteepestHillClimbing.py", text)
        if rc != 0:
            fails.append((i, "crash", err.strip().splitlines()[-1], text))
            continue
        lines = out.strip().splitlines()
        path = lines[-1].split(":", 1)[1].strip().split(" -> ")
        found = any("tim duoc (" in l for l in lines)
        adj = {v: [] for v in names}
        for u, v, _ in edges:
            adj[u].append(v)
        u, ref = start, [start]
        while u != goal:
            best = None
            for v in adj[u]:
                if best is None or h[v] < h[best]:
                    best = v
            if best is None or h[best] >= h[u]:
                break
            u = best
            ref.append(u)
        ref_found = u == goal
        if path != ref or found != ref_found:
            fails.append((i, "differs from reference", f"got {path} found={found}; expected {ref} found={ref_found}", text))
        elif not valid_path(path, edges, start):
            fails.append((i, "invalid path", str(path), text))
    return fails


def parse_sa(out):
    lines = out.strip().splitlines()
    k = int(lines[-2].split("Dinh")[-1])
    x = float(lines[-1].split(":")[1])
    return k, x


def test_sa():
    rng = random.Random(4)
    fails, notes = [], {"not_global_max": 0, "worse_than_plain_hc": 0, "total": 0}
    for i in range(N):
        n = rng.randint(1, 15)
        heights = [rng.randint(-50, 50) for _ in range(n)]
        start = rng.randint(1, n)
        text = f"{n}\n" + "".join(f"{x}\n" for x in heights) + f"{start}\n"
        rc, out, err = run("HillClimbing.py", text)
        if rc != 0:
            fails.append((i, "crash", err.strip().splitlines()[-1], text))
            continue
        try:
            k, x = parse_sa(out)
        except Exception as e:
            fails.append((i, "unparsable output", repr(out[-80:]), text))
            continue
        s = start - 1
        if not (1 <= k <= n) or x != heights[k - 1]:
            fails.append((i, "inconsistent state/score", f"k={k} x={x}", text))
            continue
        if x < heights[s]:
            fails.append((i, "worse than start", f"k={k} x={x} start_h={heights[s]}", text))
        notes["total"] += 1
        if x < max(heights):
            notes["not_global_max"] += 1
        p = s
        while True:
            nb = [q for q in (p - 1, p + 1) if 0 <= q < n]
            b = max(nb, key=lambda q: heights[q], default=None)
            if b is None or heights[b] <= heights[p]:
                break
            p = b
        if x < heights[p]:
            notes["worse_than_plain_hc"] += 1
    return fails, notes


def edge_cases():
    res = []

    def case(name, script, text):
        try:
            rc, out, err = run(script, text)
            res.append((name, script, rc, (err.strip().splitlines() or [out.strip().splitlines()[-1] if out.strip() else ""])[-1]))
        except subprocess.TimeoutExpired:
            res.append((name, script, "timeout", ""))

    base = "A 3\nB 2\nC 0\n\nA B 1\nB C 1\n\n"
    case("start == goal", "BestFirstSearch.py", base + "A\nA\n")
    case("start not in heuristics", "BestFirstSearch.py", base + "Z\nC\n")
    case("goal not in heuristics", "BestFirstSearch.py", base + "A\nZ\n")
    case("no edges", "BestFirstSearch.py", "A 1\nB 0\n\n\nA\nB\n")
    case("start == goal", "SteepestHillClimbing.py", base + "A\nA\n")
    case("start not in heuristics", "SteepestHillClimbing.py", base + "Z\nC\n")
    case("goal not in heuristics", "SteepestHillClimbing.py", base + "A\nZ\n")
    case("edge uses undeclared node, then valid retry", "SteepestHillClimbing.py", "A 3\nB 0\n\nA Z 1\nA B 1\n\nA\nB\n")
    case("edge uses undeclared node, then EOF", "SteepestHillClimbing.py", "A 3\nB 0\n\nA Z 1\n")
    case("heuristic line with 1 token", "SteepestHillClimbing.py", "A\n")
    case("n=0 then valid", "HillClimbing.py", "0\n2\n1\n5\n1\n")
    case("start out of range then valid", "HillClimbing.py", "2\n1\n5\n9\n1\n")
    case("n=1", "HillClimbing.py", "1\n7\n1\n")
    case("non numeric height", "HillClimbing.py", "2\nabc\n")
    case("non numeric n", "HillClimbing.py", "x\n")
    case("plateau (all equal)", "HillClimbing.py", "4\n3\n3\n3\n3\n2\n")
    return res


class HeuristicTests(unittest.TestCase):
    def test_best_first_search(self):
        self.assertEqual(test_bfs(), [])

    def test_steepest_hill_climbing(self):
        self.assertEqual(test_steepest(), [])

    def test_simulated_annealing(self):
        fails, notes = test_sa()
        self.assertEqual(fails, [])
        self.assertLessEqual(notes["not_global_max"], 5)
        self.assertEqual(notes["worse_than_plain_hc"], 0)


if __name__ == "__main__":
    unittest.main()
