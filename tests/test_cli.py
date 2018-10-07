import click
from click.testing import CliRunner

from scrmbl.cli import cli

def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(cli, ['Hello, world!'])
    assert result.exit_code == 0
    assert result.output.split('\r')[-1] == 'Hello, world!\n'


def test_input_stream():
    runner = CliRunner()
    with open('tests/lipsum.txt', 'r') as fin:
        data = fin.read()
    result = runner.invoke(cli, ['-s 0'], input=data)
    assert result.exit_code == 0
    for line in result.output.split('\r'):
        assert line[:-1] in data
