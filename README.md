# 🛸 Fly-in: Multi-Agent Drone Simulation & Pathfinding Challenge

**Fly-in** is a Python-based **Multi-Agent Pathfinding (MAPF)** and traffic optimization simulation project designed for autonomous drone fleets.

The primary objective is to coordinate and navigate an entire fleet of drones (`nb_drones`) from a designated departure hub (`start_hub`) to a target destination hub (`end_hub`) across a topological network of interconnected waypoints (hubs), minimizing the total number of simulation turns while strictly adhering to physical capacity constraints, movement latency, and zone rules.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features & Algorithmic Challenges](#-key-features--algorithmic-challenges)
- [Project Structure](#-project-structure)
- [Map File Format](#-map-file-format)
- [Map Categories & Benchmarks](#-map-categories--benchmarks)
- [Installation & Getting Started](#-installation--getting-started)
- [Usage](#-usage)
- [Data Models & Architecture](#-data-models--architecture)
- [Project Roadmap](#-project-roadmap)

---

## 🎯 Overview

In **Fly-in**, the flight environment is modeled as a graph where:
- **Hubs** represent air stations, waypoints, or landing pads with spatial coordinates `(x, y)`.
- **Connections** represent flight corridors between pairs of hubs.
- **Drones** operate in discrete time turns. During each turn, a drone can either wait at its current hub or traverse an adjacent valid corridor, subject to capacity availability and zone rules.

---

## ⚡ Key Features & Algorithmic Challenges

The simulation environment tests pathfinding algorithms against complex operational constraints:

1. **Capacity Constraints**:
   - **Hub Capacity (`max_drones`)**: Maximum number of drones that can simultaneously dock or occupy a hub to prevent station congestion.
   - **Link Capacity (`max_link_capacity`)**: Maximum number of drones that can travel through a flight corridor concurrently during the same turn.
2. **Dead-End Traps**:
   - Sub-paths that lead to dead ends, testing whether algorithms can detect traps, avoid bottlenecks, or backtrack efficiently.
3. **Circular Loops**:
   - Cycles in the graph topology that can cause naive or greedy search algorithms to get trapped in infinite loops.
4. **Zone Type Optimization**:
   - `normal`: Standard 1-turn traversal.
   - `restricted`: Slower flight corridor (requires 2 turns; higher latency but valuable for bypassing congestion).
   - `priority`: High-throughput, preferred corridor (1 turn).
   - `blocked`: Completely inaccessible zones.
5. **Spatio-Temporal Conflict Resolution**:
   - Scheduling conflict-free 4D trajectories (space + time) for multiple drones competing for identical resources at the same time step.

---

## 📁 Project Structure

```text
Fly-in/
├── main.py              # Application entry point to load maps and run simulations
├── requirements.txt     # Python dependencies and virtual environment instructions
├── README.md            # Main project documentation
├── src/                 # Core source code
│   ├── __init__.py
│   ├── models.py        # Pydantic data models (Hub, Connection, MapGraph, Drone...)
│   └── parsing.py       # Map file parser and schema validator (.txt)
└── maps/                # Map test suites organized by difficulty
    ├── README.md        # Detailed documentation of challenge scenarios and records
    ├── easy/            # Linear paths and simple forks for basic validation
    ├── medium/          # Traps, cycles, and priority path optimizations
    ├── hard/            # High-density bottlenecks and complex mazes
    └── challenger/      # Extreme stress-testing maps for algorithmic research
```

---

## 📝 Map File Format

Maps are defined in plain text files (`.txt`) using a clean, declarative syntax:

```ini
# Global configuration
nb_drones: 5

# Hub definitions (type: name x y [optional_attributes])
start_hub: start 0 0 [color=green]
hub: junction 1 0 [color=yellow max_drones=2]
hub: tunnel 2 0 [zone=restricted color=red max_drones=2]
hub: bypass 2 1 [zone=priority color=cyan max_drones=3]
end_hub: goal 4 0 [color=green]

# Connection definitions (connection: origin-destination [optional_attributes])
connection: start-junction [max_link_capacity=2]
connection: junction-tunnel
connection: junction-bypass
connection: tunnel-goal
connection: bypass-goal
```

### Supported Optional Attributes:
- **On Hubs**:
  - `color`: Visualization color identifier (`green`, `blue`, `yellow`, `red`, `cyan`, `orange`).
  - `max_drones`: Positive integer specifying the maximum simultaneous drone capacity at that hub.
  - `zone`: Zone behavior type (`normal`, `restricted`, `priority`, `blocked`).
- **On Connections**:
  - `max_link_capacity`: Positive integer specifying the maximum number of drones permitted on that edge concurrently.

---

## 🗺️ Map Categories & Benchmarks

| Difficulty | Description | Typical Drone Count | Target Turns | Available Maps |
| :--- | :--- | :---: | :---: | :--- |
| 🟢 **Easy** | Linear progression and basic forks for verifying fundamental movement logic. | 2 - 4 | `< 10` | `01_linear_path.txt`<br>`02_simple_fork.txt`<br>`03_basic_capacity.txt` |
| 🟡 **Medium** | Dead-end traps, circular loops, and priority zone path selection. | 5 - 6 | `10 - 30` | `01_dead_end_trap.txt`<br>`02_circular_loop.txt`<br>`03_priority_puzzle.txt` |
| 🔴 **Hard** | Complex mazes, extreme bottleneck constraints, and large-scale queue management. | 8 - 15 | `30+` | `01_maze_nightmare.txt`<br>`02_capacity_hell.txt`<br>`03_ultimate_challenge.txt` |
| ⚫ **Challenger** | *"The Impossible Dream"*: Quasi-unsolvable stress-test designed for algorithmic boundaries. | 25 | **Record: 45** | `01_the_impossible_dream.txt` |

*(Refer to [`maps/README.md`](maps/README.md) for full scenario descriptions).*

---

## 🚀 Installation & Getting Started

### Prerequisites
- **Python 3.10+**
- `pip` package manager

### 1. Clone the repository
```bash
git clone https://github.com/CarlosJX7/Fly-in.git
cd Fly-in
```

### 2. Create and activate a virtual environment
On Linux / macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies
> 💡 **Tip**: Be sure to supply the `-r` flag when installing:

```bash
pip install -r requirements.txt
```

---

## 💻 Usage

To run the parser and inspect the parsed map graph:

```bash
python main.py
```

By default, [main.py](main.py) parses a sample map (e.g. `maps/easy/01_linear_path.txt`), builds the validated Pydantic graph structure, and prints its contents to standard output.

---

## 🏗️ Data Models & Architecture

The project leverages **Pydantic v2** for strict typing, schema validation, and runtime safety:

- **`Hub`** ([src/models.py](src/models.py)): Represents a graph node with `name`, `x_axis`, `y_axis`, `color`, `max_drones`, and `zone_type`.
- **`Connection`** ([src/models.py](src/models.py)): Models an edge connecting an `origin_hub` and `destiny_hub`.
- **`MapGraph`** ([src/models.py](src/models.py)): Top-level graph model containing `nb_drones`, `starting_hub`, `hubs` dictionary, `goal_hub`, and a list of `connection`.
- **`Drone`** ([src/models.py](src/models.py)): Drone state entity containing `id`, `start_hub`, and simulation `state` (`WAITING`, `FLYING`, `IN_TRANSIT`, `FINISHED`).
- **`MapParser`** ([src/parsing.py](src/parsing.py)): Responsible for reading map files, sanitizing inputs, extracting optional bracketed parameters, and constructing `MapGraph` instances.

---

## 🛠️ Project Roadmap

- [x] Challenge maps definition and difficulty hierarchy (`maps/`).
- [x] Data models and graph representation with Pydantic validation (`src/models.py`).
- [x] Map parsing and input token extraction (`src/parsing.py`).
- [ ] Complete parsing support for link capacity parameters (`max_link_capacity`).
- [ ] Turn-based simulation and step execution engine.
- [ ] Multi-agent pathfinding solver (e.g., Space-Time A*, Conflict-Based Search - CBS, or Network Flow).
- [ ] Visualizer or export tool to replay drone mission trajectories.
