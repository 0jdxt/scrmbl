import random
import string
import time
import sys

import click

__version__ = '0.1.1'

random.seed()

ALL_CHARS = string.digits + string.ascii_letters + string.punctuation
try:
    COLS, _ = click.get_terminal_size()
except OSError: # not being run from terminal
    COLS = int(1e6)


def echo(message:str, charset:str=ALL_CHARS, speed:float=0.05, iterations:int=2) -> None:
    "scrambl print the given message"
    charset = charset.replace('\n', '').replace('\r', '')
    for line in message.split('\n'):
        echoed = ''
        for char in line:
            for iteration in range(iterations):
                click.echo('\r{}{}'.format(echoed, random.choice(charset)), nl=False)
                time.sleep(speed)

            echoed += char
            if len(echoed) >= COLS - 1:
                click.echo('\r' + echoed)
                echoed=''
        click.echo('\r' + echoed)


@click.command()
@click.argument('text_in', default='')
@click.option('-s', '--speed', type=click.FLOAT, default=0.05)
@click.option('-i', '--iter', 'niter', type=click.INT, default=2)
@click.option('-c', '--chars', type=click.Path(
    exists=True, allow_dash=True, dir_okay=False
))
@click.version_option(version=__version__)
def cli(text_in, speed, niter, chars):
    if not text_in: # no text input
        if sys.stdin.isatty() or chars == '-': # if no stdin or '-c -'
            raise click.UsageError('Need TEXT_IN or stdin input.')

        for line in sys.stdin:
            textin += line

    if chars:
        with click.open_file(chars) as f:
            charset = f.read()
    else:
        charset = ALL_CHARS

    echo(text_in.strip(), charset=charset, speed=speed, iterations=niter)

if __name__ == '__main__':
    cli()
