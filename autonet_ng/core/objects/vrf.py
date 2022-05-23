from dataclasses import dataclass, field
from typing import List, Optional

from autonet_ng.core import exceptions as exc
from autonet_ng.core.objects import validators as v


@dataclass
class VRF(object):
    name: Optional[str] = field(default=None)
    ipv4: Optional[bool] = field(default=None)
    ipv6: Optional[bool] = field(default=None)
    import_targets: Optional[List[str]] = field(default=None)
    export_targets: Optional[List[str]] = field(default=None)
    route_distinguisher: Optional[str] = field(default=None)

    def __post_init__(self):
        for rt_set in [self.import_targets, self.export_targets]:
            if rt_set is not None:
                for rt in rt_set:
                    if not v.is_route_target(rt):
                        raise exc.RequestValueError('import_targets', rt)
            if self.route_distinguisher is not None \
                    and not v.is_route_distinguisher(self.route_distinguisher):
                raise exc.RequestValueError('route_distinguisher', self.route_distinguisher)

        v.validate(self)
