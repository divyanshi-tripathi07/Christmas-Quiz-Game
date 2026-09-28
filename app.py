"""A small, dependency-free Christmas quiz game."""

from dataclasses import dataclass
import random
from typing import Callable, Optional, Sequence


@dataclass(frozen=True)
class Question:
	prompt: str
	choices: tuple[str, ...]
	answer: str
	explanation: str


QUESTIONS: tuple[Question, ...] = (
	Question("Which day is Christmas Day?", ("December 24", "December 25", "December 26", "January 1"), "December 25", "Christmas Day is celebrated on December 25."),
	Question("What is the name of Santa's reindeer with a glowing red nose?", ("Comet", "Dasher", "Rudolph", "Vixen"), "Rudolph", "Rudolph is famous for his bright red nose."),
	Question("In the song, what did the little drummer boy play?", ("A flute", "A drum", "A bell", "A violin"), "A drum", "The song is called The Little Drummer Boy."),
	Question("Which plant is traditionally hung for a Christmas kiss?", ("Holly", "Ivy", "Mistletoe", "Rosemary"), "Mistletoe", "Mistletoe is the traditional kissing plant."),
	Question("What is traditionally placed on top of a Christmas tree?", ("A star or angel", "A snowman", "A bell pepper", "A stocking"), "A star or angel", "A star or angel is commonly used as the tree topper."),
	Question("Which warm drink is often served at Christmas?", ("Lemonade", "Hot chocolate", "Iced tea", "Milkshake"), "Hot chocolate", "Hot chocolate is a popular warm Christmas drink."),
	Question("What color is Santa's suit most commonly shown as?", ("Green", "Blue", "Red", "Purple"), "Red", "Modern Christmas illustrations most commonly show Santa in red."),
	Question("What do people commonly exchange at Christmas?", ("Gifts", "Umbrellas", "Schoolbooks", "Maps"), "Gifts", "Exchanging gifts is a familiar Christmas tradition."),
)


def read_answer(
	input_fn: Callable[[str], str],
	output_fn: Callable[[str], None],
	choice_count: int,
) -> Optional[int]:
	"""Read a choice and return its zero-based index, or None for quit."""
	labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	while True:
		raw = input_fn("Your answer (number or letter, or Q to quit): ").strip().upper()
		if raw in {"Q", "QUIT", "EXIT"}:
			return None
		if raw.isdigit() and 1 <= int(raw) <= choice_count:
			return int(raw) - 1
		if len(raw) == 1 and raw in labels[:choice_count]:
			return labels.index(raw)
		output_fn(f"Please enter a number from 1 to {choice_count}, a letter, or Q.")


def play_quiz(
	questions: Sequence[Question] = QUESTIONS,
	input_fn: Callable[[str], str] = input,
	output_fn: Callable[[str], None] = print,
	shuffle_fn: Callable[[list], None] = random.shuffle,
) -> Optional[int]:
	"""Play one round and return the score, or None if the player quits."""
	if not questions:
		output_fn("There are no questions available.")
		return 0

	round_questions = list(questions)
	shuffle_fn(round_questions)
	score = 0

	for number, question in enumerate(round_questions, start=1):
		choices = list(question.choices)
		shuffle_fn(choices)
		output_fn(f"\nQuestion {number} of {len(round_questions)}: {question.prompt}")
		for index, choice in enumerate(choices, start=1):
			output_fn(f"  {index}. {choice}")

		selected = read_answer(input_fn, output_fn, len(choices))
		if selected is None:
			output_fn(f"\nYou stopped at {score}/{number - 1}.")
			return None

		chosen = choices[selected]
		if chosen == question.answer:
			score += 1
			output_fn("Correct!")
		else:
			output_fn(f"Not quite. The correct answer is {question.answer}.")
		output_fn(question.explanation)

	output_fn(f"\nFinal score: {score}/{len(round_questions)}")
	if score == len(round_questions):
		output_fn("Perfect score. Merry Christmas!")
	elif score * 2 >= len(round_questions):
		output_fn("Great job!")
	else:
		output_fn("Good try. Play again to improve your score!")
	return score


def main() -> None:
	print("\n=== Christmas Quiz Game ===")
	print("Test your holiday knowledge. Enter Q at any question to stop.\n")
	while True:
		play_quiz()
		while True:
			replay = input("\nPlay again? (Y/N): ").strip().upper()
			if replay in {"Y", "YES"}:
				break
			if replay in {"N", "NO", "Q", "QUIT"}:
				print("Thanks for playing!")
				return
			print("Please enter Y or N.")


if __name__ == "__main__":
	main()
