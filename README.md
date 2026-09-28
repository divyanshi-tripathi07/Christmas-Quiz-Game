# Christmas Quiz Game

A dependency-free Christmas quiz available as a browser game and a command-line game.

## Browser game

The easiest option is to open [index.html](index.html) in a browser.

For a local URL, run this command from the project folder:

```text
python -m http.server 8000
```

Then open <http://localhost:8000>.

The browser game supports randomized questions and choices, number-key answers,
instant feedback, score tracking, restart, and a final results screen.

## Command-line game

Run:

```text
python app.py
```

Choose an answer with its number or letter. Invalid answers are retried, and
you can enter `Q` at any question to stop.
