from src.runner import Runner
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file>")
        return
    file, *_ = sys.argv[1:]
    runner = Runner(file)
    return runner.run("-d" in sys.argv or "--debug" in sys.argv);

if(__name__ == "__main__"):
    main();