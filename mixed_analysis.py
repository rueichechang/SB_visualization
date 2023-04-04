import statsmodels.formula.api as smf
import pandas as pd
import glob, os, copy
from generate_analysis import EachTrialResult
import researchpy as rp
from statsmodels.sandbox.stats.multicomp import multipletests
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols

sighted_folder = "/Users/rueichechang/Documents/SB_visualization/sighted/"
blind_folder = "/Users/rueichechang/Documents/SB_visualization/blind/"

ID = [str(i) for i in range(1,10)]
scenes = ['scene1', 'scene2', 'scene3']
conditions = ['proxies_data','baseline', 'noise_cancellation']
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
    'VisualFeedback'
]




def create_csv(df, path, person_type):
    # df = pd.DataFrame(columns = header)
    

    for id in ID:    
        for scene in scenes:
            for condition in conditions:
                for logger in loggers:
                    json_file = path + id + "/json_files/"+scene+"/"+condition+"/"+logger+".json"
                    if not os.path.isfile(json_file): print(json_file + " not found")
                    print(json_file)
                    temp_dict = {}
                    temp_dict['BlindOrSighted'] = person_type
                    temp_dict['RandomInterceptByID'] = int(id) if person_type == "blind" else int(id)+9
                    temp_dict['Scene'] = scene
                    temp_dict['Condition'] = condition
                    temp_dict['TrialNumber'] = int(logger[-1])+1

                    eachTrialResult = EachTrialResult(json_file)
                    listToAppend = eachTrialResult.outputForMixedAnalysis()
                    for item in listToAppend:
                        new_dict = copy.deepcopy(temp_dict)
                        new_dict.update(item)
                        df =  pd.concat([df, pd.DataFrame.from_records([new_dict])], ignore_index=True)
                        # df.append(new_dict, ignore_index = True)

                    
    print(df)
                    
    return df 

def getAvgNumOfOverlaps(df):
    BL_NUM = 0
    SB_NUM = 0
    NC_NUM = 0
    BL_OVERLAP_NUM = 0
    NC_OVERLAP_NUM = 0 
    SB_OVERLAP_NUM = 0
    for index, row in df.iterrows():
        if row["Condition"] == "baseline":
            BL_NUM +=1
            BL_OVERLAP_NUM += row["NumOfOverlaps"]
        elif row["Condition"] == "noise_cancellation":
            NC_NUM += 1
            NC_OVERLAP_NUM += row["NumOfOverlaps"]
        elif row["Condition"] == "proxies_data":
            SB_NUM += 1
            SB_OVERLAP_NUM += row["NumOfOverlaps"]
    print(BL_OVERLAP_NUM/BL_NUM)
    print(NC_OVERLAP_NUM/NC_NUM)
    print(SB_OVERLAP_NUM/SB_NUM)



if __name__ == "__main__":

    # pvalues = [0.048, 0.099, 0.96]
   
    # df = pd.DataFrame(columns = header)
    # df = create_csv(df, blind_folder, "blind")
    # df = create_csv(df, sighted_folder, "sighted")
    # df.to_csv('soundblender.csv',index=True)

    soundblender = pd.read_csv('soundblender.csv')    
    soundblender.info()
    print(rp.summary_cont(soundblender.groupby(["BlindOrSighted", "Condition", "Scene"])["Success"]))

    # model = ols("Success ~ C(BlindOrSighted) + C(Scene) + C(Condition)+ TrialNumber", data=soundblender).fit()
    # print(model.summary())


    model = sm.MixedLM.from_formula('Success ~ C(BlindOrSighted) + C(Scene) + C(Condition) + C(SoundType) + C(Scene):C(BlindOrSighted) + C(Condition):C(BlindOrSighted) + C(Scene):C(Condition) + C(Condition):C(SoundType) + TrialNumber', data = soundblender, groups = 'RandomInterceptByID')

    contrast_matrix = [[1, -1, 0], [1, 0, -1]]
    contrast_names = ["proxies_data vs. noise_cancellation", "proxies_data vs. baseline"]

    result = model.fit()
    print(result.summary())

    pairwise_results = result.t_test_pairwise(contrast_matrix, method="t-test")
    print(pairwise_results.summary())


    

   


    # tukey = pairwise_tukeyhsd(endog=soundblender['Success'], groups=soundblender['Condition'], alpha=0.05)
    # print(tukey.summary())

  
    # rejected, p_adjusted, _, alpha_corrected = multipletests(tukey.pvalues, alpha=0.05/3, 
    #                            method='bonferroni', is_sorted=False, returnsorted=False)
    # print("alpha_corrected:", alpha_corrected)
    # print("p_adjusted:", p_adjusted)



    # model = smf.mixedlm('Success ~ C(BlindOrSighted) + C(Scene) + C(Condition, Treatment("noise_cancellation")) + C(SoundType) + C(Scene):C(BlindOrSighted) + C(Condition, Treatment("noise_cancellation")):C(BlindOrSighted) + C(Scene):C(Condition, Treatment("noise_cancellation")) + C(Condition, Treatment("noise_cancellation")):C(SoundType) + TrialNumber', data = soundblender, groups = 'RandomInterceptByID')
                        
    # result = model.fit()
    # print("result.pvalues", result.pvalues)
    # print(result.summary())

    # soundblender = pd.read_csv('soundblender.csv')    
    # soundblender.info()
    # print(rp.summary_cont(soundblender.groupby(["BlindOrSighted", "Condition", "Scene"])["Success"]))
    # model = smf.mixedlm('Success ~ C(BlindOrSighted) + C(Scene) + C(Condition, Treatment("proxies_data")) + C(SoundType) + C(Scene):C(BlindOrSighted) + C(Condition, Treatment("proxies_data")):C(BlindOrSighted) + C(Scene):C(Condition, Treatment("proxies_data")) + C(Condition, Treatment("proxies_data")):C(SoundType) + TrialNumber', data = soundblender, groups = 'RandomInterceptByID')
                        
    # result = model.fit()
    # print(result.summary())
