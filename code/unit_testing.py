import healthcheck
import unittest
import app
import os, csv, ipaddress, json, subprocess

# Function to valid if IPv4 or IPv6 address is valid using ipaddress python module
def validate_ip_addresses(ip_dict):
    for host, interfaces in ip_dict.items():
        for interface_type, addresses in interfaces.items():
            for ip_type, ip_list in addresses.items():
                for ip in ip_list:
                    try:
                        if ip_type == "IPv4":
                            ipaddress.ip_address(ip)
                        elif ip_type == "IPv6":
                            ipaddress.ip_address(ip.split("/")[0])
                            # ipv6 = ipaddress.IPv6Address(ip.split('/')[0])
                            # print(f'IP Status of {host} for {ip}: {type(ipv6)}')
                    except (ipaddress.AddressValueError, ValueError):
                        print(f"Invalid IP address in {host}, {interface_type}: {ip}")
                        return False
    return True


class IaC_UnitTesting(unittest.TestCase):

    # Function to test ipam.csv file path & if file content is non-zero
    def test_IPAM_file(self):
        FILE = "ipam.csv"
        # Check if file is not empty
        file_size = os.path.getsize(FILE)
        self.assertNotEqual(file_size, 0, f"The ipam.csv file is empty.")

    # Function to check if IP's from ipam.csv are valid
    def test_IP_Validation(self):
        # Creating an empty dictionary to store the IP addresses with Hostnames and Interface types
        ip_dict = {}

        # Reading data from the CSV file and storing the IP addresses with Hostnames and Interface types in the dictionary
        with open("ipam.csv", mode="r") as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                hostname = row["Hostname"]
                interface_type = row["Interface_Type"]
                if hostname not in ip_dict:
                    ip_dict[hostname] = {}
                if interface_type not in ip_dict[hostname]:
                    ip_dict[hostname][interface_type] = {"IPv4": [], "IPv6": []}
                if "IPv4_Address" in row:
                    ip_dict[hostname][interface_type]["IPv4"].append(
                        row["IPv4_Address"]
                    )
                if "IPv6_Address" in row:
                    ip_dict[hostname][interface_type]["IPv6"].append(
                        row["IPv6_Address"]
                    )

        #print(json.dumps(ip_dict, indent=4))
        self.assertTrue(validate_ip_addresses(ip_dict))

    # Function to check if IP's from ipam.csv can be pinged
    def test_checkPing(self):
        ip_dict = app.read_ipam_csv("ipam.csv")
        #print(ip_dict)
        for ip in ip_dict:
            # resp = subprocess.call(["ping", "-c", "1", ip], stdout=subprocess.DEVNULL)
            # self.assertEqual(resp, 0, f"Ping to {ip} failed")
            resp = healthcheck.checkPing(ip, ip_dict[ip])
            self.assertEqual(
                resp, f"Ping of {ip_dict[ip]} was successful", f"Ping to {ip} failed"
            )


if __name__ == "__main__":
    unittest.main()
