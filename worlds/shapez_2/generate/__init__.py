from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from .. import Shapez2World

T = TypeVar("T")
R = TypeVar("R")


def reseed(func: R) -> R:
    def wrapper(world: "Shapez2World", *args, **kwargs) -> T:
        seed = world.random.getrandbits(64)
        world.random.seed(seed)
        ret = func(world, *args, **kwargs)
        world.random.seed(seed)
        return ret
    return wrapper
