from Project03 import navigation
from Scanning import destroy_scan
from Motor import destroy
#from HeatMapCode import generate_heatmap

if __name__ == "__main__":
    print("Program is starting...")
    try:
        navigation()
        #generate_heatmap()
    except KeyboardInterrupt:
        print("Stopping Program!")
        destroy_scan()
        destroy()
