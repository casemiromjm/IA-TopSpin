#import "@preview/diatypst:0.9.1": *

#set text(font: "Lato", ligatures: false)
#show figure.caption: set text(size: 0.75em)

#show: slides.with(
  title: "Project 1 Checkpoint",
  subtitle: "Artificial Intelligence 2025/26 @ FEUP",
  authors: ("Casemiro Melo Jorge de Medeiros", "Mariana Almeida Cabral", "Pedro Andrade Castro"),
  ratio: 16/9,
  theme: "full",
  bg-color: rgb("#FFF6F6"),
  title-color: rgb("#2C687B"),
  count: "dot-section",
)

/*
= This creates a new section slide

== This creates a new simple slide
*/

= What is our project?
== Specification
// definition of the problem to be solved (the game)
Our project is based in the Top Spin game. This game is similar to Rubik's Cube, but only in 2D.

#figure(
  image("./assets/topspin.jpg", scaling: "smooth", height: 45%, ),
  caption: text("Real Top Spin board")
)

The Player can move the yellow pieces to the left or to the right and can also turn the purple circle to rotate the yelleow pieces

= Related work
== Related work
// related work with references to works found in a bibliographic search (articles, web pages, and/or source code)

//TODO

Some related work

= Top Spin as a search problem
== Top Spin as a search problem
// state representation, initial state, objective test, operators, heuristics/evaluation function

// TODO

states:

initial state:

objective test:

operators: in Top Spin game there is 3 operators, `move_right`, `move_left`, `spin`. The `move` operators represents the slide to the right or the slide to the left. Lastly, the `spin` operator represents the spin made in the center circle that rotates the slots.

heuristics / evaluation functions:

=  Our Current Implementation
== Technologies
// programming language, development environment, data structures, etc.

Our implementation is being done in Python 3.12. It uses _#link("https://docs.astral.sh/uv/", "UV")_ for project management (i.e. handling virtual environments, handling dependencies, etc.). We also use _pygame_ for UI and _ruff_ for linting and formatting our code. In addition to that, we utilise _#link("https://github.com/casey/just", "Just")_, a tool similar to Makefile but more modern.

As for data structures, we utilise a *list* for our board, a *tuple* for a state.