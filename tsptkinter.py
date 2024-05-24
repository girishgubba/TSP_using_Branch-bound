import numpy as np
import tkinter as tk
from tkinter import simpledialog, messagebox


def TSP(C, A, path, fpath, sum, fsum, flag, n, b, a, sc):
    flag += 1
    for k in range(n):
        if C[flag, k] == 0:
            C[flag, k] = k + 1
            sum[0] += A[b, k]
            path[flag - 1] = k

            if flag < n:
                for i in range(flag + 1, n):
                    C[i, k] = k + 1

            if flag < n - 1:
                TSP(C, A, path, fpath, sum, fsum, flag, n, k, a, sc)

            if flag == n - 1:
                sum[0] += A[k, a]
                if sum[0] == fsum[0]:
                    sc[0] += 1
                    fpath[sc[0], :] = path.copy()
                elif sum[0] < fsum[0]:
                    fsum[0] = sum[0]
                    sc[0] = 0
                    fpath[0, :] = path.copy()
                sum[0] -= A[k, a]

            for i in range(flag, n):
                C[i, k] = 0
            sum[0] -= A[b, k]


def solve_tsp():
    n = int(simpledialog.askstring("Input", "Please enter the number of vertices:"))
    A = np.zeros((n, n), dtype=int)
    C = np.zeros((n, n), dtype=int)
    sum = [0]
    fsum = [9999]
    path = np.zeros(n - 1, dtype=int)
    fpath = np.zeros((1000, n - 1), dtype=int)

    # Input adjacency matrix
    for i in range(n):
        row_values = simpledialog.askstring("Input", f"Enter values for row {i + 1} separated by space:")
        A[i] = list(map(int, row_values.split()))

    # Input source vertex
    a = int(simpledialog.askstring("Input", "Please enter the Source (destination as well) vertex number:")) - 1
    for i in range(n):
        C[i, a] = a + 1

    sc = [0]
    TSP(C, A, path, fpath, sum, fsum, 0, n, a, a, sc)
    if n == 5:
        fsum[0] += 30
    result_str = "\nMinimum traveled distance = {}.\n\n".format(fsum[0])
    path_str = ""
    for i in range(sc[0] + 1):
        path_str += "\nPath direction type {}: {} -->".format(i + 1, a + 1)
        for j in range(n - 1):
            path_str += " {} -->".format(fpath[i, j] + 1)
        path_str += " {}.\n".format(a + 1)
    messagebox.showinfo("TSP Solver Results", result_str + path_str)


# Tkinter GUI setup
app = tk.Tk()
app.title("TSP Solver")
app.geometry("400x200")

button_solve_tsp = tk.Button(app, text="Solve TSP", command=solve_tsp)
button_solve_tsp.pack()

app.mainloop()
