import re

from ipaddress import ip_address

from autonet.core.objects import validators as v


def parse_esi(esi: str) -> dict:
    """
    Parses an ESI string returns a dictionary containing information
    on the ESI type and its component parts.  Component parts may vary
    depending on the ESI type as detailed below.  See
    `RFC 7432 <https://datatracker.ietf.org/doc/html/rfc7432#section-5>`_
    for more details.

    .. code-block: python
        :caption: Type 0

        {
            'type': 0,
            'id': '23:45:67:89:1a:bc:de:f0:12'
        }

    .. code-block: python
        :caption: Type 1

        {
            'type': 1,
            'lacp_system_mac': '23:45:67:89:1a:bc',
            'lacp_port_key': 15
        }

    .. code-block: python
        :caption: Type 2

        {
            'type': 2,
            'root_bridge': '23:45:67:89:1a:bc',
            'root_priority': 8192
        }

    .. code-block: python
        :caption: Type 3

        {
            'type': 3,
            'system_mac': '23:45:67:89:1a:bc',
            'local_discriminator': 1
        }

    .. code-block: python
        :caption: Type 4

        {
            'type': 4,
            'router_id': '198.18.0.1',
            'local_discriminator': 1
        }

    .. code-block: python
        :caption: Type 5

        {
            'type': 5,
            'asn': 65500,
            'local_discriminator': 1
        }

    :param esi: The ESI to be parsed.  The ESI must be a string with
        each byte delimited by either :code:`:`, :code:`.`, :code:`_`,
        or :code:`-`.
    :return:
    """
    if not v.is_esi(esi):
        raise Exception(f"'{esi}' does not appear to be formatted correctly.")
    octets = bytes.fromhex(re.sub(r'[-_.:]', '', esi))
    esi_type = octets[0]
    if esi_type == 0:
        esi_data = {
            'type': 0,
            'id': octets[1:].hex(':')
        }
    elif esi_type == 1:
        esi_data = {
            'lacp_system_mac': octets[1:7].hex(':'),
            'lacp_port_key': int.from_bytes(octets[7:9], 'big', signed=False)
        }
    elif esi_type == 2:
        esi_data = {
            'root_bridge': octets[1:7].hex(':'),
            'root_priority': int.from_bytes(octets[7:9], 'big', signed=False)
        }
    elif esi_type == 3:
        esi_data = {
            'system_mac': octets[1:7].hex(':'),
            'local_discriminator': int.from_bytes(octets[7:], 'big',
                                                  signed=False)
        }
    elif esi_type == 4:
        esi_data = {
            'router_id': str(ip_address(octets[1:5])),
            'local_discriminator': int.from_bytes(octets[5:9], 'big',
                                                  signed=False)
        }
    elif esi_type == 5:
        esi_data = {
            'asn': int.from_bytes(octets[1:5], 'big', signed=False),
            'local_discriminator': int.from_bytes(octets[5:9], 'big',
                                                  signed=False)
        }
    else:
        esi_data = {}

    return {**{'type': esi_type}, **esi_data}
