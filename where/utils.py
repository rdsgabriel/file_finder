from datetime import datetime
from where.exceptions import InvalidInputError


def get_folders(path):
    """
    Obtém todos os subdiretórios no diretório pesquisado.
    :param path: Um objeto Path() que representa o diretório.
    :return: Uma lista de objetos Path() em que cada elemento será um diretório que existe em `path`.
    """
    return [item for item in path.iterdir() if item.is_dir()]


def get_files(path):
    """
    Obtém todos os arquivos do diretório pesquisado.
    :param path: Um objeto Path() que representa o diretório.
    :return: Uma lista de objetos em que cada elemento será um arquivo que existe em `dir`.
    """
    return [item for item in path.iterdir() if item.is_file()]


def find_by_name(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que
    tenham um nome igual a `value` (independente da extensão)
    :param path: Um objeto Path() que representa o diretório.
    :param value: str que representa o nome que os arquivos podem ter.
    :return: Uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com um nome igual a `value`
    """
    return [file for file in get_files(path) if file.stem == value]


def find_by_extension(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que
    tenham um nome igual a `value` (independente do nome)
    :param path: Um objeto Path() que representa o diretório.
    :param value: str que representa a extensão que os arquivos podem ter.
    :return: Uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com extensão igual a `value`
    """
    return [file for file in get_files(path) if file.suffix == value]


def find_by_modified(path, value):
    """
    Obtém todos os arquivos no diretório pesquisado que
    tenham uma data de modificação mairo ou igual ao parâmetro informado.
    :param path: Um objeto Path() que representa o diretório.
    :param value: str que representa a menor data de modificação que os arquivos podem ter.
    :return: Uma lista de objetos Path() em que cada elemento será um
    arquivo em `path` com a data de modificação maior ou igual a `value`
    """
    try:
        datetime_obj = datetime.strptime(value, '%d/%m/%Y')
    except ValueError:
        raise InvalidInputError(f'{value} não é uma data válida no formato dd/mm/aaaa.')

    return [file for file in get_files(path) if datetime.fromtimestamp(file.stat().st_mtime) >= datetime_obj]


def timestamp_to_string(system_timestamp):
    """
    Gera uma str traduzindo os segundos para um formato humanamente legível.

    :param system_timestamp: um float que representa um timestamp do sistema
    :return: str que representa o timestamp em 'd/mm/aaaa - hh:mm:ss.vvvvv' (in doc)
    """
    datetime_obj = datetime.fromtimestamp(system_timestamp)
    return datetime_obj.strftime('%d/%m/%Y - %H:%M:%S:%f')


def get_files_details(files):
    """
    Obtém uma lista de listas, contendo os detalhes que vão ser expostos na CLI.
    :param files: Lista de objetos Path(), apontando para os arquivos no sistema.
    :return: Uma lista de lista contendo os detalhes a serem expostos na CLI.
    """
    files_details = []

    for file in files:
        stat = file.stat()
        details = [
            file.name,
            timestamp_to_string(stat.st_mtime),
            file.absolute()
        ]
        files_details.append(details)

    return files_details
        
