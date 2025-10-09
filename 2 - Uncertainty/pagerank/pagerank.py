import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # corpus:           Python dictionary mapping a page name to a set of all pages linked to by that page.
    # page:             String representing which page the random surfer is currently on.
    # damping_factor:   Floating point number representing the damping factor to be used when generating the probabilities.

    pages = corpus.keys()
    num_pages = len(pages)
    links = corpus[page]

    model = dict()

    if not links:
        for p in pages:
            model[p] = 1 / num_pages
        return model
    
    for p in pages:
        model[p] = (1 - damping_factor) / num_pages
        if p in links:
            model[p] += damping_factor / len(links)
    
    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    if n <= 0:
        # Degenerate case: uniform distribution
        return {p: 1 / len(corpus) for p in corpus}

    # Count visits
    visits = {p: 0 for p in corpus}

    # 1) pick a random start page and count it
    page = random.choice(list(corpus.keys()))
    visits[page] += 1

    # 2) perform n-1 transitions using the transition model
    for _ in range(1, n):
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(
            population=list(model.keys()),
            weights=list(model.values()),
            k=1
        )[0]
        visits[page] += 1

    # 3) normalize visit counts to probabilities
    total = sum(visits.values())
    return {p: visits[p] / total for p in visits}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    N = len(pages)
    d = damping_factor

    # Start uniformly
    ranks = {p: 1 / N for p in pages}

    # Precompute inbound links: who links to p
    inbound = {p: set() for p in pages}
    for q, outs in corpus.items():
        if outs:
            for p in outs:
                inbound[p].add(q)

    # Iteration until convergence
    EPS = 0.001
    while True:
        new_ranks = {}
        # Total rank mass on dangling pages (no outlinks)
        dangling_mass = sum(ranks[q] for q, outs in corpus.items() if len(outs) == 0)

        for p in pages:
            # Base random jump
            rank = (1 - d) / N

            # Distributed dangling mass contributes equally to all pages
            rank += d * dangling_mass / N

            # Normal link-based contributions
            link_sum = 0.0
            for q in inbound[p]:
                # (won't be 0 because inbound excludes dangling)
                Lq = len(corpus[q]) if len(corpus[q]) > 0 else N
                link_sum += ranks[q] / Lq
            rank += d * link_sum

            new_ranks[p] = rank

        # Check convergence (max absolute change below EPS for all pages)
        delta = max(abs(new_ranks[p] - ranks[p]) for p in pages)
        ranks = new_ranks
        if delta < EPS:
            break

    # Optional tiny normalization to fix rounding drift
    s = sum(ranks.values())
    if s != 0:
        ranks = {p: r / s for p, r in ranks.items()}
    return ranks


if __name__ == "__main__":
    main()
