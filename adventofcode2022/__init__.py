def read_file(FILE_PATH: str) -> str:
    with open(FILE_PATH) as f:
        return f.read()
