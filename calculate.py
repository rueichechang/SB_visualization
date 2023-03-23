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

GestureMap ={

}

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
    "patrick": ONE,
    "steve": ONE,
    "michael": ONE,
    "justine": ONE,
    "xu": ONE,
    "anhong": ONE,
    "obama": ONE,
    "ariel": ONE,
    "laura": ONE,
    "vrannouncement": TWO,
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
    "knocking": RW_SECONDARY,
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

colors = {
    "RW_FOCUS": "#34a0a4",
    "RW_SECONDARY": "#76c893",
    "RW_PERIPHERAL": "#b5e48c",
    "VR_FOCUS": "#dc2f02",
    "VR_SECONDARY": "#f48c06",
    "VR_PERIPHERAL": "#ffba08",
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

    def getHitAccuracy(self):
        number = self.getTotalNumOfEvents()
        accuracy = self.HIT_CORRECT_COUNT / number
        print("Hit Accuracy: ", accuracy)
        return accuracy

    def getTotalNumOfEvents(self):
        number = 0
        for i in self.SUMS:
            number += self.SUMS[i]
        print("Total number of event is: ", number)
        return number

    def getHitErrorCount(self):
        print("Number of Hit Error Event: ", self.HIT_ERROR_COUNT)
        return self.HIT_ERROR_COUNT

    def getHitCorrectCount(self):
        print("Number of Hit Correct Event: ", self.HIT_CORRECT_COUNT)
        return self.HIT_CORRECT_COUNT

    def getMissTouchCount(self):
        print("Number of Touch Event: ", self.MISS_TOUCH_COUNT)
        return self.MISS_TOUCH_COUNT

    def getMissEventCount(self):
        print("Number of Miss Event: ", self.MISS_EVENT_COUNT)
        return self.MISS_EVENT_COUNT

    def getOverallAverageDelay(self):
        res_list = []
        for i in self.DELAYS:
            res_list.extend(self.DELAYS[i])
        if len(res_list) == 0:
            return
        delay = sum(res_list) / len(res_list)
        print("Overall average delay is:", delay)
        return delay

    def getSingleCategoryDelay(self, name):
        res_list = self.DELAYS[name]
        delay = sum(res_list) / len(res_list)
        print("delay of " + name + ":", delay)
        return delay

    def addDelayBasedOnType(self, typeOfTask, delayValue):
        self.DELAYS[typeOfTask].append(delayValue)
        return

    def countOnType(self, typeOfTask):
        self.COUNTS[typeOfTask] += 1
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
                    if "whiteCane" in clipName:
                        clipName = "whiteCane"
                    if "sentence" in clipName:
                        clipName = "audiobook"
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

    def makePlot(self, output_path=""):
        fig = ff.create_gantt(
            self.eventToPlot,
            colors=colors,
            index_col="Resource",
            show_colorbar=True,
            group_tasks=True,
        )

        # RWVRPLOT = px.timeline(eventToPlot, x_start="Start", x_end="Finish", y="Resource", color="Resource")

        with open(self.path) as json_file:
            data = json.load(json_file)
            TouchLogs = data["TouchLogs"]

            for touchLog in TouchLogs:
                touchTime = pd.to_datetime(float(touchLog["touchTime"]), unit="s")

                lineColor = "blue" if touchLog["singleOrDouble"] == "single" else "red"

                fig.add_trace(
                    go.Scatter(
                        x=[touchTime, touchTime],
                        y=[-1, len(self.eventToPlot) + 1],
                        mode="lines",
                        line=go.scatter.Line(color=lineColor, width=1),
                        showlegend=False,
                    )
                )

                #         RWVRPLOT.add_trace(
                #             go.Scatter(
                #                 x = [touchTime, touchTime],
                #                 y = [10, 1010000],
                #                 mode = "lines",
                #                 line = go.scatter.Line(color = lineColor, width = 1),
                #                 showlegend = False
                #             )
                #         )
            if output_path == "": fig.show()
            # fig.write_html()
            else: fig.write_image(output_path)
            # pio.write_image(fig, output_path, format="png")

    def calculateResults(self):
        with open(self.path) as json_file:
            data = json.load(json_file)
            TouchLogs = data["TouchLogs"]
            EventLogs = data["EventLogs"]
            eventToPlot = copy.deepcopy(self.eventToPlot)

        while len(TouchLogs):
            for touchLog in TouchLogs:
                touchTime = touchLog["touchTime"]
                singelORdouble = touchLog["singleOrDouble"]
                candidateEvents = []

                for event in eventToPlot:
                    start = datetime_to_float(event["Start"])
                    end = datetime_to_float(event["Finish"])
                    if touchTime >= start and touchTime <= end:
                        candidateEvents.append(event)

                if len(candidateEvents) == 0:
                    self.MISS_TOUCH_COUNT += 1
                    TouchLogs.remove(touchLog)
                    print("------------No Hit------------\n")
                    print(touchLog)
                    print("==============================\n\n")
                    break
                elif len(candidateEvents) == 1:
                    typeOfTask = candidateEvents[0]["Resource"]
                    if (
                        singelORdouble == "single"
                        and "RW" in typeOfTask
                        or singelORdouble == "double"
                        and "VR" in typeOfTask
                    ):
                        self.HIT_CORRECT_COUNT += 1
                        self.countOnType(typeOfTask)
                        delay = abs(
                            touchTime - datetime_to_float(candidateEvents[0]["Start"])
                        )
                        self.addDelayBasedOnType(typeOfTask, delay)

                    else:
                        self.HIT_ERROR_COUNT += 1

                    print("-----------Candidate----------\n")
                    print(candidateEvents[0])
                    print("-----------Touchlog-----------\n")
                    print(touchLog)
                    print("==============================\n\n\n")

                    TouchLogs.remove(touchLog)
                    eventToPlot.remove(candidateEvents[0])
                    break
                elif len(candidateEvents) > 1:
                    RWEvents = [
                        event for event in candidateEvents if "RW" in event["Resource"]
                    ]
                    VREvents = [
                        event for event in candidateEvents if "VR" in event["Resource"]
                    ]

                    if singelORdouble == "single" and len(RWEvents) > 0:
                        TEMP_DIFF = float("inf")
                        TARGET_START = ""
                        for RWEvent in RWEvents:
                            START_OF_EVENT = datetime_to_float(RWEvent["Start"])
                            DIFF = abs(touchTime - START_OF_EVENT)
                            if DIFF < TEMP_DIFF:
                                TEMP_DIFF = DIFF
                                TARGET_START = START_OF_EVENT
                        candidateEvent = [
                            event
                            for event in RWEvents
                            if datetime_to_float(event["Start"]) == TARGET_START
                        ][0]
                        delay = abs(
                            touchTime - datetime_to_float(candidateEvent["Start"])
                        )
                        typeOfTask = candidateEvent["Resource"]
                        print("-----------Candidate----------\n")
                        print(candidateEvent)
                        print("-----------Touchlog-----------\n")
                        print(touchLog)
                        print("==============================\n\n")
                        self.addDelayBasedOnType(typeOfTask, delay)
                        self.HIT_CORRECT_COUNT += 1
                        self.countOnType(typeOfTask)
                        TouchLogs.remove(touchLog)
                        eventToPlot.remove(candidateEvent)

                    elif singelORdouble == "double" and len(VREvents) > 0:
                        TEMP_DIFF = float("inf")
                        TARGET_START = ""
                        for VREvent in VREvents:
                            START_OF_EVENT = datetime_to_float(VREvent["Start"])
                            DIFF = abs(touchTime - START_OF_EVENT)
                            if DIFF < TEMP_DIFF:
                                TEMP_DIFF = DIFF
                                TARGET_START = START_OF_EVENT
                        candidateEvent = [
                            event
                            for event in VREvents
                            if datetime_to_float(event["Start"]) == TARGET_START
                        ][0]
                        delay = abs(
                            touchTime - datetime_to_float(candidateEvent["Start"])
                        )
                        typeOfTask = candidateEvent["Resource"]
                        print("-----------Candidate----------\n")
                        print(candidateEvent)
                        print("-----------Touchlog-----------\n")
                        print(touchLog)
                        print("==============================\n\n")
                        self.addDelayBasedOnType(typeOfTask, delay)
                        self.countOnType(typeOfTask)
                        self.HIT_CORRECT_COUNT += 1
                        TouchLogs.remove(touchLog)
                        eventToPlot.remove(candidateEvent)
                    else:
                        print("-----------Wrong Hit----------\n")
                        print(touchLog)
                        print("==============================\n\n")
                        self.HIT_ERROR_COUNT += 1
                        TouchLogs.remove(touchLog)
                    break

        if len(eventToPlot) > 0:
            # print(eventToPlot, len(eventToPlot))
            self.MISS_EVENT_COUNT = len(eventToPlot)
            # eventToPlot.remote()

            # print(len(candidateEvents))


def generate_visualization(input_path, output_path):
    trial = EachTrialResult(input_path)
    trial.calculateResults()
    trial.makePlot(output_path=output_path)

    trial.getOverallAverageDelay()
    trial.getMissEventCount()
    trial.getMissTouchCount()
    trial.getHitCorrectCount()
    trial.getHitErrorCount()
    trial.getTotalNumOfEvents()
    trial.getHitAccuracy()


if __name__ == "__main__":
    input_path = "/Users/rueichechang/UnityProject/My project/Assets/StreamingAssets/OutputJson.json"
    trial = EachTrialResult(input_path)
    trial.calculateResults()