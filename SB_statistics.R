library(gplots)
data <- read.csv("/Users/rueichechang/Documents/SB_visualization/soundblender.csv", stringsAsFactors = F)
names(data) <- c('BlindOrSighted', 
                 'RandomInterceptByID',
                 'Scene', 
                 'Condition',
                 'TrialNumber',
                 'Success',
                 'Delay',
                 'SoundType',
                 'NumOfOverlaps',
                 'OverlapRWVR',
                 'OverlapFP')
summary(data)
