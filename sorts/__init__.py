from .merge_sort import merge_sort
from .quick_sort import quick_sort
from .tree_sort import tree_sort

SORTS = {
    "merge": merge_sort,
    "quick": quick_sort,
    "tree": tree_sort,
}

STABLE = {"merge", "tree"}
