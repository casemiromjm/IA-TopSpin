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
  count: "dot",
)

/*
= This creates a new section slide

== This creates a new simple slide
*/

== Problem Specification

Our project is based in the Top Spin game. This game is similar to Rubik's Cube, but only in 2D.

#align(center)[
  #figure(
    image("./assets/topspin.jpg", height: 35%),
    caption: [Top Spin Board: Rotating the center "spin" disk swaps the inner pieces.],
  )
]

The game consists of 20 rounded pieces, numbered from 1 to 20, placed in one long looped track. It also has a turntable in the loop, which allows the player to rotate any 4 adjacent pieces so that they will be in reverse order.

== Related Work

- Bortoluzzi, P. P. (2012) #link("https://ai.dmi.unibas.ch/papers/theses/bortoluzzi-bachelor-12.pdf")[#text([A Pattern Database Approach
    for Solving the TopSpin Puzzle Problem])]. University of Basel.
- Mortensen, E. (2017) #link("https://www.geekyhobbies.com/top-spin-puzzle-review-solution")[#text([Top Spin Puzzle Review and Solution])]. Geeky Hobbies
- Scherphuis, J. #link("https://www.jaapsch.net/puzzles/topspin.html")[#text([Topspin / No. Crunch])]. Jaap's Puzzel Page.
- Jamie Mulholand (2019) #link("https://www.sfu.ca/~jtmulhol/math302/puzzles-ot.html")[#text([Oval Track puzzle])]. Simon Fraser University

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
- *Heuristics / Evaluation Functions*:
  - Adjacency, Mininum Misplaced Pieces, Pattern Database

  - Adjacency (Number of Breaks)
    - Instead of looking for the piece itself, check the neighbouring piece to see if it is in the correct order. Piece _i_ must be followed by piece _i+1_, but piece 20 must be followed by piece 1. Moving a piece does not fix any breaks; only spinning fixes them (at most two, on the edges).
    $ h = ceil("Number of Breaks" / 2) $

  - Mininum Misplaced Slots
    - Generate all possible winning boards and compare the current state with a possible winning state. This gives the number of misplaced tiles and computes the minimum number of misplaced pieces.
  $ h = ceil("Mininum Misplaced Slots" / 4) $

  - Pattern Database
    - Pick a subset of tiles and treat all the others as indistinguishable 'blank' tiles. Before running the game, run a search for only the subset and store the number of moves needed to solve it from any configuration in a database (i.e. a dictionary/map, a file). During the game, simply look up the database. The cost of solving 20 pieces is always greater than the cost of solving a smaller number of pieces.

  // vamos precisar de uma heuristica non-admissable p o weighted A*

== Our Implementation

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

*Search Algorithms:* BFS, DFS, Iterative Deepening Search (run in background thread)

== Experimental results

#lorem(80)
