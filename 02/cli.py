import re
from collections import deque
from math import prod

import click


def parseLine(line, colours, **kwargs):
    game = re.match(
        r"Game (\d+): ",
        line,
    )

    (game_number,) = game.groups()
    output = (game_number, colours)

    parts = line[game.end() :].split(";")
    games = [f.strip().split(",") for f in parts]

    for g in games:
        for pick in g:
            match = re.match(r"\s*(\d+) (red|green|blue)", pick)
            if match:
                (num, colour) = match.groups()
                max_num = colours[colour]
                if int(num) > max_num:
                    output = (
                        kwargs["output"](game_number) if "output" in kwargs else output
                    )
                    if "update" in kwargs:
                        kwargs["update"](colours, colour, num)

    return output


def outputIsFalse(game_number):
    return (game_number, False)


def updateColours(colours, colour, num):
    colours[colour] = int(num)


def outputPart1(file, red, green, blue):
    validGames = 0
    validNum = 0
    for line in deque(file):
        (game, valid) = parseLine(
            line, {"red": red, "blue": blue, "green": green}, output=outputIsFalse
        )

        if valid:
            validNum += int(game)
            validGames += 1

    click.echo(f"r: {red}, g: {green}, b: {blue}")
    click.echo(f"valid games: {validGames}")
    click.echo(f"valid sum: {validNum}")


def outputPart2(file, red, green, blue):
    validNum = 0
    for line in deque(file):
        (_, colours) = parseLine(
            line, {"red": 0, "blue": 0, "green": 0}, update=updateColours
        )
        validNum += prod([colours[colour] for colour in colours])

    click.echo(f"r: {red}, g: {green}, b: {blue}")
    click.echo(f"valid sum: {validNum}")


@click.command()
@click.option("--red", type=click.INT, default=12)
@click.option("--green", type=click.INT, default=13)
@click.option("--blue", type=click.INT, default=14)
@click.option("--part", type=click.Choice(["1", "2"]), default="1")
@click.argument("file", type=click.File(mode="r"))
def cli(file, red, green, blue, part):
    if part == "1":
        outputPart1(file, red, green, blue)

    if part == "2":
        outputPart2(file, red, green, blue)


if __name__ == "__main__":
    cli()
