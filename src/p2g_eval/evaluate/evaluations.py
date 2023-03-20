import numpy as np
from geopy.distance import distance


def evaluate_stop_distance(lat1, lon1, lat2, lon2) -> float:
    """ Return the distance between the given locations in meter. """
    return distance((lat1, lon1), (lat2, lon2)).m


v_evaluate_stop_distance = np.vectorize(evaluate_stop_distance)


