
## Explanation

This demonstration showcases an **Internationalized Domain Name (IDN)** Homograph Attack by simulating a phishing attack using a website similar to the Algerian e-commerce website ouedkniss.com, where attackers use visually similar characters from different languages (like Japanese characters) to create deceptive domain names that look legitimate but actually point to malicious websites.

This demo has been inspired from this Hacker News article ( [article link](https://cybersecuritynews.com/phishing-attack-uses-japanese-character/) ).

**The Risk**: Users can't distinguish between legitimate domains and fake ones because they look identical to the human eye. For example, `www.account-booking.com` vs `www.accοunt-bοoking.com` (using Greek omicrons instead of Latin 'o').

As a result malicious actors can steal credentials , and upload malwares in your host.

**Real-World Impact**: In 2017, a security researcher registered domains like `apple.com` using Cyrillic characters that were visually identical, demonstrating how easily users could be tricked.

## Requirements

- Python 3.x
- `idna` library (`pip install idna`)
- Local web server (Python's `http.server` or similar)
- Access to edit system hosts file (`/etc/hosts` on Linux/Mac, `C:\Windows\System32\drivers\etc\hosts` on Windows)

## Tutorial

### Step 1: Create the Malicious Domain

```python
import idna

# Create a domain that looks legitimate but contains special characters
malicious_domain = "account.ouedkniss.comんdetailんrestric-access.www-account-ouedkniss.com"

# Encode it for DNS/hosts file
encoded_domain = idna.encode(malicious_domain).decode('ascii')
print(f"Add this to your hosts file: 127.0.0.1 {encoded_domain}")
```

### Step 2: Configure Local DNS

Add the encoded domain to your hosts file:

**Linux/Mac:**
```bash
echo "127.0.0.1 account.ouedkniss.xn--comdetailrestric-access-ge5vga.www-account-ouedkniss.com" | sudo tee -a /etc/hosts
```

**Windows (Run as Administrator):**
```cmd
echo 127.0.0.1 account.ouedkniss.xn--comdetailrestric-access-ge5vga.www-account-ouedkniss.com >> C:\Windows\System32\drivers\etc\hosts
```

### Step 3: Set Up Fake Login Page

download the  `index.html` file :


### Step 4: Start Local Web Server

Start the local web server at the same directoy as the `index.html` file

```bash
python3 -m http.server 80
```

### Step 5: Demonstrate the Attack

1. Open browser and visit: `https://account.ouedkniss.comんdetailんrestric-access.www-account-ouedkniss.com`
2. Show how the URL looks legitimate in the address bar
3. Demonstrate how users would enter their credentials
4. Show the captured data in the `credentials.json` file

## Automation Script

use the  `setup_attack.py` :
```bash
sudo python3 setup_attack.py
```


### Mitigation Strategies

1. **For Users**:
   - Always check the full URL in address bar
   - Use password managers that detect domain changes
   - Enable two-factor authentication
   - Bookmark important sites instead of typing URLs
   - Be careful of phishing emails.

2. **For Organizations**:
   - Implement IDN display policies in browsers
   - Use HTTPS and check certificates carefully
   - Educate employees about homograph attacks.

3. **Technical Defenses**:
   - Browser plugins that highlight suspicious domains
   - Email filters that flag potentially malicious links

