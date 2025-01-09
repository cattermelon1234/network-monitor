from RealTimeNetworkMonitor import RealTimeMonitor
    
def main():
    print("starting!")
    monitor = RealTimeMonitor()
    monitor.analyze('en0')

if __name__ == "__main__":
    main()