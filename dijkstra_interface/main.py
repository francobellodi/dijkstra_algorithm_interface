# main.py

import tkinter as tk
from gui import DijkstraVisualizer

def main():
    root = tk.Tk()
    app = DijkstraVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()

