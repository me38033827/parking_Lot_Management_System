from collections import defaultdict, deque
import json, math
# return the shortest distance and corresponding path
# call shortestPath(parkLot) where parkLot is the id of the parkLot point


class Graph(object):
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

        with open('utils/parkingdb.json') as json_file:
            park = json.load(json_file)

        for point in park:
            if point['fields']['isParkingLot'] == False:
                self.add_node(point['pk'])
                nearpoints = intToList(point['fields']['nearPoint'])
                x = [point['fields']['xCoord'], point['fields']['yCoord']]
                for nearpoint in nearpoints:
                    if park[nearpoint]['fields']['isParkingLot'] == False:
                        y = [park[nearpoint]['fields']['xCoord'], park[nearpoint]['fields']['yCoord']]
                        self.add_edge(point['pk'], nearpoint, distance(x, y))

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijkstra(graph, initial):
    visited = {initial: 0}
    path = {}

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node
        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            try:
                weight = current_weight + graph.distances[(min_node, edge)]
            except:
                continue
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge] = min_node

    return visited, path


def shortest_path(graph, origin, destination):
    visited, paths = dijkstra(graph, origin)
    full_path = deque()
    _destination = paths[destination]

    while _destination != origin:
        full_path.appendleft(_destination)
        _destination = paths[_destination]

    full_path.appendleft(origin)
    full_path.append(destination)

    return visited[destination], list(full_path)


def intToList(nearPoints):
    points = []
    while (nearPoints // 100 > 0):
        points.append(nearPoints % 100)
        nearPoints = nearPoints // 100
    points.append(nearPoints)
    return points


def distance(x, y):
    return math.sqrt(((x[0] - y[0]) ** 2) + ((x[1] - y[1]) ** 2))


def shortestPath(xCoord,yCoord, type="car"):
    graph = Graph()

    with open('utils/parkingdb.json') as json_file:
        park = json.load(json_file)

    parkLotX=park[0]['fields']['xCoord']
    parkLotY=park[0]['fields']['yCoord']
    minDis=distance([xCoord,yCoord],[parkLotX,parkLotY])
    parkLot=0

    for i in range(1,28):
        parkLotX = park[i]['fields']['xCoord']
        parkLotY = park[i]['fields']['yCoord']
        if distance([xCoord,yCoord],[parkLotX,parkLotY])<=minDis:
            minDis=distance([xCoord,yCoord],[parkLotX,parkLotY])
            parkLot=i


    result = []
    if parkLot <= 10 or parkLot >= 17:
        origin = park[parkLot]['fields']['nearPoint']
        if type == "car":
            result.append(shortest_path(graph, origin, 30))
            result.append(shortest_path(graph, origin, 31))
        else:
            result.append(shortest_path(graph, origin, 28))
            result.append(shortest_path(graph, origin, 29))
            result.append(shortest_path(graph, origin, 30))
            result.append(shortest_path(graph, origin, 31))

        minDistance = min(result[i][0] for i in range(len(result)))
        for i in range(len(result)):
            if result[i][0] == minDistance:
                return result[i]

    else:
        origins = intToList(park[parkLot]['fields']['nearPoint'])
        if type == "car":
            result.append(shortest_path(graph, origins[0], 30))
            result.append(shortest_path(graph, origins[0], 31))
            result.append(shortest_path(graph, origins[1], 31))
            result.append(shortest_path(graph, origins[1], 30))
        else:
            result.append(shortest_path(graph, origins[0], 28))
            result.append(shortest_path(graph, origins[0], 29))
            result.append(shortest_path(graph, origins[0], 30))
            result.append(shortest_path(graph, origins[0], 31))
            result.append(shortest_path(graph, origins[1], 28))
            result.append(shortest_path(graph, origins[1], 29))
            result.append(shortest_path(graph, origins[1], 31))
            result.append(shortest_path(graph, origins[1], 30))

        minDistance = min(result[i][0] for i in range(len(result)))
        for i in range(len(result)):
            if result[i][0] == minDistance:
                return result[i]



def recommend(carPosition,LotPosition):
    if carPosition==LotPosition:
        return [0,[]]

    graph = Graph()

    return shortest_path(graph,carPosition,LotPosition)
