import pathlib

from hw4 import easy_solution, medium_solution

def main():
    pathlib.Path('artifacts').mkdir(exist_ok=True)

    easy_solution()
    medium_solution()

if __name__ == "__main__":
    main()