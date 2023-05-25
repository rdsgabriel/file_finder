import click
import shutil
from tabulate import tabulate
from pathlib import Path
from utils import find_by_extension
from utils import find_by_name
from utils import find_by_modified
from utils import get_files_details
from utils import get_folders
from datetime import datetime


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
        "extension": find_by_extension,
        "modified": find_by_modified
    }

    files = search_dict[key](path, value)

    if recursive:
        subdirs = get_folders(path)
        for subdir in subdirs:
            files += process_search(subdir, key, value, recursive)

    return files


def process_results(files, key, value):
    if not files:
        click.echo(click.style(f'Nenhum arquivo com {key} {value} foi encontrado.', bg='red', italic=True))
    else:
        table_headers = ["Nome", "Modificação", "Localização"]
        table_data = get_files_details(files)
        tabulated_data = tabulate(tabular_data=table_data, headers=table_headers, tablefmt='tsv')
        click.echo(tabulated_data)
        return tabulated_data


@click.command()
@click.argument("path", default="")
@click.option("-k", "--key", required=True, type=click.Choice(["name", "extension", "modified"]))
@click.option("-v", "--value", required=True)
@click.option("-r", "--recursive", is_flag=True, default=False)
@click.option("-c", "--copy-to")
@click.option("-s", "--save", is_flag=True, default=False)
def finder(path, key, value, recursive, copy_to, save):
    root = Path(path)

    if not root.is_dir():
        raise Exception('O caminho informado não representa um diretório.')
    click.echo(f'O diretório selecionado foi: {root.absolute()}')

    files = process_search(path=root, key=key, value=value, recursive=recursive)
    report = process_results(files=files, key=key, value=value)

    save_report(report=report, save=save, root=root)
    copy_files(copy_to=copy_to, files=files)


finder()
