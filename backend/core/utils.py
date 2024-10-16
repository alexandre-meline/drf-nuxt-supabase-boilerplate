def splitting_var_env(var_env: str) -> list[str]:
    """
    Get env variables from the settings, ensuring no leading or trailing spaces.
    """
    methods = var_env.split(',')
    return [method.strip() for method in methods]