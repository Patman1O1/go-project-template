# Builtin Imports
import sys
import os

# Pip Imports
from jinja2 import Environment, Template, FileSystemLoader

class Project(object):
    def __init__(self, argv: list[str]) -> None:  # raises ValueError
        if len(argv) < 4:
            raise ValueError(f"Usage {argv[0]} <project_name> <project_author> {{Library|Executable}}")
        self.name = argv[1]
        self.author = argv[2]
        self.type = argv[3]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name: str = value

    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        self._author: str = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str) -> None:  # raises ValueError
        if value != "Executable" and value != "Library":
            raise ValueError(f"Expected 'value' to be 'Executable' or 'Library' but got '{value}'")
        self._type: str = value

    def render(self) -> None:
        # Set the environment
        env: Environment = Environment(loader=FileSystemLoader(os.getcwd()))

        # Get the templates
        mod_template: Template = env.get_template("go.mod.j2")
        src_template: Template = env.get_template("src/{{ project.name }}.go.j2")

        # Render the go.mod.j2 template
        with open("go.mod.j2", "w", encoding="utf-8") as mod_file:
            mod_file.write(mod_template.render(project=self))

        # Rename go.mod.j2 to go.mod
        os.rename("go.mod.j2", "go.mod")

        # Render the source file template
        with open("src/{{ project.name }}.go.j2", "w", encoding="utf-8") as src_file:
            src_file.write(src_template.render(project=self))

        # Rename "src/{{ project.name }}.rs.j2" to "src/<project_name>.rs" where <project_name> is the .name property
        if self.type == "Executable":
            os.rename("src/{{ project.name }}.go.j2", "src/main.go")
        else:
            os.rename("src/{{ project.name }}.go.j2", f"src/{self.name}.go")

def main() -> int:
    try:
        project: Project = Project(sys.argv)
        project.render()
        return 0
    except Exception as exception:
        os.write(os.STDERR_FILENO, str(f"{exception}\n").encode("utf-8"))
        return 1

if __name__ == "__main__":
    sys.exit(main())