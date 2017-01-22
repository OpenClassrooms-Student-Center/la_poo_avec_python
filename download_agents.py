#! /usr/bin/env python
import argparse
import json
import time
import urllib.error
import urllib.request


def main():
    parser = argparse.ArgumentParser(description="Download agents from pplapi.com")
    parser.add_argument("-c", "--count", type=int, default=10, help="Number of agents to download.")
    parser.add_argument("-d", "--dest", help="Destination file. If absent, will print to stdout")
    args = parser.parse_args()

    agents = []
    while len(agents) < args.count:
        if agents:
            # Wait one second between every request
            time.sleep(1)

        request_count = min(args.count - len(agents), 500)
        try:
            response = urllib.request.urlopen("http://pplapi.com/batch/{}/sample.json".format(request_count))
            agents += json.loads(response.read().decode("utf8"))
        except urllib.error.HTTPError:
            print("Too may requests, sleeping 10s ({} agents)".format(len(agents)))
            time.sleep(10)

    result = json.dumps(agents, indent=2, sort_keys=True)
    if args.dest:
        with open(args.dest, 'w') as out_f:
            out_f.write(result)
    else:
        print(result)


if __name__ == "__main__":
    main()
