
# -*- coding: utf-8 -*-
"""
CONTINUOUS ASSESSMENT

Created on Sun Mov 20 2022

Instructors: Antoine NOEL 

Group Members:
    1. Amin ILYAS
    2. Nico Benedikt HORSTMANN
    3. Pritam RITU RAJ
    4. Sayanna MUKHERJEE 
    5. Zahi SAMAHA

Corporation: 
    Unilever (UN)

Starting Date:
    08/03/1998

Ending Date:
    04/30/1999


"""
#%%
#STEP 2

# working with TAQ data step 2

# The quote file

import numpy as np
import pandas as pd #we saved it as pd as this is the convention
#import datetime as dt
import matplotlib.pyplot as plt

from datetime import datetime

################################################################################
################### Quotes file transformation #################################

df1 = pd.read_excel("UN_quotes_full.xlsx",
                   sheet_name="UN_quotes_full", 
                   header=0, index_col=None,
                   dtype={'Name': str, 'Value' : float})

df2 = pd.read_excel("UN_trades_full.xlsx", #I use a relative file path here and set my working directory
                       sheet_name="UN_trades_full", 
                       header=0, index_col=None,
                       dtype={'Name': str, 'Value' : float})

def MyDailyStats(Tfile,yyyy,mm,dd):
    #Select one day
    smaller_Quote = df1[df1["DATE"] == pd.Timestamp(year=yyyy, month=mm, day=dd, hour=00)]
     
    #Drop values smaller than or equal to zero
    smaller_Quote.drop(smaller_Quote[smaller_Quote["BID"] <= 0].index, inplace = True)
    
    smaller_Quote.drop(smaller_Quote[smaller_Quote["OFR"] <= 0].index, inplace = True)
    
    smaller_Quote.drop(smaller_Quote[smaller_Quote["BIDSIZ"] <= 0].index, inplace = True)
    
    smaller_Quote.drop(smaller_Quote[smaller_Quote["OFRSIZ"] <= 0].index, inplace = True)
    
    #Select the time
    #Please ignore transactions
    #before 9:30 am and beyond 4:00 pm
    #We are using here two conditions such that only the observations with occurred
    #between 9:30 am and before 4:00 pm on the respective trading day remain in the
    #sample
    #I assign the remaining observations to the DataFrame smaller_Quote_t_ignore
    #Such that we know that we ignored certain trading times (t)
    Time1 = datetime.strptime('09:30:00', '%H:%M:%S').time()
    Time2 = datetime.strptime('16:00:00', '%H:%M:%S').time()
    
    
    smaller_Quote_t_ignore = smaller_Quote[(smaller_Quote["TIME"]>= Time1) &
                                   (smaller_Quote["TIME"] <= Time2)]
    
    ###############################################################################
    ############################ Trade file transformation ########################

    
    #Select one day
    smaller_Trade = df2[df2["DATE"] == pd.Timestamp(year=yyyy, month=mm, day=dd, hour=00)]
    
    #Select observations between 9:30 am and 4  for the Trade File
    smaller_Trade_t_ignore = smaller_Trade[(smaller_Trade["TIME"]>= Time1) &
                                   (smaller_Trade["TIME"] <= Time2)]
    
    
    #%%
    
    # STEP 3
    
    ###Market maker###
    
    
    theday = pd.Timestamp(year=yyyy, month=mm, day=dd, hour=00)
    
    
    k1 = smaller_Quote_t_ignore.values[:,1] == theday
    # Optional: Filters
    k2 = smaller_Quote_t_ignore.values[:,3] > 0  # bid
    k3 = smaller_Quote_t_ignore.values[:,4] > 0  # bid size
    k4 = smaller_Quote_t_ignore.values[:,5] > 0  # ask
    k5 = smaller_Quote_t_ignore.values[:,6] > 0  # ask size
    K = k1 & k2 & k3 & k4 & k5 
    bid = smaller_Quote_t_ignore.values[K,3] 
    ask = smaller_Quote_t_ignore.values[K,4]
    mm = smaller_Quote_t_ignore.values[K,9]
    
    def MyDailyStats2(db,yyyy,mm,dd):
        theday = pd.Timestamp(year=yyyy, month=mm, day=dd, hour=00)
        k1 = db.values[:,1] == theday
        k2 = db.values[:,3] > 0  # bid
        k3 = db.values[:,4] > 0  # bid size
        k4 = db.values[:,5] > 0  # ask
        k5 = db.values[:,6] > 0  # ask size
        K = k1 & k2 & k3 & k4 & k5 
        hms = db.values[K,2]
        bid = db.values[K,3] 
        ask = db.values[K,4]
        mm = db.values[K,9]
        beg_time = min(hms)
        end_time = max(hms)
        bestbid = np.max(bid)
        bestask = np.min(ask)
        avebalvl = np.mean(ask-bid)
        avebaper = np.mean((ask-bid)/(0.5*(ask+bid)))
        print('Trading day:',theday)
        print('Time range: From',beg_time,'to',end_time)
        print('Best bid of the day:',np.round(bestbid,2))
        print('Best ask of the day:',np.round(bestask,2))
        print('Average bid ask spread ($):',np.round(avebalvl,2))
        print('Average bid ask spread (%):',np.round(100*avebaper,4))
        print('')
    
    ############################### Spread by market maker
    
    # Market maker identity
    #   SHAW: Shaw (D.E.) Securities
    #   OLDE: 
    #   TRIM: Trimark Securities
    #   CAES: NASD Market Services, Inc.
    #   MADF: Bernard Madoff 
    
    ba_mm = np.empty(5)
    
    m1 = mm == 'SHAW' 
    if np.sum(m1) > 0:
        ba_mm[0] = np.mean(ask[m1]-bid[m1])
    else:
        ba_mm[0] = np.nan  
    m2 = mm == 'OLDE' 
    if np.sum(m2) > 0:
        ba_mm[1] = np.mean(ask[m2]-bid[m2])
    else:
        ba_mm[1] = 0 
    m3 = mm == 'TRIM' 
    if np.sum(m3) >0:
        ba_mm[2] = np.mean(ask[m3]-bid[m3])
    else:
        ba_mm[2] = np.nan
    m4 = mm == 'CAES' 
    if np.sum(m4) > 0: 
        ba_mm[3] = np.mean(ask[m4]-bid[m4])
    else:
        ba_mm[3] = np.nan
    m5 = mm == 'MADF' 
    if np.sum(m5) > 0:
        ba_mm[4] = np.mean(ask[m5]-bid[m5])
    else:
        ba_mm[4] = np.nan
    
    x = np.arange(5)
    trng = ('SHAW','OLDE','TRIM','CAES','MADF')
    plt.subplot(1,2,2)
    plt.bar(x,ba_mm)
    plt.title('Average spread by market maker')
    plt.xlabel('Market makers')
    plt.ylabel('Spread in dollars')
    plt.xticks(x, trng,fontsize=8)
    plt.show()
    
    np.sum(ask[m1]>0) # 2
    np.sum(ask[m2]>0) # 0
    np.sum(ask[m3]>0) # 641
    np.sum(ask[m4]>0) #
    np.sum(ask[m5]>0) # 206
    len(np.unique(ask[m3]-bid[m3])) # 6
    #len(np.unique(ask[m5]-bid[m5])) # 8
    
    #We concluded that the most active market maker is TRIM because it is the one with the lowest average spread
    #print(smaller_Quote_t_ignore)
    smaller_Quote_t_ignore.drop(smaller_Quote_t_ignore[smaller_Quote_t_ignore["MMID"] != "TRIM"].index
                                , inplace = True)
    #print(smaller_Quote_t_ignore)
    
    #Combining the DATE and TIME columns here of the repective DataFrames into a Date column
    #https://stackoverflow.com/a/49668702
    df3 = smaller_Trade_t_ignore.copy()
    df3.loc[:,"Date"] = pd.to_datetime(df3.DATE.astype(str)+' '+df3.TIME.astype(str))
    df3.drop(["DATE", "TIME"], axis = 1, inplace = True) #Here we drop the old DATE and TIME
    #columns as they are not needed anymore
    
    df4 = smaller_Quote_t_ignore.copy()
    df4.loc[:,"Date"] = pd.to_datetime(df4.DATE.astype(str)+' '+df4.TIME.astype(str))
    df4.drop(["DATE", "TIME"], axis = 1, inplace = True) #Here we drop the old DATE and TIME
    #columns as they are not needed anymore
    
    #merging the two datframes and delaying the trades
    merged_total = pd.merge_asof(df3, df4, on= "Date"
                                 , direction = "backward")
    #print(merged_total)
    ######################################Calculation of the merged_total###############################################################
    #NEXT remove NaN (because of the first line) or remove the first line
    #Afterwards do STEP 4!!!
    
    #%%
    
    #STEP 4: (DONE)
    
    #Now, for each transaction, you have now a prevailing bid and a prevailing ask.
    #You can now classify trades. To do so, please implement the CLNV algorithm (slide 108).
    
    #Create some arrays here
    
    #STEP 4 CLNV algorithm
    #Define the Bid-Ask-Spread 
    merged_total["Spread"] = merged_total["OFR"] - merged_total["BID"] 
    
    #Define the 30% away form bid price point, Midpoint and 70% away from Bid price point
    
    merged_total["30point"] =merged_total["OFR"] - merged_total["Spread"].mul(0.70) #mul multiples all values with in this cas by 0.70 of the respective column
    merged_total["Midpoint"] =merged_total["OFR"] - merged_total["Spread"].mul(0.50)
    merged_total["70point"] =merged_total["OFR"] - merged_total["Spread"].mul(0.30)
    
    #1: buyer, 0: sellers
    
    #Above ask and Tick Rule (comparing the trade with the previous trade) (Above ask buyers)
    merged_total["buyer1"] = np.where((merged_total["PRICE"] > merged_total["OFR"]) & 
                                     (merged_total["PRICE"] > merged_total["PRICE"].shift()), 1, 0)
    
    #Quote Rule at ask (At Ask Buyers)
    merged_total["buyer2"] = np.where((merged_total["PRICE"] == merged_total["OFR"]), 1, 0)
    
    #Quote rule 30% below ask and not greater than ask (Up to 30 below Ask Buyers)
    merged_total["buyer3"] = np.where((merged_total["PRICE"] >=
    merged_total["70point"]) & (merged_total["PRICE"] <  merged_total["OFR"]), 1, 0)
    
    #Tick rule < 70 Point and > Mid point (in between) (Up to 20 % above the mid point buyers)
    merged_total["buyer4"] = np.where((merged_total["PRICE"] <
    merged_total["70point"]) & (merged_total["PRICE"] >  merged_total["Midpoint"]) & 
                                (merged_total["PRICE"] > merged_total["PRICE"].shift()), 1, 0)
    
    #Tick rule > 30 Point and < Mid point (in between) (Up to 20 % below the mid point buyers)
    merged_total["buyer5"] = np.where((merged_total["PRICE"] >
    merged_total["30point"]) & (merged_total["PRICE"] <  merged_total["Midpoint"]) & 
                                (merged_total["PRICE"] > merged_total["PRICE"].shift()), 1, 0)
    
    #Quote rule < = 30% point > than bid Quote rule (Up to 30% above the Bid buyers)
    merged_total["buyer6"] = np.where((merged_total["PRICE"] <=  merged_total["30point"]) 
                                      & (merged_total["PRICE"] >= merged_total["BID"]), 1, 0)
    
    #Tick rule Below bid and Tick Rule (comparing the trade with the previous trade) (Below Bid Buyers)
    merged_total["buyer7"] = np.where((merged_total["PRICE"] < merged_total["BID"]) & 
                                     (merged_total["PRICE"] > merged_total["PRICE"].shift()), 1, 0)
    #Create one column with all buyers
    merged_total["Total_buyers"] = merged_total["buyer1"] + merged_total["buyer2"]+merged_total["buyer3"] + merged_total["buyer4"] + merged_total["buyer5"]+ merged_total["buyer6"] + merged_total["buyer7"]
    
    #Create one column with all buyers
    merged_total["Total_sellers"] = np.where((merged_total["Total_buyers"] == 1),0, 1) #changed
    
   #%%
   
    ###################################### The function ############################################
    # A function to generate the most important stats per day
    
    #STEP 5
    size= merged_total["BID"].count() #I use the bid here because of the first row. Because we don´t have a prevailing bid and ask price in the first row
    
    inside_quotes_including_bid_ask = np.sum((merged_total["PRICE"]<= merged_total["OFR"]) & (merged_total["PRICE"] >= merged_total["BID"]))/size                                  
    inside_quotes_including_bid_ask = inside_quotes_including_bid_ask * 100 #to get percentages                         
    
    outside_quotes = 100 - inside_quotes_including_bid_ask
    
    real_inside_quotes = (np.sum((merged_total["PRICE"] < merged_total["OFR"]) & (merged_total["PRICE"] > merged_total["BID"]))/size)*100                                 
    #Proportion at the quotes
    At_Ask = (np.sum(merged_total["PRICE"] == merged_total["OFR"])/size)*100
    At_Mid = (np.sum(merged_total["PRICE"] == merged_total["Midpoint"])/size)*100
    At_Bid = (np.sum(merged_total["PRICE"] == merged_total["BID"])/size)*100
    
    
    #Daily weighted average effective spread
    #step6
    #Calcculation of the Effective Spread
    merged_total["Effective_spread"] = abs(merged_total["PRICE"] - merged_total["Midpoint"])
    
    #Weighted effective spread
    merged_total["W_EF"]= merged_total["Effective_spread"] * merged_total["SIZE"] * merged_total["PRICE"]
    
    #Step 8 orderflow imbalance
    
    OFI_Data = pd.concat([merged_total["Total_buyers"], merged_total["Total_sellers"], merged_total["PRICE"], merged_total["SIZE"]], axis = 1) #changed


    OFI_Data["BIT"] = OFI_Data.Total_buyers[OFI_Data["Total_buyers"] == 1] * OFI_Data["SIZE"] * OFI_Data["PRICE"]

    OFI_Data["SIT"] = OFI_Data.Total_sellers[OFI_Data["Total_sellers"] == 1] *  OFI_Data["SIZE"] * OFI_Data["PRICE"]


    BIT= np.sum(OFI_Data["BIT"])
    SIT= np.sum(OFI_Data["SIT"])

    OFI = (BIT-SIT)/((BIT + SIT)/2)
    
    
    #Get The Ticker
    ticker = df1["SYMBOL"].unique()
    
 
    
    #OFI.plot()
    
    print('Ticker:', ticker)
    print('Trading day:',theday)
    print("The proportion of trades inside the quotes including Bid and Ask: ",round(inside_quotes_including_bid_ask, 2), "%") #97.70%
    print("The proportion of trades outside of the quotes: ",round(outside_quotes,2), "%") #2.30%
    print("The proportion of trades inside the quotes (without bid and ask): ", round(real_inside_quotes,2), "%") #69.91%
    print("The proportion of trades at the Ask Quote: ",round(At_Ask, 2), "%") #6.90% 
    print("The proportion of trades at the Mid Quote: ", round(At_Mid, 2), "%") #14.87%
    print("The proportion of trades at the Bid Quote: ", round(At_Bid, 2), "%") #20.88%
    print("The weighted average effective spread: ", round(np.mean(merged_total["W_EF"]),2)) 
    print("The Order Flow Imbalance is: ", round(OFI, 2))
    print('=========================================')
    
    return OFI, np.mean(merged_total["Effective_spread"])
   
MyDailyStats(df1, 1999, 2, 5) #doing everything for one day
 
#%%

#STEP 7 and 8 (plotting)
#Doing everything for all trading days

u_date = df1["DATE"].unique()

L = len(u_date)

yyyy = pd.DatetimeIndex(u_date).year
mm = pd.DatetimeIndex(u_date).month
dd = pd.DatetimeIndex(u_date).day
#create an empty array to get the values returned by the function
OFI = []

for i in range(L):
    OFI.append(MyDailyStats(df1,yyyy[i],mm[i],dd[i]))

#plotting

OFI_EF_Data = pd.DataFrame(OFI)

OFI_EF_Data["Date"] = u_date

OFI_EF_Data.columns = ["OFI", "Mean Effective spread", "Date"]
#The plot for the OFI time series


OFI_EF_Data.plot(x= "Date", y = "OFI",xlabel = "DAY", ylabel = "OFI", title = "Order Flow Imbalance per trading day",legend = None
         , fontsize = 10)

#The plot for the Effective spread time series
OFI_EF_Data.plot(x= "Date", y = "Mean Effective spread",xlabel = "DAY", ylabel = "Mean Effective spread", title = "Mean Effective spread per trading day",legend = None
         , fontsize = 10)

OFI_EF_Data.plot(subplots= True, x = "Date")







    
    
#####################################################################################################


  
