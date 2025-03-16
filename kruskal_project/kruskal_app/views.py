from django.shortcuts import render
from .kruskal import kruskal, prim, visualize_graph, is_graph_connected
import os

def home(request):
    error_message = None
    mst = []
    graph_image = None
    mst_image = None

    if request.method == 'POST':
        vertices = [v.strip() for v in request.POST.get('vertices').split(',')]
        edges = []

        # Validate edge input
        edge_input = request.POST.get('edges').strip()
        if edge_input:
            try:
                for edge in edge_input.split(';'):
                    parts = edge.split(',')
                    if len(parts) != 3:
                        raise ValueError("Invalid edge format. Use: A,B,1; B,C,2")
                    
                    v1, v2, weight = parts
                    edges.append((v1.strip(), v2.strip(), int(weight)))

            except ValueError:
                error_message = "Error: Invalid edge format! Use the format: A,B,1; B,C,2"
                return render(request, 'home.html', {
                    'error_message': error_message,
                    'vertices': vertices,
                    'edges': []
                })

        algorithm = request.POST.get('algorithm')
        start_node = request.POST.get('start_node')

        if not is_graph_connected(vertices, edges):
            error_message = "Error: The graph is disconnected. Please enter a connected graph."
            return render(request, 'home.html', {
                'error_message': error_message,
                'vertices': vertices,
                'edges': []
            })

        if algorithm == 'kruskal':
            mst = kruskal(vertices, edges)
        elif algorithm == 'prim' and start_node in vertices:
            mst = prim(vertices, edges, start_node)

        # Generate graph images
        graph_image_path = os.path.join('kruskal_app', 'static', 'original_graph.png')
        mst_image_path = os.path.join('kruskal_app', 'static', f'{algorithm}_mst_graph.png')

        visualize_graph(vertices, edges, [], graph_image_path)
        visualize_graph(vertices, edges, mst, mst_image_path)

        return render(request, 'home.html', {
            'mst': mst,
            'graph_image': 'static/original_graph.png',
            'mst_image': f'static/{algorithm}_mst_graph.png',
            'algorithm': algorithm,
            'vertices': vertices,
            'edges': edges
        })

    return render(request, 'home.html', {
        'mst': [],
        'graph_image': None,
        'mst_image': None,
        'algorithm': '',
        'vertices': [],
        'edges': [],
        'error_message': error_message
    })
