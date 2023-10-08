def split_event(event) -> list[str]:
    print("splitting: ", event)
    return event.split(' at ')


def normalize_performer(p: str, performers: list[str]):
    for performer in performers:
        bench = ""
        for word in p.split(' '):
            if word in performer.split(' '):
                bench += word + ' '
            if bench.rstrip() == performer.rstrip():
                return performer

    return p


def normalize_event(event: str, performers: list[str]):
    e1, e2 = split_event(event)
    e1 = normalize_performer(e1, performers)
    e2 = normalize_performer(e2, performers)
    return e1 + ' at ' + e2
