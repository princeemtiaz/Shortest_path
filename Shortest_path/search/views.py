from django.shortcuts import render
from .forms import ShortestDistanceForm
from .models import District,Distance
from collections import defaultdict
from django.db.models import Q
from heapq import heappop, heappush

def find_shortest_distance(request):
    form = ShortestDistanceForm(request.POST or None)
    shortest_distance = None
    shortest_path = None
    total_path = Distance.objects.all()
    if request.method == 'POST' and form.is_valid():
        source_district = form.cleaned_data['source_district']
        destination_district = form.cleaned_data['destination_district']

        print(source_district)
        print(destination_district)
        shortest_distance, shortest_path = dijkstra_shortest_path(source_district, destination_district)
        print(shortest_distance)
        shortest_path = "-->".join([district.name for district in shortest_path])
    return render(request, 'search.html', {'form': form, 'shortest_distance': shortest_distance, 'shortest_path': shortest_path, 'total_path' : total_path})


from collections import defaultdict
import heapq


def dijkstra_shortest_path(start_district, end_district):
    distances = {district: float('inf') for district in District.objects.all()}
    distances[start_district] = 0
    visited = {}

    queue = [(0, start_district)]

    while queue:
        current_distance, current_district = heapq.heappop(queue)

        # Skip if the district is already visited
        if current_district in visited:
            continue

        visited[current_district] = True

        # Check if we have reached the end district
        if current_district == end_district:
            break

        # Update the distances of neighboring districts
        for distance in current_district.source_distances.all():
            neighbor_district = distance.destination_district
            new_distance = current_distance + distance.distance

            if new_distance < distances[neighbor_district]:
                distances[neighbor_district] = new_distance
                heapq.heappush(queue, (new_distance, neighbor_district))

    # Generate the shortest path
    path = []
    current_district = end_district

    while current_district != start_district:
        path.append(current_district)
        current_district = min(distances, key=lambda d: distances[d] if d not in path else float('inf'))

    path.append(start_district)
    path.reverse()

    return distances[end_district], path