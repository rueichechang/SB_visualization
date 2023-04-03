import statsmodels.formula.api as smf
import pandas as pd
import glob, os, copy
# from generate_analysis import EachTrialResult

ID = [str(i) for i in range(1,10)]
scenes = ['scene1', 'scene2', 'scene3']
conditions = ['baseline', 'noise_cancellation', 'proxies_data']
loggers = ['logger_0', 'logger_1', 'logger_2', 'logger_3', 'logger_4']

header = [
    'BlindOrSighted', 
    'RandomInterceptByID',
    'Scene', 
    'Condition',
    'TrialNumber',

    'Success',
    'Delay',

    'SoundType',
    'NumOfOverlaps',
    'OverlapRWVR',
    'OverlapFP',
]


if __name__ == "__main__":
    # df = pd.DataFrame(columns = header)
    # df = create_csv(df, blind_folder, "blind")
    # df = create_csv(df, sighted_folder, "sighted")
    # df.to_csv('soundblender.csv',index=True)


    soundblender = pd.read_csv('soundblender.csv')    
    # model = smf.mixedlm('Success ~ C(OverlapFP)', data = soundblender, groups = 'RandomInterceptByID')
    model = smf.mixedlm('Success ~ C(BlindOrSighted) + C(Scene) + C(Condition) + C(SoundType) + NumOfOverlaps + C(OverlapRWVR) + C(OverlapFP) + C(Condition):C(BlindOrSighted) + C(Condition):C(Scene) + C(Condition):C(SoundType) + C(Condition):NumOfOverlaps + C(Condition):C(OverlapRWVR) + C(Condition):C(OverlapFP)', data = soundblender, groups = 'RandomInterceptByID')
    result = model.fit()
    print(result.summary())