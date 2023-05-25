import click
from where.finder import finder
from where.exceptions import FileFinderError


def cli():
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(f'❌ {err}', bg='black', fg='red', italic=True))
