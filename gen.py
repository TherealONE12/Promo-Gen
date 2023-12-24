import requests
import string
import random
import threading
import time
import ctypes
import os
import uuid
from random import choice

os.system('cls' if os.name == 'nt' else 'clear')

class counter:
    count = 0

red = '\x1b[31m(-)\x1b[0m'
blue = '\x1b[34m(+)\x1b[0m'
green = '\x1b[32m(+)\x1b[0m'
yellow = '\x1b[33m(!)\x1b[0m'

def get_timestamp():
    time_idk = time.strftime('%H:%M:%S')
    timestamp = f'[\x1b[90m{time_idk}\x1b[0m]'
    return timestamp

def gen(proxy, webhook_url=None, generate_infinite=False, num_codes=None):
    codes_to_generate = 9999999 if generate_infinite else num_codes

    start_time = time.time()

    if webhook_url:
        send_to_webhook(webhook_url, "Hi! Thanks for using my Private Tool! Please wait until the setup is finished. Then, the Promos will come HERE through")

    for _ in range(codes_to_generate):
        url = "https://api.discord.gx.games/v1/direct-fulfillment"
        headers = {
            "Content-Type": "application/json",
            "Sec-Ch-Ua": '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
        }

        data = {
            "partnerUserId": str(uuid.uuid4())
        }

        try:
            if proxy is not None:
                credentials, host = proxy.split('@')
                user, password = credentials.split(':')
                host, port = host.split(':')
                formatted_proxy = f"http://{user}:{password}@{host}:{port}"
                response = requests.post(url, json=data, headers=headers, proxies={'http': formatted_proxy, 'https': formatted_proxy}, timeout=5)
            else:
                response = requests.post(url, json=data, headers=headers, timeout=5)

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    counter.count += 1
                    ctypes.windll.kernel32.SetConsoleTitleW(
                            f"Opera Gx Promo Gen | Made With <3 By Joy"
                            f" | Generated : {counter.count}")
                    link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"
                    if webhook_url:
                        send_to_webhook(webhook_url, f"Promo Generated! : {link}")
                    with open("promos.txt", "a") as f:
                        f.write(f"{link}\n")
                    print(f"{get_timestamp()} {green} Generated Promo Link : {link}")
            elif response.status_code == 429:
                print(f"{get_timestamp()} {yellow} You are being rate-limited!")
            else:
                print(f"{get_timestamp()} {red} Request failed : {response.status_code}")
        except Exception as e:
            print(f"{get_timestamp()} {red} Request Failed : {e}")

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"\nTime taken: {time_taken:.2f} seconds")
    print(f"Number of codes generated: {counter.count}")
    print(f"Settings: Threads={threading.active_count()}, Infinite={generate_infinite}, Num Codes={num_codes}")

    if webhook_url:
        summary_message = (
            f"The Generator is Up! All of your coodes are being generated in a second. Please be patient. "
            f"Also note our \0REFUND POLICY allows refunds UP TO 24h Later! So please say it soon when your Promos don't work/They are not enough!"
            f"(Please provide also proof then.)"
            f"You have now 24h to report any not OK codes! If everything is fine, please vouch me! THX <3"
        )
        send_to_webhook(webhook_url, summary_message)

def send_to_webhook(webhook_url, message):
    payload = {"content": message}
    requests.post(webhook_url, json=payload, timeout=5)

def main():
    num_threads = int(input(f"{get_timestamp()} {blue} Enter Number Of Threads : "))
    destination_option = int(input(f"{get_timestamp()} {blue} Choose Destination: Webhook (1), File (2), Both (3) : "))
    
    webhook_url = None
    if destination_option in [1, 3]:
        webhook_url = input(f"{get_timestamp()} {blue} Input your Discord Webhook URL: ")

    generate_infinite = False
    num_codes = None

    if destination_option in [1, 2, 3]:
        generation_option = int(input(f"{get_timestamp()} {blue} Choose Generation Option: Infinite (1), Generate x Codes (2) : "))
        if generation_option == 2:
            num_codes = get_positive_int("Enter the number of codes to generate: ")

    with open("proxies.txt") as f:
        proxies = f.read().splitlines()

    threads = []
    for i in range(num_threads):
        proxy = choice(proxies) if proxies else None
        thread = threading.Thread(target=gen, args=(proxy, webhook_url, generate_infinite, num_codes))
        threads.append(thread)

    for thread in threads:
        thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for thread in threads:
            thread.join()

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("Please enter a non-negative integer.")
        except ValueError:
            print("Please enter a valid integer.")

if __name__ == "__main__":
    main()
