import csv
import logging
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException
import os

# Configure logging
logging.basicConfig(filename='script.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Function to read CSV file
def read_csv(file):
    devices = []
    try:
        with open(file, mode='r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                devices.append(row)
    except FileNotFoundError as e:
        logging.error(f"CSV file not found: {e}")
        raise
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
        raise
    return devices

# Function to collect BGP configuration from each device
def collect_bgp_config(device):
    try:
        connection = ConnectHandler(
            device_type=device['device_type'],
            host=device['ip_address'],
            username=device['username'],
            password=device['password']
        )
        bgp_output = connection.send_command('show running-config router bgp')
        with open(f"{device['hostname']}_bgp.txt", 'w') as file:
            file.write(bgp_output)
        connection.disconnect()
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        logging.error(f"Connection failure for {device['hostname']}: {e}")
    except Exception as e:
        logging.error(f"Failed to collect BGP config for {device['hostname']}: {e}")

# Function to check each best practice
def check_best_practice(pattern, bgp_config, recommendation):
    return pattern not in bgp_config, recommendation

# Function to compare BGP configuration with best practices
def compare_bgp_config(device):
    recommendations = []
    try:
        with open(f"{device['hostname']}_bgp.txt", 'r') as file:
            bgp_config = file.read()

        checks = [
            ('synchronization', "no synchronization"),
            ('log-neighbor-changes', "log neighbor changes"),
            ('no auto-summary', "no auto-summary"),
            ('remove-private-AS', "remove private AS"),
            ('maximum-prefix', "set maximum-prefix limit"),
            ('router-id', "use loopback for router-id"),
            ('next-hop-self', "set next-hop-self for iBGP neighbors"),
            ('ttl-security', "enable ttl-security check"),
            ('password', "enable neighbor authentication"),
            ('filter-list', "enable neighbor access or filter list"),
        ]

        for pattern, recommendation in checks:
            practice_needed, practice_recommendation = check_best_practice(pattern, bgp_config, recommendation)
            if practice_needed:
                recommendations.append(practice_recommendation)

    except FileNotFoundError as e:
        logging.error(f"Configuration file not found for {device['hostname']}: {e}")
    except Exception as e:
        logging.error(f"Error comparing BGP config for {device['hostname']}: {e}")

    return recommendations

# Function to generate and save recommendations
def generate_recommendations(differences, device):
    try:
        with open('recommendations.txt', 'a') as file:
            file.write(f"Recommendations for {device['hostname']}:\n")
            for rec in differences:
                file.write(f"{rec}\n")
            file.write("\n")
    except Exception as e:
        logging.error(f"Failed to write recommendations for {device['hostname']}: {e}")

# Main execution
if __name__ == "__main__":
    # Example usage of environment variable (for demonstration only)
    csv_file = os.getenv('ROUTERS_CSV_FILE', 'routers.csv')  # CSV file path could be an env variable

    devices = read_csv(csv_file)

    for device in devices:
        collect_bgp_config(device)
        differences = compare_bgp_config(device)
        generate_recommendations(differences, device)

    logging.info("Script execution completed.")