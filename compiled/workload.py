import json
import sys
import requests


def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)

def read_workload_file(line):
    # Implement logic to read and parse the workload file
    servicetarget = line[0] 
    if servicetarget == "USER":
        line = {
            'command': servicetarget[1],
            'uid': servicetarget[2],
            'username': servicetarget[3],
            'email': servicetarget[4],
            'password': servicetarget[5]
        }
    elif servicetarget == "PRODUCT":
        line = {
            'command': servicetarget[1],
            'pid': servicetarget[2],
            'productname': servicetarget[3],
            'price': servicetarget[4],
            'quantity': servicetarget[5]
        }
    
    elif servicetarget == "ORDER":
        line = {
            'command': servicetarget[1],
            'uid': servicetarget[2],
            'pid': servicetarget[3],
            'quantity': servicetarget[4],
        }
    return line

def make_post_request(url, command):
    try:
        work = read_workload_file(command)
        response = requests.post(url, work)
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
    config = load_config(config_file)
    ip = config['OrderService']['ip_address']
    port =config['OrderService']['port']

    f = open('myfile.txt', 'r')
    Lines = f.readlines()
    for nline in Lines:
        line = nline.split()
        command = line[1]
        order_service_url = 'http://{}:{}/{}'.format(ip, port,line[0].lower())
        if (line[0].lower() == "user" and command == "get") or (command == "info" and line[0].lower() == "product"):
            make_get_request(order_service_url, nline)
        elif (line[0].lower() == "user" or line[0].lower() == "product") and (command == "create" or command == "update" or command == "delete") or (line[0].lower() == "order" and command == "place"):
            make_post_request(order_service_url, nline)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python workload_parser.py <config_file.json> <workload_file.txt>")
        sys.exit(1)
    config_file_path = sys.argv[1]
    workload_file_path = sys.argv[2]
    main(config_file_path, workload_file_path)




