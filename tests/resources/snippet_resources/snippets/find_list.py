# updated_snippets
def find_list(item: str, keys: list[str]) -> bool:
    for key in keys:
        if item.find(key) != -1:
            return True
    return False
