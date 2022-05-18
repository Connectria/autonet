from dataclasses import dataclass, field
from typing import List, Optional, Union

import autonet_ng.core.exceptions as exc
from autonet_ng.core.objects import validators as v


@dataclass
class VXLAN(object):
    id: int = field(default=None)
    source_address: str = field(default=None)
    layer: int = field(default=None)
    import_targets: Optional[List[str]] = field(default=None)
    export_targets: Optional[List[str]] = field(default=None)
    route_distinguisher: str = field(default=None)
    bound_object_id: Optional[Union[str, int]] = field(default=None)

    def __post_init__(self):
        if self.source_address:
            if not v.is_ipv4_address(self.source_address):
                raise exc.RequestValueError('source_address', self.source_address)
        if self.layer:
            valid_layers = [2, 3]
            if self.layer not in valid_layers:
                raise exc.RequestValueError('layer', self.layer, valid_layers)
            # Layer 2 VNIs get bound to VLANs.  The VLAN may be assigned as a
            # string.  We'll verify it's numeric here, and cast to int as
            # needed.
            if self.layer == 2 and self.bound_object_id:
                if not str(self.bound_object_id).isdigit():
                    raise exc.RequestValueError('bound_object_id', self.bound_object_id)
                self.bound_object_id = int(self.bound_object_id)
            # Layer 3 VNIs get bound to a VRF, which maybe has a numeric name, but
            # needs to be cast to a string either way.
            if self.layer == 3 and self.bound_object_id:
                self.bound_object_id = str(self.bound_object_id)
            # Make sure the route-targets are actual route-targets, and same with the
            # route distinguisher.
            for rt_set in [self.import_targets, self.export_targets]:
                if rt_set is not None:
                    for rt in rt_set:
                        if not v.is_route_target(rt):
                            raise exc.RequestValueError('import_targets', rt)
            if self.route_distinguisher is not None \
                    and not v.is_route_distinguisher(self.route_distinguisher):
                raise exc.RequestValueError('route_distinguisher', self.route_distinguisher)

        v.validate(self)
