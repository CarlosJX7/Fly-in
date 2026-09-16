from src.models import Hub, MapGraph
from src.parsing import MapParser


def main():
    path = "maps/easy/01_linear_path.txt"
    parser = MapParser()
    raw_data = parser.input_parser(path)
    parsed_data = parser.list_to_dict(raw_data)

    print("Dict created:")
    print(parsed_data)
    for element in parsed_data:
        print(element)
    print()

    print("=== Getting hubs list===")
    hubs = MapParser.get_hubs_list(parsed_data)
    print(hubs)
    print("===================")
    exit(1)
    print("=== Getting connections ===")
    #necesito que origin y destiny esten dentro de los hubs
    connections = parser.get_connections(parsed_data)
    print(connections[0])
    name_hub = connections[0].get("destiny_hub")
    hub1 = hubs[name_hub]
    print(hub1)
    #parser.create_connection(connections[0])
    print("===========================")

    print("=== Getting Graph")
    graph = parser.get_graph(path)


if __name__ == "__main__":
    main()