class PingInfo(object):
    """Stores info about pings to a node in an Object for ease-of-use."""
    def __init__(self, target):
        self.target = target
        self.path = []
        self.count = 0
        self.sum = 0
        self.average = None
        self.counts = []
        self.standard_dev = 0
        self.median = 0

    def add_to_stats(self, time, path):
        """adds an item to the ping's stats. Returns the z-score."""
        if path is not self.path:
            self.count = 0
            self.counts = []
            self.sum = 0
            self.average = 0
            self.path = path
        self.sum += time
        self.count += 1
        self.counts = []
        self.average = self.sum / self.count
        self.counts.sort()
        if self.counts % 2 == 1:
            self.median = self.counts[self.count // 2]
        else:
            self.median = (self.counts[self.count // 2] + self.counts[self.count // 2 + 1])/2.0
        self.calc_std_dev()
        return (time - self.average)/self.standard_dev

    def calc_std_dev(self):
        """Calculates the standard deviation of the ping info."""
        if self.count == 1:
            #z-score is going to be 0 anyway
            #as there is only one item in counts and therefore the average
            self.standard_dev = 1
        else:
            running_variance = 0
            for count in self.counts:
                running_variance += abs(self.average - count)
            self.standard_dev = (running_variance / (self.counts - 1))**(1/2.0)

    def information_summary(self):
        """Prints a summary of the statistics of the ping info."""
        message = 'Target: ' + self.target
        message += ('\n Mean: ' + self.average +'\t Median:' + self.median
                    + '\t Std Dev: ' + self.standard_dev + '\t N: ' + self.count)
        message += ('\n Path ->')
        for edge in self.path[:-1]:
            message += edge + '->'
        message += self.path[-1] + '\n'

