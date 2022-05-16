def vlan_list_to_glob(vlans: list[int]) -> str:
    """
    Converts a VLAN ID list into a glob string commonly used by
    Cisco-like CLIs.
    :param vlans: The list of VLANs to convert to a glob.
    :return:
    """
    vlans.sort()
    in_range = False
    glob = ''
    for i, vid in enumerate(vlans):
        # Match on first element
        if i == 0:
            glob = str(vid)
        # Match if current element contiguous with the last
        elif vid != vlans[i - 1] + 1:
            # If we are in a range, then we have passed its end.  Append the last
            # element.
            if in_range:
                glob = glob + f'-{vlans[i - 1]}'
                in_range = False
            # Comma delimit and append current element.
            glob = glob + f',{vid}'
        # Element is contiguous with last, but we've hit the end of the list.
        elif i + 1 == len(vlans):
            in_range = False
            glob = glob + f'-{vid}'
        # If nothing above matched, then we are contiguous and therefore in
        # a range.
        else:
            in_range = True

    return glob


def glob_to_vlan_list(glob: str) -> list[int]:
    """
    Convert a Cisco-like CLI VLAN glob into a list of vlans.
    :param glob: The config glob.
    :return:
    """
    vlans = []
    for chunk in glob.split(','):
        bits = chunk.split('-')
        # If we two bits, then it's a range
        if len(bits) == 2:
            vlans += list(range(int(bits[0]), int(bits[1])+1))
        # Else it's a single number
        else:
            vlans.append(int(bits[0]))
    return vlans
