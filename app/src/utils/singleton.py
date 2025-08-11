from typing import Any, Callable, Dict, TypeVar

T = TypeVar("T")


def singleton(class_: Callable[..., T]) -> Callable[..., T]:
    instance: Dict[Callable[..., T], T] = {}

    def getinstance(*args: Any, **kwargs: Any) -> T:
        if class_ not in instance:
            instance[class_] = class_(*args, **kwargs)
        return instance[class_]

    return getinstance
