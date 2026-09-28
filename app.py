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
	Question("What is the name of Santa's reindeer with a glowing red nose?", ("Comet", "Dasher", "Rudolph", "Vixen"), "Rudolph", "Rudolph was created for a 1939 story and became part of modern Christmas culture."),
	Question("In the song, what did the little drummer boy play?", ("A flute", "A drum", "A bell", "A violin"), "A drum", "The song is called The Little Drummer Boy."),
	Question("Which plant is traditionally hung for a Christmas kiss?", ("Holly", "Ivy", "Mistletoe", "Rosemary"), "Mistletoe", "Mistletoe is the traditional kissing plant."),
	Question("What is traditionally placed on top of a Christmas tree?", ("A star or angel", "A snowman", "A bell pepper", "A stocking"), "A star or angel", "The star can represent the Star of Bethlehem, while an angel recalls the Christmas story."),
	Question("Which warm drink is often served at Christmas?", ("Lemonade", "Hot chocolate", "Iced tea", "Milkshake"), "Hot chocolate", "Hot chocolate is a popular warm Christmas drink."),
	Question("What color is Santa's suit most commonly shown as?", ("Green", "Blue", "Red", "Purple"), "Red", "Modern Christmas illustrations most commonly show Santa in red."),
	Question("What do people commonly exchange at Christmas?", ("Gifts", "Umbrellas", "Schoolbooks", "Maps"), "Gifts", "Exchanging gifts is a familiar Christmas tradition."),
	Question("Which ancient Roman festival is often discussed when explaining the history of winter celebrations?", ("Saturnalia", "Lupercalia", "Floralia", "Vinalia"), "Saturnalia", "Saturnalia was a Roman winter festival known for feasting and gift giving."),
	Question("Who wrote A Christmas Carol?", ("Jane Austen", "Charles Dickens", "Mark Twain", "Oscar Wilde"), "Charles Dickens", "Charles Dickens published A Christmas Carol in 1843."),
	Question("What is the name of the traditional Christmas ballet with the Sugar Plum Fairy?", ("Swan Lake", "The Nutcracker", "Giselle", "Coppelia"), "The Nutcracker", "Tchaikovsky's The Nutcracker is a classic Christmas-season ballet."),
	Question("Which country is widely associated with popularizing the Christmas tree tradition?", ("Germany", "Brazil", "Egypt", "Australia"), "Germany", "The modern Christmas tree tradition became especially popular in German-speaking regions."),
	Question("What does the word Noel commonly mean in Christmas songs?", ("Winter", "Christmas", "Star", "Candle"), "Christmas", "Noel comes from a word associated with Christmas and the Christmas season."),
	Question("Which Christmas song begins with the words 'You better watch out'?", ("Jingle Bells", "Santa Claus Is Coming to Town", "Silent Night", "O Holy Night"), "Santa Claus Is Coming to Town", "The song playfully warns children that Santa is on his way."),
	Question("What is panettone?", ("A festive Italian sweet bread", "A candle holder", "A Christmas dance", "A type of ornament"), "A festive Italian sweet bread", "Panettone is a tall, airy sweet bread traditionally eaten in Italy at Christmas."),
	Question("In many countries, what does an Advent calendar count down to?", ("New Year's Day", "Christmas Day", "Valentine's Day", "The first snowfall"), "Christmas Day", "Advent calendars count the days leading up to Christmas."),
	Question("What is a yule log traditionally called in French?", ("Buche de Noel", "Pain d'epices", "Galette des rois", "Croquembouche"), "Buche de Noel", "Buche de Noel is a French Christmas cake shaped like a log."),
	Question("Which famous Christmas market tradition is strongly associated with Nuremberg?", ("Christkindlesmarkt", "Mardi Gras", "Oktoberfest", "La Tomatina"), "Christkindlesmarkt", "Nuremberg's Christkindlesmarkt is one of Germany's best-known Christmas markets."),
	Question("What does an evergreen tree symbolize in many winter traditions?", ("Life continuing through winter", "The end of summer", "A new school year", "The longest night"), "Life continuing through winter", "Evergreen plants stay green through winter and are often linked with life and hope."),
	Question("Which film features the character Kevin McCallister?", ("Elf", "Home Alone", "The Polar Express", "The Holiday"), "Home Alone", "Kevin is the child who protects his home in Home Alone."),
	Question("What modern technology has made sending digital Christmas greetings common?", ("Email", "Typewriter ribbon", "Film projector", "Compass"), "Email", "Email and messaging apps let people send digital Christmas greetings instantly."),
	Question("Why are LED lights popular for modern Christmas decorations?", ("They use less energy", "They melt snow", "They make trees grow", "They play music automatically"), "They use less energy", "LED bulbs generally use less energy and last longer than older incandescent bulbs."),
	Question("What is a common way communities celebrate Christmas today?", ("A charity gift drive", "A tax audit", "A science exam", "A silent classroom"), "A charity gift drive", "Many communities organize gift, food, or toy drives during the Christmas season."),
	Question("Which streaming activity is now common during the holiday season?", ("Watching Christmas films", "Listening to weather reports all day", "Reading train schedules", "Viewing cooking timers"), "Watching Christmas films", "Holiday films and specials are widely watched through streaming services today."),
)

ROUND_SIZE = 8


def choose_questions(questions: Sequence[Question], previous: Sequence[Question] = ()) -> list[Question]:
	"""Choose a fresh random round, avoiding the previous round when possible."""
	available = [question for question in questions if question not in previous]
	if len(available) < ROUND_SIZE:
		available = list(questions)
	return random.sample(available, min(ROUND_SIZE, len(available)))


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
	previous_round: list[Question] = []
	while True:
		previous_round = choose_questions(QUESTIONS, previous_round)
		play_quiz(previous_round)
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
