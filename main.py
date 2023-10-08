import ipaddress
import platform
import subprocess
import random
from art import text2art
from colorama import Fore
import dns
from dns import resolver
from concurrent.futures import ThreadPoolExecutor


def clear():
    if platform.system() == "Windows":
        subprocess.call('cls', shell=True)
    else:
        subprocess.call('clear', shell=True)


def ansci_banner3():
    bad_colors = ['BLACK', 'WHITE', 'LIGHTBLACK_EX', 'RESET']
    codes = vars(Fore)
    colors = [codes[color] for color in codes if color not in bad_colors]
    colored_chars = [random.choice(colors) + text2art("EmperorsTools\nDomain2IpSimple", "random")]
    return ''.join(colored_chars)


class DOMAIN2IP:

    @staticmethod
    def schrijven(ip: str) -> bool:
        with open("DOMAIN2IPS.txt", "a") as schrijf:
            schrijf.write(ip + "\n")
        print(f"GOOD_IP_FOUND: {ip}")
        return True

    @staticmethod
    def is_valid_ip(value: str) -> bool:
        try:
            ipaddress.ip_address(value)
            return True
        except (ipaddress.AddressValueError, ValueError):
            return False

    @staticmethod
    def get_host(url: str) -> str:
        if "://" in url:
            url = url.split("://")[1]
        if ":" in url:
            url = url.split(":")[0]
        if "/" in url:
            url = url.split("/")[0]
        return url

    @staticmethod
    def resolve_domain(domain, timeout=4) -> str | bool:
        resolv = dns.resolver.Resolver()
        resolver.lifetime = timeout
        resolver.timeout = timeout
        try:
            answers = resolv.resolve(domain)
            ip_addresses = [str(answer) for answer in answers][0]
            return ip_addresses
        except dns.exception.Timeout:
            return False
        except dns.exception.DNSException:
            return False

    def ip_from_domain(self, url: str) -> bool:
        url = url.strip()
        host_to_use = self.get_host(url=url)
        if self.is_valid_ip(value=host_to_use) is True:
            self.schrijven(ip=host_to_use)
            return False
        ip = self.resolve_domain(domain=host_to_use)
        if ip is False:
            print(f"BAD_HOST: {host_to_use}")
            return False
        else:
            self.schrijven(ip=ip)
            return True


#
if __name__ == '__main__':
    clear()
    print(ansci_banner3())
    data_name = input("Your Domains or Urls List .txt: ")
    domain2ip = DOMAIN2IP()
    with open(data_name, "r") as data_file:
        data = data_file.read().strip().split("\n")
    with ThreadPoolExecutor(max_workers=100) as start_up:
        start_up.map(domain2ip.ip_from_domain, data)
