from datetime import datetime
import math 
from Connection import Connection

class ConnectionDistribution:
    INTERVAL = 1000
    def __init__(self):
        self.total_packets = 0
        self.interval_distribution = {}
        self.startTime = None
        self.entropy_distribution = {}
    
    def collect(self, timestamp, packet):
        if not self.startTime:
            self.startTime = timestamp

        elapsed = 1000 * abs(timestamp - self.startTime)
        connection = Connection(packet)
        self.total_packets += 1
        entropy = None
        if elapsed >= self.INTERVAL:
            entropy = self.calculateEntropy(self.interval_distribution)
            self.entropy_distribution[self.startTime] = entropy
            self.startTime = timestamp
            self.interval_distribution = {}
            self.total_packets = 0
        else:
            if connection in self.interval_distribution:
                self.interval_distribution[connection] += 1
            else:
                self.interval_distribution[connection] = 1
        return entropy
    
    def calculateEntropy(self, interval_distribution):
        entropy = 0.0
        for connection in interval_distribution:
            probability = interval_distribution[connection] / self.total_packets
            entropy -= probability * math.log(probability) / math.log(2)
        return entropy

    def calculateMean(self):
        sum = 0
        for time in self.entropy_distribution:
            sum += self.entropy_distribution[time]
        return sum / len(self.entropy_distribution)

    def getMaxDeviation(self):
        mean = self.calculateMean()
        threshold = 0
        for time in self.entropy_distribution:
            dev = abs(self.entropy_distribution[time] - mean)
            if dev > threshold:
                threshold = dev
        return threshold
            
    