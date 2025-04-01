from Scanning import scan
from ScanVisualization import plot_scan

if __name__ == "__main__":
    print("Program is starting...")
    data = scan()
    if data:
        plot_scan(data)
    else:
        print("No data found")