import pandas as pd
import ipaddress

# Function to update the IPAM with the new router IP addresses
def update_ipam(data):
    # Read the CSV into a DataFrame
    df = pd.read_csv('ipam.csv')

    # Extract relevant fields from the dictionary
    new_rows = []
    '''
    m_ipv4 = data['management_ipv4']
    m_ipv4_subnet = ipaddress.IPv4Network(m_ipv4, strict=False)
    m_ipv4_subnet = m_ipv4_subnet.netmask
    print(f'Management IPv4 Subnet: {m_ipv4_subnet}')
'''
    new_rows.append([
        data['hostname'],
        'Management',
        data['management_ipv4'].split('/')[0],
        str(ipaddress.IPv4Network(data['management_ipv4'], strict=False).netmask),
        data['management_ipv6']
    ])

    for interface in data['interfaces']:
        # Check if the address is IPv4 or IPv6
        if ':' in interface['ipv4_address']:
            # IPv6 address
            ipv4_address = ''
            ipv4_subnet = ''
            ipv6_address = interface['ipv4_address']
        else:
            # IPv4 address
            ipv4_address = interface['ipv4_address'].split('/')[0]
            # Convert CIDR notation to dotted decimal format
            ipv4_subnet = str(ipaddress.IPv4Network(interface['ipv4_address'], strict=False).netmask)
            ipv6_address = interface['ipv6_address']

        new_rows.append([
            data['hostname'],
            interface['name'],
            ipv4_address,
            ipv4_subnet,
            ipv6_address
        ])

    # Create a new DataFrame with the new rows
    new_df = pd.DataFrame(new_rows, columns=df.columns)

    # Concatenate the new DataFrame with the original DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    # Write back to the CSV file
    df.to_csv('ipam.csv', index=False)

# Function to read contents of neighboring routers config
def get_neighboring_router_config(router_name):
    main_routers = ['R1','R2','R3','R4','R5']
    #Get file path for main routers:
    try:
        if router_name in main_routers:
            file_path = f'/home/ana-moeez-2/lab4/updated_startup_configs/{router_name}_startup.txt'
    except:
        print(f'Unable to find path for {router_name}\n Exiting Program!')
        SystemExit()
    # Read the content from the file
    with open(file_path, 'r') as file:
        neighboring_router_config = file.read()
    return file_path, neighboring_router_config

def update_neighboring_router_ospf(router_name, ospf_networks, ospf_areas):
    # Get the existing configuration content from the file
    file_path, neighboring_router_config = get_neighboring_router_config(router_name)
    
    ospf_index = neighboring_router_config.find('router ospf')   
    while ospf_index != -1:
        # Find the end of the OSPF section
        router_ospf_section_end = neighboring_router_config.find('!', ospf_index)

        if router_ospf_section_end != -1:
            # Extract the OSPF number dynamically
            ospf_number_start = ospf_index + len('router ospf')
            ospf_number_end = neighboring_router_config.find(' ', ospf_number_start)
            ospf_number = neighboring_router_config[ospf_number_start:ospf_number_end]

            ospf_section = neighboring_router_config[ospf_index:router_ospf_section_end]

            for network, area in zip(ospf_networks, ospf_areas):
                network_line = f'   network {network} area {area}\n'
                # Check if the network line already exists, if yes, replace it; otherwise, append
                if network_line in ospf_section:
                    ospf_section = ospf_section.replace(network_line, '')
                ospf_section += network_line

            # Replace the original OSPF section with the updated one
            neighboring_router_config = neighboring_router_config[:ospf_index] + ospf_section + neighboring_router_config[router_ospf_section_end:]

            # Find the next occurrence of "router ospf" after the end of the current OSPF section
            ospf_index = neighboring_router_config.find('router ospf', router_ospf_section_end)

        else:
            break  # If "router ospf" section is not found, exit the loop

        # Concatenate the parts to get the final updated config
        updated_config = neighboring_router_config

    # Write the updated configuration back to the file
    with open(file_path, 'w') as file:
        file.write(updated_config)

    return updated_config
