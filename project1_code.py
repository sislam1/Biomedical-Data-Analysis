import json
import os

import util_5353
import pandas as pd
import numpy as np
import lxml.etree as et

# Load the data into whatever data structure you see fit.  You can leave it in
# the csv format, use a custom data structure, or (best idea) use a pandas
# frame.  I would suggest any basic data modifications (certainly any
# file-specific modifications) be handled here. Hint: there are lots of
# extraneous spaces in the data that you're going to want to remove
load_data_count = 0
def load_data(filename):
  global load_data_count
  load_data_count += 1
  if load_data_count >= 5:
    print('WARNING: load_data called too many times')
  data = None
  # Begin CODE
  # read in file as a pandas dataframe
  # there are columns and rows with NaN in their entirety. get rid
  # of those rows and columns and then reset index so that the dataset
  # is zero-based. Perform further data cleaning 
  data = pd.read_csv(filename)
  data.dropna(axis='columns', how='all', inplace=True)
  data.dropna(axis='rows', how='all', inplace=True)
  data.drop([0], inplace=True) # first line in dataset seems to just have year; not needed
  data.columns = data.columns.str.replace(' ', '')
  data = data[data['CONAME'].str.contains('County')] # extract rows where CONAME contains the word County
  data['CONAME'] = data['CONAME'].str.strip() # strip leading and trailing spaces in CONAME
  data.replace(',','', regex=True, inplace=True) 
  data.replace('%','', regex=True, inplace=True)
  data.replace('\$','', regex=True, inplace=True)
  data.replace('---',np.nan, regex=True, inplace=True)
  data.replace('\#REF\!',np.nan, regex=True, inplace=True)
  data.replace('- ',np.nan, regex=True, inplace=True)
  data.replace('\#DIV\/0\!',np.nan, regex=True, inplace=True)
  data.iloc[:, 2:] = data.iloc[:, 2:].apply(pd.to_numeric)
  data.reset_index(drop=True, inplace=True) # reset index to be zero-based
  # End CODE
  return data

# Return the name of the county at the given (zero-based) index in the dataset.
# Note: this should be done entirely with code. Hard-coding values, e.g.,
# "return 'Austin County'" is not a smart move at all...
def county_at_index(data, index):
  county_name = None
  # Begin CODE
  county_name = data.at[index,'CONAME']
  # End CODE
  return county_name

# Return the number of counties in the dataset.
def num_counties(data):
  num = None
  # Begin CODE
  num = data['CONAME'].nunique()
  # End CODE
  return num

# return the population of the county
def county_pop(data, county):
  pop = None
  # Begin CODE
  pop = data.loc[data['CONAME'] == county, 'TOTPOP'].item()
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 1: \n'+ str(pop) + '\n\n')
  f.close()
  return pop

# return counties with highest percentage of anglo, black, hispanic and other ethnic groups.
# in case of ties, choose in alphabetic order
def highest_ethnic_counties(data):
  highest = {}
  # Begin CODE
  angMaxVal = data['POPANGPC'].max()
  angpc = data.loc[data['POPANGPC'] == angMaxVal, 'CONAME'].sort_values().values[0]
  blMaxVal = data['POPBLPCT'].max()
  blpc = data.loc[data['POPBLPCT'] == blMaxVal, 'CONAME'].sort_values().values[0]
  hisMaxVal = data['POPHISPC'].max()
  hispc = data.loc[data['POPHISPC'] == hisMaxVal, 'CONAME'].sort_values().values[0]
  othMaxVal = data['POPOTHPC'].max()
  othpc = data.loc[data['POPOTHPC'] == othMaxVal, 'CONAME'].sort_values().values[0]
  highest = {'Anglos':angpc, 'Blacks':blpc, 'Hispanics':hispc, 'Other':othpc}
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 2: \n'+ str(highest) + '\n\n')
  f.close()
  return highest

# return a 2-tuple with the names of the counties with the highest 
# female and male percentages, respectively
def highest_sex_counties(data):
  highest = None
  # Begin CODE
  # find the maximum percentage. Then find which CONAME(s) have that max value
  # in POPTFMPC or POPTMPC column. Sort these in alphabetic order to return the first 
  # one
  femMaxVal = data['POPTFMPC'].max()
  femCo = data.loc[data['POPTFMPC'] == femMaxVal, 'CONAME'].sort_values().values[0]
  maleMaxVal = data['POPTMPC'].max()
  maleCo = data.loc[data['POPTMPC'] == maleMaxVal, 'CONAME'].sort_values().values[0]
  highest = tuple([femCo, maleCo])
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 3: \n'+ str(highest) + '\n\n')
  f.close()
  return highest

# return a 2-tuple with the names of the counties with the highest and lowest specific
# disease death rates, respectively. This function is called by other functions.
def low_high_dis_counties(data, column):
  # find the maximum and minimum death rate values. Then find which CONAME(s) have that 
  # max and min values in column of interest. Sort these in alphabetic order to return the
  # first one.
  disMaxVal = data[column].max(skipna=True)
  disMaxCo = data.loc[data[column] == disMaxVal, 'CONAME'].sort_values().values[0]
  disMinVal = data[column].min(skipna=True)
  disMinCo = data.loc[data[column] == disMinVal, 'CONAME'].sort_values().values[0]
  lowhigh = tuple([disMaxCo, disMinCo])
  return lowhigh

# return a 2-tuple with the names of the counties with the highest and lowest heart 
# disease death rates, respectively. Calls low_high_dis_counties function.
def low_high_heartdisease_counties(data):
  lowhigh = None
  # Begin CODE
  lowhigh = low_high_dis_counties(data, 'HRTDEART')
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 4: \n'+ str(lowhigh) + '\n\n')
  f.close()
  return lowhigh

# return a 2-tuple with the names of the counties with the highest and lowest lung 
# cancer death rates, respectively. Calls low_high_dis_counties function.
def low_high_lungcancer_counties(data):
  lowhigh = None
  # Begin CODE
  lowhigh = low_high_dis_counties(data, 'LNGCANDR')
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 5: \n'+ str(lowhigh) + '\n\n')
  f.close()
  return lowhigh

# return a 10-tuple with the names of the counties with the five highest and five lowest, 
# specific injury or death rates, respectively. This function is called by other functions.
def low_high_inj_death_counties(data, column):
  # Find the 5 maximum and 5 minimum injury or death rate values. 
  # Then find which CONAME values have those max and min values in specific column of interest.
  # Sort these in alphabetic order to return the first one, in case of ties.
  # A list of length 5 stores the max values and another one stores the min values. These
  # are concatenated into a 10-elecment list and returned as a tuple
  maxCo = []
  minCo = []
  maxVal = list(data[column].nlargest(5).iloc[0:])
  minVal = list(data[column].nsmallest(5).iloc[0:])
  for i in range(len(maxVal)):
    maxCo.append(data.loc[data[column] == maxVal[i], 'CONAME'].sort_values().values[0])
    minCo.append(data.loc[data[column] == minVal[i], 'CONAME'].sort_values().values[0])
  injList = maxCo+minCo
  lowhigh = tuple(injList)
  return lowhigh

# return a 10-tuple with the names of the counties with the five highest and five lowest, 
# motor injury rates, respectively. Calls low_high_counties function
def low_high_motorinjury_counties(data):
  lowhigh = None
  # Begin CODE
  lowhigh = low_high_inj_death_counties(data, 'MVDEART')
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 6: \n'+ str(lowhigh) + '\n\n')
  f.close()
  return lowhigh

# return a 10-tuple with the names of the counties with the five highest and five lowest, 
# suicide rates, respectively. Calls low_high_counties function
def low_high_suicide_counties(data):
  lowhigh = None
  # Begin CODE
  lowhigh = low_high_inj_death_counties(data, 'SUIDEART')
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 7: \n'+ str(lowhigh) + '\n\n')
  f.close()
  return lowhigh

# return the county with the most average monthly food stamp participants relative to 
# (i.e., divided by) the number of persons living below the poverty line
def most_relative_foodstamp_county(data):
  county_name = None
  # Begin CODE
  maxVal = data['FSPARTIC']/data['POVTOT']
  maxVal = maxVal.max()
  county_name = data.loc[data['FSPARTIC']/data['POVTOT'] == maxVal, 'CONAME'].values[0]
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 8: \n'+ str(county_name) + '\n\n')
  f.close()
  return county_name

# return the county with the biggest single-year jump in pertussis rates (measured as Y2 – Y1). 
# Limit to counties with at least 10 cases per year in both years. This is designed to measure 
# the most surprising outbreak of a contagious disease. Note that data_list is a list containing 
# each year. Assume the list is properly ordered.
# include only those with >= 10 cases
# data_list can be of any length between 2 and 4. 
def biggest_pertussis_jump(data_list):
  county_name = None
  county_dict = {}
  # Begin CODE
  # this is first year
  df_p1 = data_list[0].loc[data_list[0]['PERTNO']>=10, ['CONAME', 'PERTRATE']]
  # loop through rest of data_list and for every year, find the difference between
  # PERTNO from this year and the previous year. Then find max value and corresponding
  # county. Store these in a dictionary. Once loop is complete for all years, find
  # maximum value from dictionary and corresponding key
  for i in range(1, len(data_list)):
    df_p2 = data_list[i].loc[data_list[i]['PERTNO']>=10, ['CONAME', 'PERTRATE']]
    # inner join the 2 dataframes so that we include counties where PERTNO >= 10 
    # in BOTH years
    df_p = pd.merge(df_p1, df_p2, on=['CONAME'])
    maxVal = (df_p['PERTRATE_y']-df_p['PERTRATE_x']).max()
    cname = df_p.loc[df_p['PERTRATE_y']-df_p['PERTRATE_x'] == maxVal, 'CONAME'].values[0]
    county_dict[cname] = maxVal
    df_p1 = df_p2
  # End CODE
  county_name = max(county_dict, key=county_dict.get)
  f = open('project1.txt', 'w')
  f.write('Problem 9: \n'+ str(county_name) + '\n\n')
  f.close()
  return county_name

# the following function is used in problem 10. This function calculates a weighted 
# average (micro-average). This will be used in problem 10.
def wavg(group, avg_name, weight_name):
    d = group[avg_name]
    w = group[weight_name]
    return round(((d/100) * w).sum() / w.sum(), 3)

# return a dict with the average low birth rate % (micro-averaged by live births) 
# in counties with at least 100 live births, stratified by the % of people 18-64 without 
# health insurance, in 10% increments
def mean_lowbirth_noinsurance(data):
  rates = {}
  # Begin CODE
  # create a list of insurance bins that will be used as keys for the return dictionary 
  insBinVec = ['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
  # only include counties with >= 100 live births
  df_birth = data.loc[data['LIVEBIR']>=100, ['CONAME', 'LIVEBIR', 'LBWPCT', 'NOHI1864', 'NOHI1864POP']]
  # calculate % of people without health insurance. NOTE: The columns NOHILT18 is not correct in the
  # dataset. Therefore, this is being calculated in the code
  df_birth['NOHI1864PCT'] = round(df_birth['NOHI1864']/df_birth['NOHI1864POP']*100, 1)
  # bin the insurance % into 0-10%, 10.1-20%, 20.1-30%, ..., 90.1-100%. Note that the 
  # pd.cut function starts at 0 and ends at 101. The increment is 10. The left limit is not 
  # inclusive, but right limit is. We have also rounded % of people without health insurance
  # to 1 decimal place. So, insurance bins are set appropriately.
  df_birth['INSBIN'] = pd.cut(df_birth['NOHI1864PCT'], np.arange(0, 101, 10), right=True)
  # grouping by insurance bins, calculate micro average using above function
  df_lbrt = df_birth.groupby('INSBIN', as_index=False).apply(wavg, 'LBWPCT', 'LIVEBIR')
  # rename insurance bins so that keys of return dictionary are in correct format
  df_lbrt['INSBIN'] = insBinVec
  # some insurance bins don't have any values. Drop those
  df_lbrt.dropna(inplace=True)
  df_lbrt.reset_index(inplace=True, drop=True)
  # set the keys and values of the return dictionary
  keyList = list(df_lbrt['INSBIN'])
  valList = list(df_lbrt.iloc[:,1])
  for i in range(len(keyList)):
        rates[keyList[i]] = valList[i]
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 10: \n'+ str(rates) + '\n\n')
  f.close()
  return rates

# write an XML file with the given filename (the current directory) with the root element 
# named CountyEmploymentInfo, having a child element for each county named County. The County 
# element should have an attribute name, which is the name of the county, and the 
# following elements: Population, LaborForce, Unemployed, and PerCapitaIncome
# Note: I'd recommend lxml.etree over xml.etree.ElementTree, it has all the
# same functionality plus more, including write(file, pretty_print=True)
def employment_xml(data, filename):
  # Begin CODE
  root = et.Element('CountyEmploymentInfo')
  for row in data.index:
        child1 = et.SubElement(root, 'County',  attrib={'name': data.loc[row, 'CONAME']})
        for item in [['Population', 'TOTPOP'], ['LaborForce', 'LaborForce'], ['Unemployed', '#UnEmp'], ['PerCapitaIncome', 'PCPI']]:
              el1 = et.SubElement(child1, item[0])
              el1.text = str(data.loc[row, item[1]]) # return values as text
  tree = et.ElementTree(root)
  tree.write(filename, pretty_print=True)
  # End CODE
  f = open('project1.txt', 'w')
  f.write('Problem 11: Check XML file \n\n')
  f.close()
  return

# write a JSON file with the given filename (the current directory) that maps seven 
# infectious diseases (tuberculosis, syphilis, gonorrhea, chlamydia, pertussis, varicella, 
# and aids) to the yearly frequencies in each county for all the years in the given data_list
# Note: for nice printing, the json library has sort_keys and indent parameters
# in the dump method.
def infectious_json(data_list, filename):
  # Begin CODE
  # create dataframe with relevant columns from data_list[0]. Loop through next data file and start
  # by merging relevant columns with the previously created dataframe. Convert all values to
  # comma separated string. Before entering next for loop, save this dataframe as the one
  # that needs to be merged with the next data file.
  df1 = pd.DataFrame()
  df_dis = pd.DataFrame()  
  dis_list = ['TBNO', 'SYPHNO', 'GONNO', 'CHLAMNO', 'PERTNO', 'VARICNO', 'AIDSNO']
  dis_name_list = ['tuberculosis', 'syphilis', 'gonorrhea', 'chlamydia', 'pertussis', 'varicella', 'aids']
  col_list_dis = ['CONAME'] + dis_list
  col_list_dis_name = ['County'] + dis_name_list
  df1['CONAME'] = data_list[0]['CONAME']
  # make sure that values in all the disease columns do not appear as float
  df1[dis_list] = data_list[0][dis_list].astype(int) 
  for i in range(1, len(data_list)):   
    # make sure that values in all the disease columns do not appear as float 
    data_list[i][dis_list].astype(int)
    df2 = pd.merge(df1, data_list[i][col_list_dis], on='CONAME', how='outer')
    df_dis['CONAME'] = df2['CONAME']
    # concatenate values into a comma separated string
    for i in dis_list:
      df_dis[i] = df2[i+'_x'].astype(str)+','+df2[i+'_y'].astype(str)
    df1 = df_dis
  # convert comma separated string to list
  for i in dis_list:
    df_dis[i] = df_dis[i].apply(lambda x: [int(y) for y in x.split(',')])
  # renaming columns based on requirements
  df_dis.columns = col_list_dis_name  
  # will be doing a columns orientation for creating json object. So set index of dataframe 
  # to be County.
  df_dis.set_index('County', drop=True, inplace=True)
  json_data = df_dis.to_json(orient = 'columns') # this will create json based on the column (disease) values
  parsed = json.loads(json_data)
  # NOTE: the indent option indents each field of the JSON file for nicer printing. HOWEVER, the values which
  # are lists (e.g. [4, 1]), get split into 2 separate lines. I looked online, but couldn't find a clean solution
  # for this. A messy option would be to turn the list into a string, use regular expressions to get rid of 
  # quotes and then print. I don't find that option particularly appealing.
  json_str = json.dumps(parsed, indent=2, sort_keys=True) 
  # Writing to sample.json
  with open(filename, "w") as outfile:
    outfile.write(json_str)
  f = open('project1.txt', 'w')
  f.write('Problem 12: check json file \n\n')
  f.close()
  # End CODE

## MAIN ##
if __name__ == '__main__':
  print('::: Loading data :::')
  data = {}
  for year in range(2006, 2010):
    data[year] = load_data('Data File for Texas Health Facts %d.csv' % year)

  print('::: Name of county at given index (eg. 2006, index 0):::')
  zeroB_ret = county_at_index(data[2006], 0)
  print(zeroB_ret)

  print('::: Number of counties in dataset (eg. 2006) :::')
  zeroC_ret = num_counties(data[2006])
  print(zeroC_ret)

  print('::: Population of county :::')
  one_ret = county_pop(data[2006], 'Bowie County')
  print(':::   Bowie County Population: ' + str(one_ret))

  print('::: Counties with most minorities :::')
  two_ret = highest_ethnic_counties(data[2006])
  print(':::   2006 Highest County for \'Anglos\':    ' + str(two_ret['Anglos']))
  print(':::   2006 Highest County for \'Blacks\':    ' + str(two_ret['Blacks']))
  print(':::   2006 Highest County for \'Hispanics\': ' + str(two_ret['Hispanics']))
  print(':::   2006 Highest County for \'Other\':     ' + str(two_ret['Other']))

  print('::: Counties with most females and males, respectively :::')
  three_ret = highest_sex_counties(data[2006])
  print(':::   2006 Highest County for \'Female\': ' + str(three_ret[0]))
  print(':::   2006 Highest County for \'Male\':   ' + str(three_ret[1]))

  print('::: Counties with highest and lowest heart disease rates, respectively :::')
  four_ret = low_high_heartdisease_counties(data[2006])
  print(':::   2006 Highest County for Heart Disease: ' + four_ret[0])
  print(':::   2006  Lowest County for Heart Disease: ' + four_ret[1])

  print('::: Counties with highest and lowest lung cancer rates, respectively :::')
  five_ret = low_high_lungcancer_counties(data[2006])
  print(':::   2006 Highest County for Lung Cancer: ' + five_ret[0])
  print(':::   2006  Lowest County for Lung Cancer: ' + five_ret[1])

  print('::: Counties with 5 highest and 5 lowest motor injury rates :::')
  six_ret = low_high_motorinjury_counties(data[2006])
  print(':::   2006 Highest Counties for Motor Injury:')
  for i in range(5):
    print(':::    ' + str(i+1) + '. ' + six_ret[i])
  print(':::   2006 Lowest Counties for Motor Injury:')
  for i in range(4):
    ir = 5 + i
    print(':::    N-' + str(5-i-1) + '. ' + six_ret[ir])
  print(':::    N.   ' + six_ret[-1])

  print('::: Counties with 5 highest and 5 lowest suicide rates :::')
  seven_ret = low_high_suicide_counties(data[2006])
  print(':::   2006 Highest Counties for Suicide:')
  for i in range(5):
    print(':::    ' + str(i+1) + '. ' + seven_ret[i])
  print(':::   2006 Lowest Counties for Suicide:')
  for i in range(4):
    ir = 5 + i
    print(':::    N-' + str(5-i-1) + '. ' + seven_ret[ir])
  print(':::    N.   ' + seven_ret[-1])

  print('::: Highest food stamp utilization :::')
  eight_ret = most_relative_foodstamp_county(data[2006])
  print(':::   2006 County with Highest Food Stamp Utilization: ' + eight_ret)

  print('::: Pertussis jump :::')
  data_list = [data[2006], data[2007], data[2008], data[2009]]
  nine_ret = biggest_pertussis_jump(data_list)
  print(':::   County with Biggest Jump in Pertussis from 2006->2007: ' + nine_ret)

  print('::: Insurance and low birth rate :::')
  ten_ret = mean_lowbirth_noinsurance(data[2006])
  print(':::   2006 Relation between Insurance and Low Birth Weight Rate:')
  print(':::   Insurance_Rate    Low_Birth_Rate')
  for rate in sorted(ten_ret.keys()):
    print(':::     ' + rate + '               ' + str(ten_ret[rate]))

  print('::: Writing to XML file :::')
  eleven_filename = 'prob11.xml'
  if os.path.exists(eleven_filename):
    os.remove(eleven_filename)
  employment_xml(data[2006], eleven_filename)
  print('::: First 10 lines of file for 2006:')
  with open(eleven_filename, 'r') as reader:
    lines = [line for line in reader.readlines()]
    for line in lines[:10]:
      print(':::   ' + line.replace('\n', ''))

  print('::: Writing to JSON file :::')
  twelve_filename = 'prob12.json'
  if os.path.exists(twelve_filename):
    os.remove(twelve_filename)
  infectious_json(data_list, twelve_filename)
  with open(twelve_filename, 'r') as f:
    twelve_ret = json.load(f)
  print('::: First 10 lines of file for 2006 and 2007:')
  with open(twelve_filename, 'r') as reader:
    lines = [line for line in reader.readlines()]
    for line in lines[:10]:
      print(':::   ' + line.replace('\n', ''))

  print('~~~ Analysis complete ~~~')


