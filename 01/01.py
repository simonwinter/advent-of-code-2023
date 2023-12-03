import re
from collections import deque

import click


@click.command()
@click.argument("file", type=click.File(mode="r"))
def cli(file):
    output = 0
    for line in deque(file):
        matches = re.findall("\d", line)
        if matches:
            output += int(matches[0] + matches[-1])

    click.echo(f"the correct coordinate number is {output}", nl=True)


if __name__ == "__main__":
    cli()
