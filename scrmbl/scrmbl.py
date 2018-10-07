import random
import string
import time

import click

random.seed()

ALL_CHARS = string.digits + string.ascii_letters + string.punctuation
try:
    COLS, _ = click.get_terminal_size()
except OSError:  # not being run from terminal
    COLS = int(1e6)


def echo(message: str, charset: str = ALL_CHARS, speed: float = 0.05,
         iterations: int = 2) -> None:
    """Scrambl print the given message."""
    # strip \n and \r from charset
    if not charset:
        charset = ALL_CHARS
    charset = charset.replace('\n', '').replace('\r', '')
    for line in message.split('\n'):
        echoed = ''
        for char in line:
            for _ in range(iterations):
                ran_char = random.choice(charset)
                click.echo('\r{0}{1}'.format(echoed, ran_char), nl=False)
                time.sleep(speed)

            echoed += char
            # this logic is so lines larger than the console format nicely
            if len(echoed) >= COLS - 1:
                click.echo('\r' + echoed)
                echoed = ''
        click.echo('\r' + echoed)
