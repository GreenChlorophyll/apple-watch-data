import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

oneDay = True
targetDay = datetime(2023, 6, 6)

tree = ET.parse('exports/export.xml')
root = tree.getroot()

class HealthDataPlotter:
    def __init__(self, recordType, lineColor='blue'):
        self.recordType = recordType
        self.values = []
        self.creationDates = []
        self.lineColor = lineColor

    def extractData(self, oneDay=False, targetDay=None):
        for record in root.findall('Record'):
            if record.get('type') == self.recordType:
                value = record.get('value')
                if self.isFloat(value):
                    creationDate = datetime.strptime(record.get('creationDate'), "%Y-%m-%d %H:%M:%S %z")
                    if oneDay and targetDay is not None:
                        if creationDate.date() == targetDay.date():
                            self.values.append(float(value))
                            self.creationDates.append(creationDate)
                    else:
                        self.values.append(float(value))
                        self.creationDates.append(creationDate)

    def isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError as e:
            print(e)
            return False

    def plotData(self):
        plt.plot(self.creationDates, self.values, color=self.lineColor)
        plt.xlabel('Creation Date')
        plt.ylabel('Value')
        plt.title(self.recordType)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'graphs/{self.recordType}.png')
        plt.close()

recordTypes = [
    'HKQuantityTypeIdentifierStepCount',
    'HKQuantityTypeIdentifierActiveEnergyBurned',
    'HKCategoryTypeIdentifierSleepAnalysis',
    'HKQuantityTypeIdentifierWalkingStepLength',
    'HKQuantityTypeIdentifierWalkingSpeed',
    'HKQuantityTypeIdentifierAppleStandTime',
    'HKQuantityTypeIdentifierWalkingDoubleSupportPercentage',
    'HKQuantityTypeIdentifierHeartRate'
]

plotters = []
for recordType in recordTypes:
    lineColor = 'red' if recordType == 'HKQuantityTypeIdentifierHeartRate' else 'blue'
    plotter = HealthDataPlotter(recordType, lineColor)
    plotters.append(plotter)


for plotter in plotters:
    plotter.extractData(oneDay, targetDay)
    plotter.plotData()