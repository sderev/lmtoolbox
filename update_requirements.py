#!/usr/bin/python3

import json
import urllib.error
import urllib.request


def get_latest_version(package_name):
    """
    Fetches the latest version of the package from PyPI.
    """
    url = f"https://pypi.org/pypi/{package_name}/json"
    try:
        with urllib.request.urlopen(url) as response:
            if response.status == 200:
                data = response.read()
                decoded_data = data.decode("utf-8")
                return json.loads(decoded_data)["info"]["version"]
            else:
                print(
                    f"Error fetching version for {package_name}: HTTP {response.status}"
                )
                return None
    except urllib.error.HTTPError as error:
        print(f"Error fetching version for {package_name}: {error}")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON for {package_name}")
        return None
    except Exception as err:
        print(f"An unexpected error occurred for {package_name}: {err}")
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
    packages_to_update = ["lmterminal", "shellgenius", "vocabmaster"]
    update_requirements(packages_to_update)
