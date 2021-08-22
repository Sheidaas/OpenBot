import eXLib
import chr


def parse_instances_list():
    instances_list = []
    for vid in eXLib.InstancesList:
        chr.SelectInstance(vid)
        x, y, z = chr.GetPixelPosition(vid)
        _id = chr.GetRace()
        _type = chr.GetInstanceType(vid)
        instances_list.append({
            'vid': vid,
            'id': _id,
            'x': x,
            'y': y,
            'type': _type
        })
    return instances_list
