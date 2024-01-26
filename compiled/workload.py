import json
import sys
import requests


def load_config(config_file):
    try:
        with open(config_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Config file '{config_file}' not found.")
        sys.exit(1)

def read_workload_file(lines, operation):
    # Implement logic to read and parse the workload file
    # line = lines.split()
    servicetarget = lines
    if operation == "user":
        dp = {
            'command': servicetarget[1],
            'uid': servicetarget[2],
            'username': servicetarget[3],
            'email': servicetarget[4],
            'password': servicetarget[5]
        }
    elif operation == "product":
        dp = {
            'command': servicetarget[1],
            'pid': servicetarget[2],
            'productname': servicetarget[3],
            'price': servicetarget[4],
            'quantity': servicetarget[5]
        }
    
    elif operation == "order":
        dp = {
            'command': servicetarget[1],
            'uid': servicetarget[2],
            'pid': servicetarget[3],
            'quantity': servicetarget[4],
        }
    return dp

def make_post_request(url, command):
    try:
        work = read_workload_file(command)
        response = requests.post(url, data=work)
        if response.status_code == 200:
            print(f"POST request did work: {response.status_code}")
            print("Response: ", response.text)
        else:
            print(f"POST request did not work: {response.status_code}")
            print("Response: ", response.text)
    except Exception as e:
        print(e)



def make_get_request(url, command):
    try:
        response = requests.get(url + str(command[2]))
        if response.status_code == 200:
            print(f"POST request did work: {response.status_code}")
            print("Response: ", response.text)
        else:
            print(f"POST request did not work: {response.status_code}")
            print("Response: ", response.text)
    except Exception as e:
        print(e)


def main(config_file, workload_file_path):
    action_to_method_post = {
        "user": ["create","update", "delete"],
        "order": ["place"],
        "product": ["create","update", "delete"]
    }
    action_to_method_get = {
        "product": ["info"],
        "user": ["get"]
    }

    config = load_config(config_file)
    ip = config['OrderService']['ip_address']
    port =config['OrderService']['port']

    try:
        f = open(workload_file_path, 'r')
        Lines = f.readlines()
        for nline in Lines:
            line = nline.split()
            command = line[1]
            target_service = line[0].lower()
            order_service_url = 'http://{}:{}/{}'.format(ip, port,target_service)
            if target_service in action_to_method_get:
                if command in action_to_method_get[target_service]:
                    make_get_request(order_service_url, line)
                else:
                    raise ValueError(f"Invalid service target")
            elif target_service in action_to_method_post:
                if command in action_to_method_get[target_service]:
                    make_post_request(order_service_url, line)
                else:
                    raise ValueError(f"Invalid service target")
            else:
                raise ValueError(f"Invalid service target")
    except FileNotFoundError:
        print(f"Error: workload file '{workload_file_path}' not found.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python workload_parser.py <config_file.json> <workload_file.txt>")
        sys.exit(1)
    config_file_path = sys.argv[1]
    workload_file_path = sys.argv[2]
    main(config_file_path, workload_file_path)





