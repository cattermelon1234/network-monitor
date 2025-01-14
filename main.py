import sys
from RealTimeNetworkMonitor import RealTimeMonitor

# invoking script:
# python script.py en0
# python script.py capture.pcap

def main():
    monitor = RealTimeMonitor()

    if len(sys.argv) != 2:
        print("Usage: python script.py <interface|pcap_file>")
        sys.exit(1)
    
    input_source = sys.argv[1]
    
    if input_source.endswith('.pcap'):
        print(f"Analyzing pcap file: {input_source}")
        monitor.analyze_pcap(input_source)
    else:
        print(f"Analyzing live interface: {input_source}")
        monitor.analyze(input_source)

if __name__ == "__main__":
    main()
