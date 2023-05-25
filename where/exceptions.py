class FileFinderError(Exception):
    """Classe mãe para tratar todas as excessões do file_finder."""
    pass


class InvalidInputError(FileFinderError):
    """Classe p erros devido inputs inválidos do usuário."""
    pass


class NoFileFound(FileFinderError):
    """Classe p erro de não encontrar arquivo."""
    pass
