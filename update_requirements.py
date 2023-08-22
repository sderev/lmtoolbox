import requests


def get_latest_version(package_name):
    """
    Fetches the latest version of the package from PyPI.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()["info"]["version"]
    except requests.RequestException as error:
        print(f"Error fetching version for {package_name}: {error}")
        return None


def update_requirements(packages_to_update, requirements_path="requirements.txt"):
    """
    Updates the requirements.txt with the latest versions of the specified packages.
    """
    with open(requirements_path, "r", encoding="UTF-8") as file:
        lines = file.readlines()

    updated_lines = []
    for line in lines:
        pkg_name = line.split("==")[0].strip()
        if pkg_name in packages_to_update and (version := get_latest_version(pkg_name)):
            updated_lines.append(f"{pkg_name}=={version}\n")
            continue
        updated_lines.append(line)

    with open(requirements_path, "w", encoding="UTF-8") as file:
        file.writelines(updated_lines)


if __name__ == "__main__":
    packages_to_update = ["lmt-cli", "shellgenius", "vocabmaster"]
    update_requirements(packages_to_update)
