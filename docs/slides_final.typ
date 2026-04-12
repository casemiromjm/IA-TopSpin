#import "@preview/diatypst:0.9.1": *

#set text(ligatures: false)
#show figure.caption: set text(size: 0.75em)

#show: slides.with(
  title: "Project 1 Final Delivery: Top Spin",
  subtitle: "Artificial Intelligence 2025/26 @ FEUP",
  authors: ("Casemiro Melo Jorge de Medeiros", "Mariana Almeida Cabral", "Pedro Andrade Castro"),
  ratio: 16 / 9,
  theme: "full",
  bg-color: rgb("#FFF6F6"),
  title-color: rgb("#2C687B"),
  count: "number",
  toc: false,
)

// Custom TOC: numbers slides 1, 2, 3 … instead of 0.a, 0.b …
#[
  #set heading(numbering: none)
  #show outline.entry: it => {
    let loc = it.element.location()
    let pg = counter(page).at(loc).first()
    let num = counter(heading).at(loc).at(1)
    link(loc)[#num. #h(4pt) #it.element.body #box(width: 1fr, repeat[.]) #pg]
    linebreak()
  }
  #outline(title: "Contents", target: heading.where(level: 2), indent: 0pt)
]

== Problem Specification

Our project is based in the Top Spin game. This game is similar to Rubik's Cube, but only in 2D.

#align(center)[
  #figure(
    image("./assets/topspin.jpg", height: 35%),
    caption: [Top Spin Board: Rotating the center "spin" disk swaps the inner pieces.],
  )
]

The game consists of 20 rounded pieces, numbered from 1 to 20, placed in one long looped track. It also has a turntable in the loop, which allows the player to rotate any 4 adjacent pieces so that they will be in reverse order.

== Problem Formulation

- *State*: Represented using a `TreeNode` class containing:
  - `state`: current board configuration (a tuple of 20 integers)
  - `parent`: reference to the parent node
  - `children`: list of child nodes
- *Initial State*: `(1, 2, 3, ..., 20)` - a tuple representing the state of the pieces at the beginning of the game
- *Objective Test*: Check if `state == (1, 2, 3, ..., 20)` (sorted order)
- *Operators*:
  - `move_left(state)`: Rotates the ring one position to the left
  - `move_right(state)`: Rotates the ring one position to the right
  - `spin(state)`: Reverses the first 4 elements (spin window)
  - All operators have cost = 1

== Heuristics / Evaluation Functions

- *Adjacency (Number of Breaks)*
  - Instead of looking for the piece itself, check the neighbouring piece to see if it is in the correct order. Piece _i_ must be followed by piece _i+1_, but piece 20 must be followed by piece 1. Moving a piece does not fix any breaks; only spinning fixes them (at most two, on the edges).
  #text(size: 0.82em)[$ h = ceil("Number of Breaks" / 2) $]
- *Mininum Misplaced Slots*
  - Generate all possible winning boards and compare the current state with a possible winning state. This gives the number of misplaced tiles and computes the minimum number of misplaced pieces.
  #text(size: 0.82em)[$ h = ceil("Mininum Misplaced Slots" / 4) $]
- *Pattern Database*
  - Choose a subset of tiles and pre-compute the exact number of moves to solve them from every configuration, storing the results in a database. During the game, simply look up the database.  Since solving a subset is always easier than solving all 20 pieces, this is always a valid lower bound.

== Our Implementation — Architecture

*Architecture (MVC-like):*

#align(center)[
  #table(
    columns: 3,
    align: (center, center, center),
    fill: (_, row) => if row == 1 { rgb("#E8F4F8") } else { white },
    [*UI Layer*], [*Logic Layer*], [*Data Layer*],
    [main.py \ Pygame], [Board], [TreeNode],
    [menu_view \ game_view], [Search Algorithms],
  )
]

*Data Flow:*
1. User selects board config and algorithm via menu
2. `main.py` builds a `Board` instance and starts solver in background thread
3. `Board` provides child states and goal test to search algorithms
4. Search algorithms build a tree of `TreeNode`s to find solution
5. Solution moves are animated on screen via _`Pygame`_

*Important detail:* board state is an immutable `tuple` so it's safe to share across threads with no locking.

== Our Implementation — Algorithms

#table(
  columns: (auto, auto, 1fr),
  align: (left, left, left),
  fill: (_, row) => if row == 0 { rgb("#E8F4F8") } else { white },
  [*Algorithm*], [*Type*], [*Properties*],
  [BFS],          [Uninformed], [Level by level exploration. Optimal but uses a lot of memory],
  [DFS],          [Uninformed], [Follows one path to the end. Low memory but solution is not always optimal],
  [IDS],          [Uninformed], [Runs DFS with increasing depth limits. Optimal and low memory],
  [Greedy],       [Informed],   [Expands the node closest to the goal. Fast but not always optimal],
  [A\*],          [Informed],   [Expands lowest f = g + h. Optimal with an admissible heuristic],
  [Weighted A\*], [Informed],   [Like A\* with f = g + w·h. Faster than A\* but solution may not be optimal],
)

#v(6pt)
All solvers run in a *background thread* so the UI never freezes. \
*Hint system:* Greedy runs in the background while the human plays to suggest the next best move.

== Experimental Results — Uninformed Search
#lorem(80)

== Experimental Results — Informed Search
#lorem(80)

== Conclusions
#lorem(80)

== References & Materials

*Scientific articles*
- Bortoluzzi, P. P. (2012). _A Pattern Database Approach for Solving the TopSpin Puzzle Problem_. University of Basel. #link("https://ai.dmi.unibas.ch/papers/theses/bortoluzzi-bachelor-12.pdf")

*Puzzle resources*
- Scherphuis, J. _Topspin / No. Crunch_. Jaap's Puzzle Page. #link("https://www.jaapsch.net/puzzles/topspin.html")
- Mortensen, E. (2017). _Top Spin Puzzle Review and Solution_. Geeky Hobbies. #link("https://www.geekyhobbies.com/top-spin-puzzle-review-solution")
- Mulholand, J. (2019). _Oval Track Puzzle_. Simon Fraser University. #link("https://www.sfu.ca/~jtmulhol/math302/puzzles-ot.html")

*Software & tools*
- Python 3.13 + Pygame 2 — #link("https://python.org") / #link("https://pygame.org")
- uv (package manager) — #link("https://docs.astral.sh/uv/")
- just (task runner) — #link("https://github.com/casey/just")
- Typst + diatypst theme — #link("https://typst.app") / #link("https://github.com/skriptum/diatypst")
- Ruff (linter/formatter) — #link("https://docs.astral.sh/ruff/")
