from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class TrackEntry:
    date: datetime
    type: int
    metadata: dict
    id: str = field(default_factory=lambda: str(uuid.uuid4()))  # Auto-generate unique ID
