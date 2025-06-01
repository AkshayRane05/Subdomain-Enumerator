#!/usr/bin/env python3
"""
Subdomain Enumeration Tool
Educational project for cybersecurity reconnaissance
"""

import requests
import threading
import sys
import time
from urllib.parse import urlparse
import argparse
import urllib3

# Suppress SSL warnings for cleaner output
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SubdomainEnumerator:
    def __init__(self, domain, subdomain_file="subdomains.txt", output_file="discovered_subdomains.txt", threads=50, timeout=5):
        self.domain = domain
        self.subdomain_file = subdomain_file
        self.output_file = output_file
        self.max_threads = threads
        self.timeout = timeout
        self.discovered_subdomains = []
        self.lock = threading.Lock()
        self.total_subdomains = 0
        self.checked_count = 0

    def load_subdomains(self):
        """Load subdomains from file"""
        try:
            with open(self.subdomain_file, 'r') as f:
                subdomains = [line.strip() for line in f if line.strip()]
            self.total_subdomains = len(subdomains)
            print(
                f"[INFO] Loaded {self.total_subdomains} subdomains from {self.subdomain_file}")
            return subdomains
        except FileNotFoundError:
            print(f"[ERROR] File {self.subdomain_file} not found!")
            return []
        except Exception as e:
            print(f"[ERROR] Error reading file: {e}")
            return []

    def check_subdomain(self, subdomain):
        """Check if a subdomain is active"""
        # Update progress counter at the start
        with self.lock:
            self.checked_count += 1
            current_count = self.checked_count
            if current_count % 10 == 0 or current_count == 1:
                print(
                    f"[PROGRESS] Checking {current_count}/{self.total_subdomains} subdomains...")

        url = f"http://{subdomain}.{self.domain}"
        https_url = f"https://{subdomain}.{self.domain}"

        try:
            # Try HTTP first
            response = requests.get(
                url, timeout=self.timeout, allow_redirects=True)
            if response.status_code < 400:
                self.save_discovered_subdomain(
                    f"{subdomain}.{self.domain}", url, response.status_code)
                return True
        except requests.exceptions.RequestException:
            pass

        try:
            # Try HTTPS if HTTP fails
            response = requests.get(
                https_url, timeout=self.timeout, allow_redirects=True, verify=False)
            if response.status_code < 400:
                self.save_discovered_subdomain(
                    f"{subdomain}.{self.domain}", https_url, response.status_code)
                return True
        except requests.exceptions.RequestException:
            pass

        return False

    def save_discovered_subdomain(self, subdomain, url, status_code):
        """Save discovered subdomain to file and list"""
        with self.lock:
            discovery_info = f"{subdomain} - {url} (Status: {status_code})"
            self.discovered_subdomains.append(discovery_info)

            # Write to file immediately
            with open(self.output_file, 'a') as f:
                f.write(f"{discovery_info}\n")

            print(f"[FOUND] {discovery_info}")

    def worker(self, subdomain_queue):
        """Worker thread function"""
        while True:
            try:
                subdomain = subdomain_queue.pop(0)
                self.check_subdomain(subdomain)
            except IndexError:
                # Queue is empty
                break
            except Exception as e:
                print(f"[ERROR] Thread error: {e}")

    def enumerate(self):
        """Main enumeration function"""
        print(f"[INFO] Starting subdomain enumeration for {self.domain}")
        print(
            f"[INFO] Using {self.max_threads} threads with {self.timeout}s timeout")

        # Clear output file
        open(self.output_file, 'w').close()

        # Load subdomains
        subdomains = self.load_subdomains()
        if not subdomains:
            return

        # Create thread pool
        threads = []
        subdomain_queue = subdomains.copy()

        start_time = time.time()

        # Start threads
        for i in range(min(self.max_threads, len(subdomains))):
            t = threading.Thread(target=self.worker, args=(subdomain_queue,))
            t.daemon = True
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        end_time = time.time()

        # Print results
        print(f"\n[COMPLETE] Subdomain enumeration finished!")
        print(f"[STATS] Time taken: {end_time - start_time:.2f} seconds")
        print(f"[STATS] Total subdomains checked: {self.total_subdomains}")
        print(
            f"[STATS] Active subdomains found: {len(self.discovered_subdomains)}")
        print(f"[INFO] Results saved to {self.output_file}")

        if self.discovered_subdomains:
            print("\n[SUMMARY] Discovered subdomains:")
            for subdomain in self.discovered_subdomains:
                print(f"  → {subdomain}")


def create_sample_subdomain_file():
    """Create a sample subdomain file for testing"""
    common_subdomains = [
        "www", "mail", "ftp", "admin", "test", "dev", "staging", "api", "blog",
        "shop", "store", "news", "support", "help", "docs", "portal", "app",
        "mobile", "secure", "login", "auth", "cpanel", "webmail", "pop", "smtp",
        "imap", "ns1", "ns2", "dns", "mx", "exchange", "autodiscover", "remote",
        "vpn", "ssl", "secure", "static", "media", "cdn", "assets", "img",
        "images", "video", "downloads", "files", "upload", "backup", "old",
        "new", "beta", "alpha", "demo", "preview", "sandbox", "qa", "uat"
    ]

    try:
        with open("subdomains.txt", 'w') as f:
            for subdomain in common_subdomains:
                f.write(f"{subdomain}\n")
        print(
            f"[INFO] Created sample subdomain list with {len(common_subdomains)} entries")
    except Exception as e:
        print(f"[ERROR] Could not create subdomain file: {e}")


def main():
    parser = argparse.ArgumentParser(description="Subdomain Enumeration Tool")
    parser.add_argument("domain", nargs='?',
                        help="Target domain (e.g., example.com)")
    parser.add_argument(
        "-f", "--file", default="subdomains.txt", help="Subdomain list file")
    parser.add_argument(
        "-o", "--output", default="discovered_subdomains.txt", help="Output file")
    parser.add_argument("-t", "--threads", type=int,
                        default=50, help="Number of threads")
    parser.add_argument("--timeout", type=int, default=5,
                        help="Request timeout in seconds")
    parser.add_argument("--create-sample", action="store_true",
                        help="Create sample subdomain file")

    args = parser.parse_args()

    if args.create_sample:
        create_sample_subdomain_file()
        return

    # Validate domain
    if not args.domain:
        print("[ERROR] Please provide a domain name")
        print("Usage: python subdomain_enum.py <domain>")
        print("   or: python subdomain_enum.py --create-sample")
        return

    # Remove protocol if present
    domain = args.domain.replace(
        "http://", "").replace("https://", "").strip("/")

    # Initialize and run enumerator
    enumerator = SubdomainEnumerator(
        domain=domain,
        subdomain_file=args.file,
        output_file=args.output,
        threads=args.threads,
        timeout=args.timeout
    )

    try:
        enumerator.enumerate()
    except KeyboardInterrupt:
        print("\n[INFO] Enumeration interrupted by user")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")


if __name__ == "__main__":
    main()
