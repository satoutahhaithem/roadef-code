import numpy as np


conferenceSession = np.arange(1,41)
print (conferenceSession)

workingGroup = np.arange(1,21)
print (workingGroup)

workingGroupNames= ["TADJ","DAAO","ROSA","ROET","ROES","DOR","META","GT2L","OR","CAGDO","ORIGIN","P2LS",
"ROQ","ATOM","ROCT","GOTHA","POC","SCALE","COSMOS","OM"]
print (workingGroupNames)

SlotsParrallelSession = np.arange(1,8)
print(SlotsParrallelSession)

possibleAmountOfPapers = np.arange(3,7)
print(possibleAmountOfPapers)

maxparallelSession = 11

authorizedPapersForEachSlots = {
    1:4,
    2:6,
    3:6,
    4:4,
    5:4,
    6:5,
    7:3
}
print (authorizedPapersForEachSlots)

affectationMatrix = np.zeros((7,11))