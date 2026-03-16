# SocialSim

CLI-based social network simulation in Python. Uses a B+ Tree for general user management, a directed graph for follow/unfollow connections, and the Merge Sort + Binary Search algorithms for post management. Persistence via CSV and local file system. Some features incomplete; post-related options are broken due to file handling issues.

Built for the Estructura de Datos y Algoritmos 2 course — UNAM Facultad de Ingeniería.

---

## Features

| Feature | Status |
|---------|--------|
| User registration and login |  Working |
| View and edit profile |  Working |
| Follow / unfollow users |  Working |
| View followers and following |  Working |
| Friend suggestions |  Working |
| Create and delete posts |  Broken (file handling issues) |
| View and search posts |  Working |
| Sort posts by date or title |  Broken (file handling issues) |

---

## Data Structures & Algorithms

- **B+ Tree** — general user management: registration, login, search, and deletion.
- **Directed graph** (adjacency list) — models follow/unfollow relationships and generates friend suggestions via friends-of-friends traversal.
- **Merge Sort** — sorts posts by date or title.
- **Binary Search** — searches posts by title or date after sorting.

---

## Requirements

Python 3. No external libraries required — only standard library modules are used (`csv`, `os`, `datetime`, `random`).

---

## Usage

```bash
python proyecto.py
```

On first run, the program expects a `BaseDeDatos.csv` file in the same directory. If it does not exist, create an empty one:

```bash
touch BaseDeDatos.csv  # macOS/Linux
type nul > BaseDeDatos.csv  # Windows
```

Each registered user gets a folder in the working directory where their data is stored.

---

## Known Issues

- Post creation, deletion, search, and sorting are not working as expected due to file handling issues with user directories.
- Some features remain incomplete.

---

## Notes

- This is a simulation — there is no server, no concurrency handling, and no real networking. All data is stored locally via CSV files and the file system.
- Developed as a third-semester project for the Estructura de Datos y Algoritmos 2 course.
