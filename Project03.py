from Scanning import scan
from ScanVisualization import plot_scan

if __name__ == "__main__":
    print("Program is starting...")
    data = scan()
    plot_scan(data)