import math


def paginate(page, perPage, querySet, queryList=[], orderBy=["-id"]):
    offset = (int(page) - 1) * perPage
    query = querySet.filter(*queryList).order_by(*orderBy)
    data = query[offset : offset + perPage]
    total = query.count()
    lastPage = 1 if int(total / perPage) == 0 else math.ceil(total / perPage)
    nextPage = page + 1 if (offset + perPage) < total else None

    if page > 1 and (page - 1) < lastPage:
        previous = page - 1
    else:
        previous = None

    return {
        "current": page,
        "next": nextPage,
        "previous": previous,
        "last": lastPage,
        "total": total,
        "data": data,
    }
