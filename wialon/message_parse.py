# -*- coding: utf-8 -*-

import binascii
import struct


def parser(fmt, binary, offset=0):
    '''
    Unpack the string

    fmt      @see https://docs.python.org/2/library/struct.html#format-strings
    value    value to be formated
    offset   offset in bytes from begining
    '''
    parsed = struct.unpack_from(fmt, binary, offset)
    return parsed[0] if len(parsed) == 1 else parsed


def parse_packet(packet):
    '''
    Parse Wialon Retranslator v1.0 packet w/o first 4 bytes (packet size)
    '''

    msg = {
        'id': 0,
        'time': 0,
        'flags': 0,
        'params': {},
        'blocks': []
    }

    controller_id_size = packet.find(b'\x00')
    (msg['id'], msg['time'], msg['flags']) = parser('> %ds x i i' % controller_id_size, packet)

    data_blocks = packet[controller_id_size + 1 + 4 + 4:]

    while len(data_blocks):
        offset = 2 + 4 + 1 + 1
        name_size = data_blocks.find(b'\x00', offset) - offset
        (block_type, block_length, visible, data_type, name) = parser('> h i b b %ds' % (name_size), data_blocks)

        block = {'type': block_type, 'length': block_length, 'visibility': visible, 'data_type': data_type,
                 'name': name, 'data_block': data_blocks[offset + name_size + 1:block_length * 1 + 6]}

        # get block data

        v = ''
        if data_type == 1:
            pass
        if data_type == 2:
            if name == b'posinfo':
                v = {'lon': 0, 'lat': 0, 'h': 0, 's': 0, 'c': 0, 'sc': 0}
                (v['lon'], v['lat'], v['h']) = parser('d d d', block['data_block'])
                (v['s'], v['c'], v['sc']) = parser('> h h b', block['data_block'], 24)
        elif data_type == 3:
            v = parser('> i', block['data_block'])
        elif data_type == 4:
            v = parser('d', block['data_block'])
        elif data_type == 5:
            v = parser('> q', block['data_block'])

        msg['params'][name] = v

        msg['blocks'].append(block)

        data_blocks = data_blocks[block_length + 6:]

    return msg


if __name__ == '__main__':
    data = [
        '333533393736303133343435343835004B0BFB70000000030BBB000000270102706F73696E666F00A027AFDF5D9848403AC7253383DD4B400000000000805A40003601460B0BBB0000001200047077725F657874002B8716D9CE973B400BBB00000011010361766C5F696E707574730000000001',
        '73686d6900552d3f49000000070bbb000000270102706f73696e666f001f090e42538d3b40af8c20a82dfc4a400000000000000000006c0109ff0bbb0000000f000461646331000000000000ca21400bbb00000011010361766c5f696e7075747300000000240bbb00000012010361766c5f6f7574707574730000000037'
    ]
    for i in range(len(data)):
        print('\nParse packet: %s\n' % data[i])
        print(parse_packet(binascii.unhexlify(data[i])))
