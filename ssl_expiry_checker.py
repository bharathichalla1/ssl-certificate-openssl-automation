import datetime
import ssl
import socket

# Function to fetch the expiry date of SSL certificate for a domain
def get_ssl_expiry_date(domain):
    try:
        # Create a secure SSL context
        context = ssl.create_default_context()
        # Establish SSL connection
        with context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=domain) as conn:
            conn.connect((domain, 443))
            cert = conn.getpeercert()

        # Extract the expiry date from the certificate
        expiry_date_str = cert['notAfter']
        expiry_date = datetime.datetime.strptime(expiry_date_str, "%b %d %H:%M:%S %Y GMT")
        return expiry_date
    except Exception as e:
        print(f"Error fetching SSL certificate for {domain}: {e}")
        return None

# Function to check SSL expiry for multiple domains
def check_expiry_for_domains(domains):
    for domain in domains:
        print(f"Checking SSL certificate expiry for domain: {domain}")
        expiry_date = get_ssl_expiry_date(domain)
        
        if expiry_date:
            print(f"Expiry Date for {domain}: {expiry_date}")
            
            if expiry_date < datetime.datetime.now():
                print(f"Warning: SSL certificate for {domain} has expired!")
            elif expiry_date < datetime.datetime.now() + datetime.timedelta(days=30):  # Expiring soon (within 30 days)
                print(f"Warning: SSL certificate for {domain} is expiring soon!")
            else:
                print(f"SSL certificate for {domain} is valid until {expiry_date}")
        else:
            print(f"Failed to retrieve expiry date for {domain}")

# List of domains to check
domains_to_check = ["example.com", "google.com", "github.com"]  # Add more domains as needed

# Run the SSL expiry check for the domains
check_expiry_for_domains(domains_to_check) 
