from dataclasses import dataclass
from .logger import get_logger

logger = get_logger(__name__)


@dataclass
class game_state:
    hearts = 3
