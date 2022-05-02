import time


def difference_time(start_t: float, need_t: float) -> float:

    dif_time = time.time()-start_t-need_t
    return dif_time
