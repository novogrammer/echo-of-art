import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--address", help="hostname or ip")
parser.add_argument("--port",type=int, help="port number")
args=parser.parse_args()

print(args.address)
print(args.port)