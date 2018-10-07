import sys

import click

import scrmbl

@click.command()
@click.argument('text_in', default='')
@click.option('-s', '--speed', type=click.FLOAT, default=0.05,
              help='Time in seconds between prints. Default: 0.05')
@click.option('-i', '--iter', 'niter', type=click.INT, default=2,
              help='Number of iterations per character. Default: 2')
@click.option('-c', '--chars', type=click.Path(
    exists=True, allow_dash=True, dir_okay=False,
), help='Set of chars to scramble. Default: {0}'.format(scrmbl.ALL_CHARS))
# @click.version_option(version=scrmbl.__version__)
@click.version_option(version='0.1.1')  # cant find scrmbl__version__
def cli(text_in, speed, niter, chars):
    """Click cli endpoint."""
    if not text_in:  # no text input
        if sys.stdin.isatty() or chars == '-':  # if no stdin or '-c -'
            raise click.UsageError('Need TEXT_IN or stdin input.')

        for line in sys.stdin:
            text_in += line

    if chars:
        with click.open_file(chars) as f:
            charset = f.read()
    else:
        charset = scrmbl.ALL_CHARS

    scrmbl.echo(text_in.strip(), charset=charset, speed=speed, iterations=niter)
