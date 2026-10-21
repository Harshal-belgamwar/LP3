
import xml.etree.ElementTree as ET


def parse_xml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    graph = {}
    topics = {}

    # Parse pages and their outgoing links
    for page in root.findall("page"):
        page_id = page.get("id")
        topics[page_id] = page.get("topic", "unknown")

        graph[page_id] = [
            link.text.strip()
            for link in page.findall("link")
            if link.text and link.text.strip()
        ]

    # Keep only links pointing to pages in this XML
    for page in graph:
        graph[page] = [
            link for link in graph[page] if link in graph
        ]

    return graph, topics


def topic_pagerank(graph, topics, target_topic,
                   damping=0.85, iterations=100):
    pages = list(graph.keys())
    n = len(pages)

    if n == 0:
        return {}

    # Give higher teleportation probability to topic pages
    relevant = [
        page for page in pages
        if topics[page].lower() == target_topic.lower()
    ]

    if not relevant:
        raise ValueError("No pages found for the requested topic.")

    personalization = {
        page: (1 / len(relevant) if page in relevant else 0)
        for page in pages
    }

    rank = {page: 1 / n for page in pages}

    for _ in range(iterations):
        new_rank = {
            page: (1 - damping) * personalization[page]
            for page in pages
        }

        dangling_rank = sum(
            rank[page] for page in pages if not graph[page]
        )

        for page in pages:
            # Redistribute rank from pages without outgoing links
            for target in pages:
                new_rank[target] += (
                    damping * dangling_rank * personalization[target]
                ) / 1

            # Distribute rank through outgoing links
            if graph[page]:
                share = damping * rank[page] / len(graph[page])

                for target in graph[page]:
                    new_rank[target] += share

        rank = new_rank

    return rank


if __name__ == "__main__":
    graph, topics = parse_xml("webdata.xml")

    print("Web Graph:")
    for page, links in graph.items():
        print(f"{page} -> {links}")

    target_topic = input(
        "\nEnter topic (sports/technology): "
    ).strip()

    scores = topic_pagerank(graph, topics, target_topic)

    print(f"\nTopic-specific PageRank for '{target_topic}':")
    for page, score in sorted(
        scores.items(), key=lambda item: item[1], reverse=True
    ):
        print(f"Page {page}: {score:.4f} (Topic: {topics[page]})")
