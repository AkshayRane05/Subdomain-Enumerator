# Subdomain Enumeration Tool

A fast, multithreaded Python tool for automated subdomain discovery during cybersecurity reconnaissance. This educational project demonstrates the fundamentals of subdomain enumeration, HTTP requests, and concurrent programming.

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

## 🔍 Overview

Subdomain enumeration is a crucial step in the reconnaissance phase of cybersecurity assessments. This tool automates the process of discovering active subdomains by testing common subdomain patterns against a target domain using HTTP/HTTPS requests.

### Key Features

- **🚀 Fast Multithreading**: Concurrent subdomain checking with configurable thread count
- **🔒 Dual Protocol Support**: Tests both HTTP and HTTPS endpoints
- **📊 Real-time Progress**: Live progress tracking and statistics
- **💾 File I/O Operations**: Reads wordlists and saves results automatically
- **🛡️ Error Handling**: Robust handling of network timeouts and connection errors
- **⚙️ Customizable**: Flexible configuration options for different use cases

## 🛠️ Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AkshayRane05/subdomain-enumeration-tool.git
   cd subdomain-enumeration-tool
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv myenv

   # Windows
   myenv\Scripts\activate

   # Linux/MacOS
   source myenv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install requests
   ```

## 🚀 Quick Start

### 1. Create a Subdomain Wordlist

Generate a sample wordlist with common subdomains:

```bash
python subdomain_enum.py --create-sample
```

This creates a `subdomains.txt` file with 56 common subdomain patterns.

### 2. Run Basic Enumeration

```bash
python subdomain_enum.py example.com
```

### 3. View Results

Results are automatically saved to `discovered_subdomains.txt` and displayed in the terminal:

```
[INFO] Starting subdomain enumeration for example.com
[PROGRESS] Checking 1/56 subdomains...
[FOUND] www.example.com - http://www.example.com (Status: 200)
[FOUND] mail.example.com - https://mail.example.com (Status: 200)
[COMPLETE] Subdomain enumeration finished!
[STATS] Active subdomains found: 2
```

## 📖 Usage

### Command Line Options

```bash
python subdomain_enum.py [OPTIONS] <domain>
```

| Option            | Description                    | Default                     |
| ----------------- | ------------------------------ | --------------------------- |
| `domain`          | Target domain to enumerate     | Required                    |
| `-f, --file`      | Custom subdomain wordlist file | `subdomains.txt`            |
| `-o, --output`    | Output file for results        | `discovered_subdomains.txt` |
| `-t, --threads`   | Number of concurrent threads   | `50`                        |
| `--timeout`       | Request timeout in seconds     | `5`                         |
| `--create-sample` | Generate sample wordlist       | -                           |
| `-h, --help`      | Show help message              | -                           |

### Examples

**Basic usage**:

```bash
python subdomain_enum.py google.com
```

**Custom wordlist and output**:

```bash
python subdomain_enum.py target.com -f custom_subs.txt -o results.txt
```

**High-speed scanning**:

```bash
python subdomain_enum.py target.com -t 100 --timeout 3
```

**Generate wordlist only**:

```bash
python subdomain_enum.py --create-sample
```

## 📁 File Structure

```
subdomain-enumeration-tool/
├── subdomain_enum.py          # Main enumeration script
├── subdomains.txt             # Default wordlist (generated)
├── discovered_subdomains.txt  # Results output (generated)
├── README.md                  # This file
└── requirements.txt           # Python dependencies
```

## 🎯 How It Works

### Architecture Overview

1. **Input Processing**: Loads subdomain wordlist from file
2. **Thread Pool Creation**: Spawns configurable number of worker threads
3. **HTTP Testing**: Each thread tests subdomains with HTTP/HTTPS requests
4. **Result Collection**: Thread-safe collection and storage of active subdomains
5. **Output Generation**: Real-time display and file output of results

### Technical Implementation

- **Multithreading**: Uses Python's `threading` module for concurrent execution
- **HTTP Requests**: Leverages the `requests` library for web communication
- **Thread Synchronization**: Implements locks to prevent race conditions
- **Error Handling**: Graceful handling of network timeouts and connection errors

## 📊 Sample Output

```
[INFO] Starting subdomain enumeration for example.com
[INFO] Using 50 threads with 5s timeout
[INFO] Loaded 56 subdomains from subdomains.txt
[PROGRESS] Checking 10/56 subdomains...
[FOUND] www.example.com - http://www.example.com (Status: 200)
[FOUND] api.example.com - https://api.example.com (Status: 200)
[PROGRESS] Checking 20/56 subdomains...
[FOUND] mail.example.com - https://mail.example.com (Status: 302)
[COMPLETE] Subdomain enumeration finished!
[STATS] Time taken: 4.23 seconds
[STATS] Total subdomains checked: 56
[STATS] Active subdomains found: 3
[INFO] Results saved to discovered_subdomains.txt
```

## 🔧 Customization

### Creating Custom Wordlists

Create your own `subdomains.txt` with one subdomain per line:

```
admin
api
blog
dev
staging
test
www
```

### Modifying Detection Logic

The tool considers subdomains "active" if they return HTTP status codes < 400. You can modify the `check_subdomain()` function to customize this behavior.

## ⚡ Performance Tips

- **Thread Count**: Start with 50 threads; increase gradually based on your network
- **Timeout**: Use shorter timeouts (2-3s) for faster scanning
- **Wordlist Size**: Larger wordlists take more time but find more subdomains
- **Target Selection**: Some domains have rate limiting; adjust threads accordingly

## 🛡️ Ethical Usage

### Important Legal Notice

This tool is designed for **educational purposes** and **authorized security testing** only.

**✅ Acceptable Use:**

- Testing domains you own
- Authorized penetration testing
- Educational cybersecurity learning
- Security research with permission

**❌ Prohibited Use:**

- Scanning domains without permission
- Malicious reconnaissance
- Unauthorized testing
- Any illegal activities

**Always ensure you have explicit permission before testing any domain you don't own.**

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Ideas for Contributions

- DNS resolution validation
- Additional output formats (JSON, CSV)
- Integration with other recon tools
- GUI interface
- Additional wordlists
- Performance optimizations

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Educational Value

This project teaches:

- **Network Programming**: HTTP requests and response handling
- **Concurrent Programming**: Multithreading and synchronization
- **File Operations**: Reading wordlists and writing results
- **Error Handling**: Network timeout and exception management
- **Cybersecurity Concepts**: Reconnaissance and subdomain enumeration

## 🔗 Related Tools

- [Sublist3r](https://github.com/aboul3la/Sublist3r) - Python subdomain enumeration tool
- [Amass](https://github.com/OWASP/Amass) - Advanced subdomain enumeration
- [Subfinder](https://github.com/projectdiscovery/subfinder) - Fast passive subdomain enumeration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/AkshayRane05/subdomain-enumeration-tool/issues) page
2. Create a new issue with detailed information
3. Include your Python version and operating system

## 🏆 Acknowledgments

- Inspired by common cybersecurity reconnaissance techniques
- Built for educational purposes in ethical hacking courses
- Thanks to the Python community for excellent networking libraries

---

**⭐ Star this repository if you found it helpful!**

_Remember: With great power comes great responsibility. Use this tool ethically and legally._
