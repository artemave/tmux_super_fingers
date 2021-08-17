def eval_file(path: str) -> None:
    with open(path) as code:
        exec(code.read())
