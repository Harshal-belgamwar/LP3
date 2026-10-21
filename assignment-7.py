
def pagerank(graph, damping=0.85, iterations=100, tolerance=1e-6):
    
    pages = list(graph.keys())
    n = len(pages)

    if n == 0:
        return {}

    rank = {page: 1 / n for page in pages}

    for _ in range(iterations):
        new_rank = {
            page: (1 - damping) / n
            for page in pages
        }

     
        for page in pages:
            links = graph[page]

            if links:
                share = damping * rank[page] / len(links)

                for linked_page in links:
                    new_rank[linked_page] += share
            else:
              
                share = damping * rank[page] / n

                for target in pages:
                    new_rank[target] += share

        
        difference = sum(
            abs(new_rank[p] - rank[p]) for p in pages
        )

        rank = new_rank

        if difference < tolerance:
            break

    return rank


# Directed graph: pages and their outgoing links
graph = {
    "A": ["B", "C"],
    "B": ["C"],
    "C": ["A"],
    "D": ["C"]
}

scores = pagerank(graph)

print("PageRank Scores:")
for page, score in sorted(scores.items()):
    print(f"Page {page}: {score:.4f}")

print("\nPages ranked by importance:")
for page, score in sorted(
    scores.items(), key=lambda item: item[1], reverse=True
):
    print(f"{page}: {score:.4f}")
