import subprocess

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# def startApi():
#     return subprocess.Popen(
#     [
#         "uvicorn",
#         "api:app",
#         "--host", "127.0.0.1",
#         "--port", "8000",
#         "--no-access-log",
#         "--log-level", "critical"
#     ],
#     cwd="backend",
#     stdout=subprocess.DEVNULL,
#     stderr=subprocess.DEVNULL
# )
    


def startFetcher():
    return subprocess.Popen(
        [
            sys.executable,
            "runFetcher.py"
        ],
        cwd="backend"
    )

def main():
    print("Starting backend processes...")
    # api = startApi()
    # fetcher = startFetcher()

    # try:
    #     api.wait()
    #     fetcher.wait()
    # except KeyboardInterrupt:
    #     api.terminate()
    #     fetcher.terminate()


if __name__ == "__main__":
    main()