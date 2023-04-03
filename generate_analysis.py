import json
import pandas as pd
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from datetime import datetime
import copy

RW_FOCUS = "RW_FOCUS"
RW_PERIPHERAL = "RW_PERIPHERAL"
RW_SECONDARY = "RW_SECONDARY"

VR_FOCUS = "VR_FOCUS"
VR_PERIPHERAL = "VR_PERIPHERAL"
VR_SECONDARY = "VR_SECONDARY"


ONE = "1"
TWO = "2"
THREE = "3"
FOUR = "4"

GestureMap = {}

EventMap = {ONE: RW_FOCUS, TWO: VR_FOCUS, THREE: RW_PERIPHERAL, FOUR: VR_PERIPHERAL}

KeyMap = {
    "whiteCaneStone": ONE,
    "whiteCane": ONE,
    "voiceAssistant": TWO,
    "constructionNoise": THREE,
    "cartoonDrilling": THREE,
    "voiceMessage": FOUR,
    "audiobook": ONE,
    "knocking": TWO,
    "announcement": THREE,
    "supervisorMessage": FOUR,
    "doga": ONE,
    "benko": ONE,
    "vlk": ONE,
    "patrick": TWO,
    "steve": TWO,
    "michael": TWO,
    "justine": TWO,
    "xu": TWO,
    "anhong": TWO,
    "obama": ONE,
    "ariel": ONE,
    "laura": ONE,
    "vrannouncement": FOUR,
    "tableCleaning": THREE,
}

Categories = {
    "constructionNoise": RW_PERIPHERAL,
    "cartoonDrilling": RW_PERIPHERAL,
    "voiceMessage": VR_PERIPHERAL,
    "voiceAssistant": VR_FOCUS,
    "whiteCaneStone": RW_FOCUS,
    "whiteCane": RW_FOCUS,
    "audiobook": VR_FOCUS,
    "knocking": RW_FOCUS,
    "announcement": RW_PERIPHERAL,
    "supervisorMessage": VR_PERIPHERAL,
    "doga": RW_FOCUS,
    "benko": RW_FOCUS,
    "vlk": RW_FOCUS,
    "patrick": VR_FOCUS,
    "steve": VR_FOCUS,
    "michael": VR_FOCUS,
    "justine": VR_FOCUS,
    "xu": VR_FOCUS,
    "anhong": VR_FOCUS,
    "obama": RW_FOCUS,
    "ariel": RW_FOCUS,
    "laura": RW_FOCUS,
    "vrannouncement": VR_PERIPHERAL,
    "tableCleaning": RW_PERIPHERAL,
}


def returnRealName(name):
    if "whiteCane" in name:
        name = "whiteCane"
    if "cartoonDrilling" in name:
        name = "constructionNoise"

    if "doga" in name:
        name = "anhong"
    if "anhong" in name:
        name = "anhong"
    if "benko" in name:
        name = "benko"
    if "vlk" in name:
        name = "vlk"
    if "patrick" in name:
        name = "patrick"
    if "steve" in name:
        name = "steve"
    if "michael" in name:
        name = "michael"
    if "justine" in name:
        name = "justine"
    if "xu" in name:
        name = "xu"
    if "obama" in name:
        name = "obama"
    if "ariel" in name:
        name = "ariel"
    if "laura" in name:
        name = "laura"
    if "sentence" in name:
        name = "audiobook"
    if "supervisorMessage" in name:
        name = "supervisorMessage"
    if "vrannouncement" in name:
        name = "vrannouncement"

    return name


colors = {
    "RW_FOCUS": "#34a0a4",
    # "RW_SECONDARY": "#76c893",
    "RW_PERIPHERAL": "#76c893",
    "VR_FOCUS": "#dc2f02",
    # "VR_SECONDARY": "#f48c06",
    "VR_PERIPHERAL": "#f48c06",
}

lineColors = {
    "1": colors["RW_FOCUS"],
    "2": colors["VR_FOCUS"],
    "3": colors["RW_PERIPHERAL"],
    "4": colors["VR_PERIPHERAL"],
}

# for event in eventToPlot:
#     if 'Finish' not in event:
#         print(event)
def datetime_to_float(d):
    epoch = datetime.utcfromtimestamp(0)
    total_seconds = (d - epoch).total_seconds()
    return total_seconds


class EachTrialResult:
    def __init__(self, path):

        self.path = path

        self.COUNTS = {
            "RW_FOCUS": 0,
            "VR_FOCUS": 0,
            "RW_SECONDARY": 0,
            "VR_SECONDARY": 0,
            "RW_PERIPHERAL": 0,
            "VR_PERIPHERAL": 0,
        }

        self.ERROR_COUNTS = {
            "RW_FOCUS": 0,
            "VR_FOCUS": 0,
            "RW_SECONDARY": 0,
            "VR_SECONDARY": 0,
            "RW_PERIPHERAL": 0,
            "VR_PERIPHERAL": 0,
        }

        self.MISS_EVENT = {
            "RW_FOCUS": 0,
            "VR_FOCUS": 0,
            "RW_SECONDARY": 0,
            "VR_SECONDARY": 0,
            "RW_PERIPHERAL": 0,
            "VR_PERIPHERAL": 0,
        }

        self.MISS_TOUCH = {
            "RW_FOCUS": 0,
            "VR_FOCUS": 0,
            "RW_SECONDARY": 0,
            "VR_SECONDARY": 0,
            "RW_PERIPHERAL": 0,
            "VR_PERIPHERAL": 0,
        }

        self.HIT_ERROR_COUNT = 0
        self.HIT_CORRECT_COUNT = 0
        self.MISS_EVENT_COUNT = 0
        self.MISS_TOUCH_COUNT = 0

        self.DELAYS = {
            "VR_FOCUS": [],
            "RW_FOCUS": [],
            "VR_PERIPHERAL": [],
            "RW_PERIPHERAL": [],
            "VR_SECONDARY": [],
            "RW_SECONDARY": [],
        }

        self.eventToPlot = self.preprocessing(path)

        self.SUMS = {
            "VR_FOCUS": len(
                [x for x in self.eventToPlot if x["Resource"] == "VR_FOCUS"]
            ),
            "RW_FOCUS": len(
                [x for x in self.eventToPlot if x["Resource"] == "RW_FOCUS"]
            ),
            "VR_PERIPHERAL": len(
                [x for x in self.eventToPlot if x["Resource"] == "VR_PERIPHERAL"]
            ),
            "RW_PERIPHERAL": len(
                [x for x in self.eventToPlot if x["Resource"] == "RW_PERIPHERAL"]
            ),
            "VR_SECONDARY": len(
                [x for x in self.eventToPlot if x["Resource"] == "VR_SECONDARY"]
            ),
            "RW_SECONDARY": len(
                [x for x in self.eventToPlot if x["Resource"] == "RW_SECONDARY"]
            ),
        }

    def getHitAccuracy(self, type=""):
        if type == "":
            number = self.getTotalNumOfEvents()
            accuracy = self.HIT_CORRECT_COUNT / number
            # print("Hit Accuracy: ", accuracy)
            return accuracy
        else:
            if self.SUMS[type] == 0:
                return 1
            # print("delay of " + type + ":", self.COUNTS[type] / self.SUMS[type])
            return self.COUNTS[type] / self.SUMS[type]

    def getTotalNumOfEvents(self, type=""):
        if type == "":
            number = 0
            for i in self.SUMS:
                number += self.SUMS[i]
            # print("Total number of event is: ", number)
            return number
        else:
            return self.SUMS[type]

    def getHitErrorCount(self, type=""):
        if type == "":
            # print("Number of Hit Error Event: ", self.HIT_ERROR_COUNT)
            return self.HIT_ERROR_COUNT
        else:
            return self.ERROR_COUNTS[type]

    def getHitCorrectCount(self, type=""):
        if type == "":
            # print("Number of Hit Correct Event: ", self.HIT_CORRECT_COUNT)
            return self.HIT_CORRECT_COUNT
        else:
            return self.COUNTS[type]

    def getMissTouchCount(self, type=""):
        if type == "":
            # print("Number of Miss Touch: ", self.MISS_TOUCH_COUNT)
            return self.MISS_TOUCH_COUNT
        else:
            return self.MISS_TOUCH[type]

    def countOnTypeMissTouch(self, typeOfTask):
        self.MISS_TOUCH[typeOfTask] += 1
        return

    def countOnTypeMissEvent(self, typeOfTask):
        self.MISS_EVENT[typeOfTask] += 1
        return

    def getMissEventCount(self, type=""):
        if type == "":
            # print("Number of Miss Event: ", self.MISS_EVENT_COUNT)
            return self.MISS_EVENT_COUNT
        else:
            return self.MISS_EVENT[type]

    def getOverallAverageDelay(self):
        res_list = []
        for i in self.DELAYS:
            res_list.extend(self.DELAYS[i])
        if len(res_list) == 0:
            return 0
        delay = sum(res_list) / len(res_list)
        # print("Overall average delay is:", delay)
        return delay

    def getSingleCategoryDelay(self, type):
        res_list = self.DELAYS[type]
        if len(res_list) == 0:
            return 0
        delay = sum(res_list) / len(res_list)
        # print("delay of " + type + ":", delay)
        return delay

    def addDelayBasedOnType(self, typeOfTask, delayValue):
        self.DELAYS[typeOfTask].append(delayValue)
        return

    def countOnType(self, typeOfTask):
        self.COUNTS[typeOfTask] += 1
        return

    def countOnTypeWithError(self, typeOfTask):
        self.ERROR_COUNTS[typeOfTask] += 1
        return

    def preprocessing(self, path):
        with open(path) as json_file:
            data = json.load(json_file)

            EventLogs = data["EventLogs"]
            df = {}
            eventToPlot = []

            while len(EventLogs):
                for eventLog in EventLogs:
                    clipName = eventLog["clipName"]
                    clipName = returnRealName(clipName)
                    # if "whiteCane" in clipName:
                    #     clipName = "whiteCane"
                    # if "sentence" in clipName:
                    #     clipName = "audiobook"
                    if clipName not in df:
                        df[clipName] = {}

                    happenTime = pd.to_datetime(float(eventLog["happenTime"]), unit="s")
                    df[clipName]["Task"] = clipName
                    df[clipName]["Resource"] = Categories[clipName]
                    if (
                        eventLog["enterOrExit"] == "enter"
                        and "Start" not in df[clipName]
                    ):
                        df[clipName]["Start"] = happenTime
                        EventLogs.remove(eventLog)
                        break
                    elif eventLog["enterOrExit"] == "exit" and "Start" in df[clipName]:
                        df[clipName]["Finish"] = happenTime
                        eventToPlot.append(df[clipName])
                        del df[clipName]
                        EventLogs.remove(eventLog)
                        break
            for clipName in df:
                eventToPlot.append(df[clipName])
        return eventToPlot

    def overlapCheck(self, event1, event2):
        start1  = datetime_to_float(event1["Start"])
        end1    = datetime_to_float(event1["Finish"])
        start2  = datetime_to_float(event2["Start"])
        end2    = datetime_to_float(event2["Finish"])
        interval1 = pd.Interval(start1, end1)
        interval2 = pd.Interval(start2, end2)
        return interval1.overlaps(interval2)
        # str = 'yes' if result else 'no'
        # start1 = datetime_to_float(event1["Start"])
        # end1 = datetime_to_float(event1["Finish"])
        # start2 = datetime_to_float(event2["Finish"])
        # end2 = datetime_to_float(event2["Finish"])
        # return  start1<end2 and start2<end1

    def dictForMixedAnalysis(self, input_event, Success, SoundType, Delay=0 ):
        temp = {}
        temp['Success'] = Success
        temp['Delay'] = Delay 
        temp['SoundType'] = SoundType
        temp['NumOfOverlaps'] = 0
        temp['OverlapRWVR'] = []
        temp['OverlapFP'] = []

        # print(len(self.eventToPlot))
        for event in self.eventToPlot:
            if self.overlapCheck(input_event, event):
                temp['NumOfOverlaps'] += 1
                eventType = event["Resource"]
                if 'RW' in eventType: temp['OverlapRWVR'].append('RW')
                if 'VR' in eventType: temp['OverlapRWVR'].append('VR')
                if 'FOCUS' in eventType: temp['OverlapFP'].append('F')
                if 'PERIPHERAL' in eventType: temp['OverlapFP'].append('P')
        
        if len(temp['OverlapRWVR']) ==0: temp['OverlapRWVR'] = None
        elif 'RW' in temp['OverlapRWVR'] and 'VR' in temp['OverlapRWVR']: temp['OverlapRWVR'] = "RW+VR"
        elif 'RW' in temp['OverlapRWVR'] and 'VR' not in temp['OverlapRWVR']: temp['OverlapRWVR'] = "RW"
        elif 'RW' not in temp['OverlapRWVR'] and 'VR' in temp['OverlapRWVR']: temp['OverlapRWVR'] = "VR"
        
        if len(temp['OverlapFP']) ==0: temp['OverlapFP']= None
        elif 'F' in temp['OverlapFP'] and 'P' in temp['OverlapFP']: temp['OverlapFP'] = "F+P"
        elif 'F' in temp['OverlapFP'] and 'P' not in temp['OverlapFP']: temp['OverlapFP'] = "F"
        elif 'F' not in temp['OverlapFP'] and 'P' in temp['OverlapFP']: temp['OverlapFP'] = "P"

        # if temp['NumOfOverlaps'] == 0:
        #     print("no overlap", input_event)
        return temp

    def outputForMixedAnalysis(self):
        temp = []
        with open(self.path) as json_file:
            data = json.load(json_file)
            TouchLogs = data["TouchLogs"]
            eventToPlot = copy.deepcopy(self.eventToPlot)
        while len(TouchLogs):
            for touchLog in TouchLogs:
                touchTime = touchLog["touchTime"]
                touchEvent = touchLog["singleOrDouble"]
                playingObjects = [returnRealName(x) for x in touchLog["playingObjects"]]

                if len(playingObjects) == 0:
                    # self.MISS_TOUCH_COUNT += 1
                    # self.countOnTypeMissTouch(EventMap[touchEvent])
                    TouchLogs.remove(touchLog)
                    break

                else:
                    collectedTouchEvents = [KeyMap[x] for x in playingObjects]
                    if touchEvent not in collectedTouchEvents:
                        # self.HIT_ERROR_COUNT += 1
                        # self.countOnTypeWithError(EventMap[touchEvent])
                        TouchLogs.remove(touchLog)
                        break
                    for playingObject in playingObjects:
                        if KeyMap[playingObject] == touchEvent:
                            eventStillExist = False
                            for event in eventToPlot:
                                start = datetime_to_float(event["Start"])
                                end = datetime_to_float(event["Finish"])
                                clipName = event["Task"]
                                category = event["Resource"]
                                if (
                                    touchTime >= start
                                    and touchTime <= end
                                    and playingObject == clipName
                                ):
                                    eventStillExist = True

                            if not eventStillExist:
                                # self.HIT_ERROR_COUNT += 1
                                # self.countOnTypeWithError(EventMap[touchEvent])
                                TouchLogs.remove(touchLog)
                                break
                            for event in eventToPlot:
                                start = datetime_to_float(event["Start"])
                                end = datetime_to_float(event["Finish"])
                                clipName = event["Task"]
                                category = event["Resource"]
                                if (
                                    touchTime >= start
                                    and touchTime <= end
                                    and playingObject == clipName
                                ):
                                    delay = abs(
                                        touchTime - datetime_to_float(event["Start"])
                                    )
                                    # self.addDelayBasedOnType(category, delay)
                                    # self.HIT_CORRECT_COUNT += 1
                                    # self.countOnType(category)

                                    temp.append(self.dictForMixedAnalysis(event, 1, category, delay))

                                    TouchLogs.remove(touchLog)
                                    eventToPlot.remove(event)
                                    break
                            break
        # self.MISS_EVENT_COUNT = len(eventToPlot)
        for event in eventToPlot:
            # self.countOnTypeMissEvent(event["Resource"])
            category = event["Resource"]
            temp.append(self.dictForMixedAnalysis(event, 0, category, Delay=0))


        return temp

    def calculateResultsByKey(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
            TouchLogs = data["TouchLogs"]
            # EventLogs = data["EventLogs"]
            eventToPlot = copy.deepcopy(self.eventToPlot)
        while len(TouchLogs):
            for touchLog in TouchLogs:
                touchTime = touchLog["touchTime"]
                touchEvent = touchLog["singleOrDouble"]
                playingObjects = [returnRealName(x) for x in touchLog["playingObjects"]]

                if len(playingObjects) == 0:
                    self.MISS_TOUCH_COUNT += 1
                    self.countOnTypeMissTouch(EventMap[touchEvent])
                    TouchLogs.remove(touchLog)
                    break

                else:
                    # check if hit wrong first
                    collectedTouchEvents = [KeyMap[x] for x in playingObjects]
                    # print(collectedTouchEvents)
                    # print("\n")
                    if touchEvent not in collectedTouchEvents:
                        self.HIT_ERROR_COUNT += 1
                        self.countOnTypeWithError(EventMap[touchEvent])
                        TouchLogs.remove(touchLog)
                        break
                    for playingObject in playingObjects:
                        # typeOfTask = Categories[playingObject]
                        # print(KeyMap[playingObject],touchEvent)
                        # print("\n")
                        if KeyMap[playingObject] == touchEvent:
                            # find event first, if not then break, yes then continue
                            # basically this is to catch multiple inputs on a single event
                            eventStillExist = False
                            for event in eventToPlot:
                                start = datetime_to_float(event["Start"])
                                end = datetime_to_float(event["Finish"])
                                clipName = event["Task"]
                                category = event["Resource"]
                                if (
                                    touchTime >= start
                                    and touchTime <= end
                                    and playingObject == clipName
                                ):
                                    eventStillExist = True

                            if not eventStillExist:
                                self.HIT_ERROR_COUNT += 1
                                self.countOnTypeWithError(EventMap[touchEvent])
                                TouchLogs.remove(touchLog)
                                break
                            for event in eventToPlot:
                                start = datetime_to_float(event["Start"])
                                end = datetime_to_float(event["Finish"])
                                clipName = event["Task"]
                                category = event["Resource"]
                                if (
                                    touchTime >= start
                                    and touchTime <= end
                                    and playingObject == clipName
                                ):
                                    delay = abs(
                                        touchTime - datetime_to_float(event["Start"])
                                    )
                                    self.addDelayBasedOnType(category, delay)
                                    self.HIT_CORRECT_COUNT += 1
                                    self.countOnType(category)

                                    TouchLogs.remove(touchLog)
                                    eventToPlot.remove(event)
                                    break
                            break
        self.MISS_EVENT_COUNT = len(eventToPlot)
        for event in eventToPlot:
            self.countOnTypeMissEvent(event["Resource"])


def generate_type_analysis(input_path):
    trial = EachTrialResult(input_path)
    trial.calculateResultsByKey()

    result = {}

    for type in EventMap.values():
        delay = trial.getSingleCategoryDelay(type)
        miss_event = trial.getMissEventCount(type)
        miss_touch = trial.getMissTouchCount(type)
        hit_correct = trial.getHitCorrectCount(type)
        hit_error = trial.getHitErrorCount(type)
        total_event = trial.getTotalNumOfEvents(type)
        hit_accuracy = trial.getHitAccuracy(type)

        result[type] = [
            hit_accuracy,
            hit_error / total_event,
            miss_event,
            miss_touch,
            delay,
        ]

        # result[type] = [
        #     delay,
        #     miss_event,
        #     miss_touch,
        #     hit_correct,
        #     hit_error,
        #     total_event,
        #     hit_accuracy,
        # ]

    return result


def generate_result(input_path):
    trial = EachTrialResult(input_path)
    trial.calculateResultsByKey()

    delay = trial.getOverallAverageDelay()
    miss_event = trial.getMissEventCount()
    miss_touch = trial.getMissTouchCount()
    hit_correct = trial.getHitCorrectCount()
    hit_error = trial.getHitErrorCount()
    total_event = trial.getTotalNumOfEvents()
    hit_accuracy = trial.getHitAccuracy()

    result = [
        hit_accuracy,
        hit_error / total_event,
        miss_event,
        miss_touch,
        delay,
        # hit_correct,
        # hit_error,
        # total_event,
    ]

    return result
