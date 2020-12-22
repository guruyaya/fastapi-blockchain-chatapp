from app import app

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--port", help="Set the port to run blockchain", default=8000, type=int)
parser.add_argument("--host", help="Set the host to run blockchain", default="0.0.0.0")
parser.add_argument("-d", help="Start with debug mode", action="store_true")

args = parser.parse_args()

app.run(debug=True, host=args.host, port=args.port)