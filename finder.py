import click
from pathlib import Path
from utils import find_by_extension
from utils import find_by_name
from utils import find_by_modified
from utils import timestamp_to_string


def process_search(path, key, value):
    search_dict = {
        "name": find_by_name,
        "extension": find_by_extension,
        "modified": find_by_modified
    }

    files = search_dict[key](path, value)

    if not files:
        click.echo(f'Nenhum arquivo com {key} {value} foi encontrado.')
    else:
        for f in files:
            click.echo(click.style(
                '\n------------------------------------------------------------------------------------\n'
                f'Nome: {f.name}\n'              
                '------------------------------------------------------------------------------------\n'
                f'Data de Modificação: {timestamp_to_string(f.stat().st_mtime)}\n'
                '------------------------------------------------------------------------------------\n'
                f'Localização: {f.parent.absolute()}\n'
                '------------------------------------------------------------------------------------\n'
                , fg='green'

            ))


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(["name", "extension", "modified"]))
@click.option("-v", "--value", required=True)
def finder(path, key, value):
    root = Path(path)

    if not root.is_dir():
        raise Exception('O caminho informado não representa um diretório.')
    click.echo(f'O diretório selecionado foi: {root.absolute()}')

    process_search(path=root, key=key, value=value)


finder()
