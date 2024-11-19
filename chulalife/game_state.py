from dataclasses import dataclass
from .logger import get_logger
from .setting import initial_hearts

logger = get_logger(__name__)


@dataclass
class game_state:
    hearts = initial_hearts
