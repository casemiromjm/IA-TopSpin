#import "@preview/diatypst:0.9.1": *

#set text(font: "Lato", ligatures: false)
#show figure.caption: set text(size: 0.75em)

#show: slides.with(
  title: "Project 1 Checkpoint: Top Spin",
  subtitle: "Artificial Intelligence 2025/26 @ FEUP",
  authors: ("Casemiro Melo Jorge de Medeiros", "Mariana Almeida Cabral", "Pedro Andrade Castro"),
  ratio: 16 / 9,
  theme: "full",
  bg-color: rgb("#FFF6F6"),
  title-color: rgb("#2C687B"),
  count: "dot-section",
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

The Player can move the yellow pieces to the left or to the right and can also turn the purple circle to rotate the yellow pieces

== Related Work

// TODO

Some related work

== Problem Formulation

states:

initial state:

objective test:

operators: in Top Spin game there is 3 operators, `move_right`, `move_left`, `spin`. The `move` operators represents the slide to the right or the slide to the left. Lastly, the `spin` operator represents the spin made in the center circle that rotates the slots.

heuristics / evaluation functions:

== Current Implementation

Our implementation is being done in Python 3.12. It uses _#link("https://docs.astral.sh/uv/", "UV")_ for project management (i.e. handling virtual environments, handling dependencies, etc.). We also use _pygame_ for UI and _ruff_ for linting and formatting our code. In addition to that, we utilize _#link("https://github.com/casey/just", "Just")_, a tool similar to Makefile but more modern.

As for data structures, we utilize a *list* for our board, a *tuple* for a state.
