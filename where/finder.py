import click
import shutil
from tabulate import tabulate
from pathlib import Path
from where.utils import find_by_extension
from where.utils import find_by_name
from where.utils import find_by_modified
from where.utils import get_files_details
from where.utils import get_folders
from datetime import datetime
from where.exceptions import InvalidInputError, NoFileFound, FileFinderError


def copy_files(copy_to, files):
    if copy_to:
        copy_path = Path(copy_to)
        if not copy_path.is_dir():
            copy_path.mkdir(parents=True)
        for file in files:
            dst_file = copy_path / file.name

            if dst_file.is_file():
                dst_file = copy_path / f'{file.stem}{datetime.now().strftime("%d%m%Y%H%M%S%f")}{file.suffix}'

            shutil.copy(src=file.absolute(), dst=dst_file)


def save_report(save, report, root):
    if save and report:
        report_file_path = root / f'finder_report_{datetime.now().strftime("%d%m%Y%H%M%S%f")}.txt'
        with open(report_file_path.absolute(), mode='w') as report_file:
            report_file.write(report)


def process_search(path, key, value, recursive):
    search_dict = {
        "name": find_by_name,
        "ext": find_by_extension,
        "mod": find_by_modified
    }

    files = search_dict[key](path, value)

    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += process_search(subdir, key, value, recursive)

    return files


def process_results(files, key, value):
    if not files:
        raise NoFileFound(f'Nenhum arquivo com {key} {value} foi encontrado.')

    table_headers = ["Nome", "Modificação", "Localização"]
    table_data = get_files_details(files)
    tabulated_data = tabulate(tabular_data=table_data, headers=table_headers, tablefmt='tsv')
    click.echo(tabulated_data)
    return tabulated_data


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(["name", "ext", "mod"]), help="Define o tipo de chave utilizada para a busca, podendo ser: Nome, Extensão ou última data de modificação do arquivo")
@click.option("-v", "--value", required=True, help="Define um valor para a chave.")
@click.option("-r", "--recursive", is_flag=True, default=False, help="Se presente, faz busca recursiva em todos os sub-diretórios.")
@click.option("-c", "--copy-to", help="Copia todos os arquivos para o caminho informado.")
@click.option("-s", "--save", is_flag=True, default=False, help="Se presente salva um 'relatório' da busca realizada.")
def finder(path, key, value, recursive, copy_to, save):
    """
    Um programa que realiza busca de arquivos por meio de uma chave (-k | --key) a partir do diretório PATH.

    PATH define o diretório onde a pesquisa inicia. Caso não informado, assume o diretório atual.
    """
    root = Path(path)

    if not root.is_dir():
        raise InvalidInputError(f'O caminho "{path}" não representa um diretório existente.')
    click.echo(f'O diretório selecionado foi: {root.absolute()}')

    files = process_search(path=root, key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key, value=value)

    save_report(report=report, save=save, root=root)
    copy_files(copy_to=copy_to, files=files)


if __name__ == '__main__':
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(f'❌ {err}', bg='black', fg='red', italic=True))
