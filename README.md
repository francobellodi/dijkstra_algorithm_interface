Dijkstra's Algorithm Visualizer
===============================

A Python-based graphical tool to visualize Dijkstra's shortest path algorithm step by step. Build your own graphs, run the algorithm interactively, and watch a car icon traverse the nodes and edges to find the shortest path.

Table of Contents
-----------------

-   [Features](#features)
-   [Installation](#installation)
-   [Usage](#usage)
-   [Dependencies](#dependencies)
-   [Contributing](#contributing)

Features
--------

-   **Interactive Graph Creation**: Add nodes and edges to build custom graphs.
-   **Edge Editing**: Easily edit edge weights by clicking near an edge.
-   **Step-by-Step Execution**: Run Dijkstra's algorithm one step at a time using the "Next Step" button.
-   **Visual Indicators**:
    -   Nodes and edges change colors to indicate their state during the algorithm.
    -   Distance labels under nodes show the current shortest distance from the start node.
-   **Animated Traversal**:
    -   A car icon animates along edges to neighbor nodes during processing.
    -   The car instantly moves to the next node when proceeding to the next step.
-   **Clear Response**: Reset node colors and distances to run the algorithm again without rebuilding the graph.

Installation
------------

1.  **Clone the Repository**:

    bash

    Copy code

    `git clone https://github.com/yourusername/dijkstras-algorithm-visualizer.git`

2.  **Navigate to the Project Directory**:

    bash

    Copy code

    `cd dijkstras-algorithm-visualizer`

3.  **Create a Virtual Environment (Optional but Recommended)**:

    bash

    Copy code

    `python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate``

4.  **Install Dependencies**:

    bash

    Copy code

    `pip install -r requirements.txt`

    *If `requirements.txt` is not provided, install the dependencies manually.*

Usage
-----

1.  **Run the Application**:

    bash

    Copy code

    `python main.py`

2.  **Build Your Graph**:

    -   **Add Nodes**: Click on "Add Node" and then click on the canvas to place nodes.
    -   **Add Edges**: Click on "Draw Edge", select the start node and then the end node. Enter the edge weight when prompted.
    -   **Edit Edges**: Click on "Edit Edge" and then click near an edge to change its weight.
3.  **Set Start and End Nodes**:

    -   Right-click on a node to set it as the start or end node.
4.  **Run Dijkstra's Algorithm**:

    -   Click on "Run Dijkstra's Algorithm".
    -   Use the "Next Step" button to execute the algorithm step by step.
5.  **Visual Feedback**:

    -   **Car Icon**: Watch the car animate along edges to neighboring nodes during processing.
    -   **Node and Edge Colors**:
        -   **Yellow Node**: Current node being processed.
        -   **Blue Edge**: Edge being considered.
        -   **Orange Node**: Neighboring node being updated.
        -   **Gray Node**: Node that has been visited.
6.  **Reset and Run Again**:

    -   Use the "Clear Response" button to reset node colors and distances without clearing the graph.

Dependencies
------------

-   Python 3.x

-   Tkinter (usually included with Python)

-   Pillow (for image handling)

    bash

    Copy code

    `pip install Pillow`

Contributing
------------

Contributions are welcome! Please follow these steps:

1.  **Fork the Repository**: Click on the "Fork" button at the top right of this page.

2.  **Clone Your Fork**:

    bash

    Copy code

    `git clone https://github.com/yourusername/dijkstras-algorithm-visualizer.git`

3.  **Create a New Branch**:

    bash

    Copy code

    `git checkout -b feature/your-feature-name`

4.  **Make Your Changes**: Implement your feature or bug fix.

5.  **Commit Your Changes**:

    bash

    Copy code

    `git commit -am 'Add new feature'`

6.  **Push to the Branch**:

    bash

    Copy code

    `git push origin feature/your-feature-name`

7.  **Open a Pull Request**: Navigate to the original repository and click on "New Pull Request".
