from ConnectionDistribution import ConnectionDistribution
import pyshark

class ConnectionAnalyzer:
    TIME_TO_LEARN = 60000
    TIME_TO_CLEAR_ALERT = 300000
    THRESHOLD_BUFFER = 50

    def __init__(self):
        self.packetCounts = {}
        self.startTime = None
        self.currentTotalCount = 0
        self.connection_distribution = ConnectionDistribution()
        self.detection_distribution = ConnectionDistribution()
        self.state = "LEARN"
        self.clearTime = None
        self.threshold = None

    
    def analyze(self, timestamp, packet):
        if not self.startTime:
            self.startTime = timestamp
            print("starting monitoring at ", timestamp)

        elapsed = 1000 * abs(timestamp - self.startTime)
        if self.state == "LEARN":
            self.connection_distribution.collect(timestamp, packet)
            if elapsed >= self.TIME_TO_LEARN:
                self.state = "DETECT"
                print("finished learning")

                self.threshold = self.connection_distribution.getMaxDeviation() * (100 + self.THRESHOLD_BUFFER) / 100
                print("threshold: ", threshold)
                print("mean entropy: ", self.connection_distribution.calculateMean())
                print("max deviation from mean: ", self.connection_distribution.getMaxDeviation())
                
        elif self.state == "DETECT":
            entropy = self.detection_distribution.collect(timestamp, packet)
            if threshold and entropy and entropy - self.connection_distribution.calculateMean() > self.threshold:
                print("alert happened at entropy value ", entropy)
                self.state = "ALERT"

        else:
            print("alerting")
            entropy = self.detection_distribution.collect(timestamp, packet)
            threshold = self.connection_distribution.getMaxDeviation() * (100 + self.THRESHOLD_BUFFER) / 100
            if entropy and threshold and entropy - self.connection_distribution.calculateMean() <= threshold:
                if not self.clearTime: 
                    self.clearTime = timestamp
                else:
                    elapsedSinceCleared = 1000 * abs(timestamp - self.clearTime)
                    if elapsedSinceCleared >= self.TIME_TO_CLEAR_ALERT:
                        print("alert cleared!")
                        print("traffic normal at entropy value " + entropy)
                        self.state = "DETECT"
            else:
                self.clearTime = None

