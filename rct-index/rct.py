def compute_rct_score_per_method(
    relevance_1: int,
    total_responses: int,
    avg_cost: float,
    avg_time: float,
    min_time: float,
    max_time: float,
    ref_cost: float = 0.03,
    weights: tuple = (0.9, 0.1, 0.0)
) -> float:
    """
    Compute the RCT (Relevance–Cost–Time) score for a method.

    Parameters:
        relevance_1 (int): Number of relevant responses (score = 1).
        total_responses (int): Total number of responses evaluated.
        avg_cost (float): Average cost per query (e.g., in USD).
        avg_time (float): Average response time (seconds).
        min_time (float): Fastest response time observed (seconds).
        max_time (float): Slowest response time observed (seconds).
        ref_cost (float): Reference cost threshold for normalization.
        weights (tuple): Weights for relevance, cost, and time (sum should be ≤ 1.0).

    Returns:
        float: Final RCT score between 0.0 and 1.0.
    """
    if total_responses == 0:
        raise ValueError("total_responses must be greater than zero.")

    # Normalize metrics
    relevance_score = relevance_1 / total_responses
    cost_score = max(0.0, 1.0 - (avg_cost / ref_cost))
    time_score = (
        1.0 - ((avg_time - min_time) / (max_time - min_time))
        if max_time > min_time else 1.0
    )

    # Apply weights
    w1, w2, w3 = weights
    rct = w1 * relevance_score + w2 * cost_score + w3 * time_score
    return round(rct, 4)
