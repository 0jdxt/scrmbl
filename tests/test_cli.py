from click.testing import CliRunner

from scrmbl.cli import cli


def test_hello_world():
    runner = CliRunner()
    result = runner.invoke(cli, ['Hello, world!'])
    assert result.exit_code == 0
    assert result.output.split('\r')[-1] == 'Hello, world!\n'


def test_input_stream():
    with open('tests/lipsum.txt', 'r') as fin:
        data = fin.read()
    runner = CliRunner()
    result = runner.invoke(cli, ['-s 0'], input=data)

    assert result.exit_code == 0

    lines = iter(result.output.split('\r'))
    # only retrieve longest lines i.e. full lines
    filt = []
    prev, curr = None, next(lines)
    while curr:
        if prev and len(curr) < len(prev):
            filt.append(prev)

        try:
            prev, curr = curr, next(lines)
        except StopIteration:
            curr = None

    for line in filt:
        assert line.split('\n')[0] in data


def test_invalid_cmd():
    runner = CliRunner()
    result = runner.invoke(cli, ['-c -'])
    assert result.exit_code == 2
    assert 'Error' in result.output
