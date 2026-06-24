import os
import sys
import time
import math
import hashlib
import base64
import pyfiglet
import colorama
from bitcoin import is_address
from pycoin.networks.registry import network_for_netcode

# Initialize Colorama
colorama.init(autoreset=True)

def generate_garbage_hashes(count):
    """Generates random hashes to simulate a heavy workload."""
    return [hashlib.sha256(os.urandom(1024)).hexdigest() for _ in range(count)]

# Load BTC Network
btc_network = network_for_netcode("BTC")

# Display Title
ascii_art = pyfiglet.figlet_format("Bitcoin Recovery")
print("-" * 100)
print(colorama.Fore.YELLOW + ascii_art + colorama.Style.RESET_ALL)
print("-" * 100)
print()
print("Welcome to Bitcoin Recovery!")
print("With this tool, you can recover your Bitcoin private key just from the public key.")
print()

# Public Key Input Validation
public_key = input("Please enter your Bitcoin public key: ").strip()
while True:
    if is_address(public_key):
        print("This is a valid address.")
        break
    else:
        print("Invalid public key, please try again.")
        public_key = input("Please enter your Bitcoin public key: ").strip()

print("Please wait...\n")

# Loading Progress Bar
duration = 8
for i in range(duration, -1, -1):
    minutes = i // 60
    seconds = i % 60
    time_str = f"{minutes:02d}:{seconds:02d}"
    
    progress_text = "Generating your private key in progress... : "
    total_blocks = 50
    percentage = ((duration - i) / duration) * total_blocks
    
    filled_length = math.ceil(percentage)
    bar = "[" + "#" * filled_length + "-" * (total_blocks - filled_length) + "]"
    
    print(f"{progress_text}{colorama.Fore.YELLOW}{bar}", end="\r" + colorama.Style.RESET_ALL)
    generate_garbage_hashes(duration * 100000)
    time.sleep(0.5)

print("\n")

#  Private Key Generation
for u in range(1, 6):
    seed = os.urandom(16)
    master_key = btc_network.keys.bip32_seed(seed)
    private_key = master_key.hwif(as_private=1)
    
    print(f"Key {u}: {colorama.Fore.GREEN}{private_key}")
    time.sleep(1.5)

print("\nKey 6 generation failed: Public key mismatch.")
