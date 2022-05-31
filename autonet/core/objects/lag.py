import re

from dataclasses import dataclass, field
from typing import List, Optional

from autonet.core import exceptions as exc
from autonet.core.objects import validators as v


@dataclass
class LAG(object):
    name: str = field(default=None)
    members: Optional[List[str]] = field(default_factory=List)
    evpn_esi: Optional[str] = field(default=None)

    def __post_init__(self):
        # 'auto' is a valid esi option for platforms that support type3 ESI.
        # Drivers that do not support Type3 ESI need to report upstream as such.
        if self.evpn_esi and self.evpn_esi != 'auto':
            if not v.is_esi(self.evpn_esi):
                raise exc.RequestValueError('evpn_esi', self.evpn_esi)
            # replace common separators, cast to bytes then cast
            # back to a well formatted string.
            self.evpn_esi = bytes.fromhex(re.sub(r'[-_.:]', '', self.evpn_esi)).hex(':')
        v.validate(self)
