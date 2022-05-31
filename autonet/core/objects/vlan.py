from dataclasses import dataclass, field
from typing import Optional

from autonet.core.objects import validators as v


@dataclass
class VLAN(object):
    id: int = field(default=None)
    name: Optional[str] = field(default=None)
    bridge_domain: Optional[str] = field(default=None)
    admin_enabled: Optional[bool] = field(default=None)

    def __post_init__(self):
        v.validate(self)
