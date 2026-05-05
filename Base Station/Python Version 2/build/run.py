import subprocess
import sys

def startBackend():
    return subprocess.Popen([
        sys.executable,
        "backend/backendStart.py"
    ], cwd="build")


def startFrontend():
    return subprocess.Popen([
        sys.executable,
        "frontend/frontendStart.py"
    ], cwd="build")


def main():
    backend = startBackend()
    frontend = startFrontend()

    try:
        backend.wait()
        frontend.wait()
    except KeyboardInterrupt:
        backend.terminate()
        frontend.terminate()


if __name__ == "__main__":
    main()