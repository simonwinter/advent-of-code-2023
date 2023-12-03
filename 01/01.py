import re
from collections import deque

import click


def findMatch(line):
    matches = re.findall("\d", line)

    if matches:
        return int(matches[0] + matches[-1])

    return 0


@click.command()
@click.argument("file", type=click.File(mode="r"))
def cli(file):
    matches = [findMatch(line) for line in deque(file)]
    click.echo(f"the correct coordinate number is {sum(matches)}", nl=True)


if __name__ == "__main__":
    cli()
