from src.parsing import MapParser
from pydantic import ValidationError
import sys


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <map_file>", file=sys.stderr)
        sys.exit(1)
    print("=== Getting Graph ===")
    try:
        graph = MapParser().get_graph(sys.argv[1])
        for element in graph:
            print(f"{element}\n")
    except (ValueError, ValidationError, IndexError) as err:
        print(f"Error: {err}")


if __name__ == "__main__":
    main()
