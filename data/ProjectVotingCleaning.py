import pandas as pd
import os

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#Load data into dataframes
voting_data = pd.read_csv("VotingData/voting_VA.csv")
census_2008 = pd.read_csv("VotingData/Census_2008.csv",engine='python',encoding='latin1')
census_2012 = pd.read_csv("VotingData/Census_2012.csv",engine='python',encoding='latin1')
census_2016 = pd.read_csv("VotingData/Census_2016.csv",engine='python',encoding='latin1')

#Change year title to reflect the voting yeat the data will be used for
census_2008['YEAR'] = census_2008['YEAR'].replace('2006-2010','2008')
census_2012['YEAR'] = census_2012['YEAR'].replace('2010-2014','2012')
census_2016['YEAR'] = census_2016['YEAR'].replace('2014-2018','2016')


### Census 2008 Processing

#Sub select the desired columns from the census data
columns_2008 = ['YEAR','STATE','COUNTY','JLZE001','JN9E011','JN9E028','JOCE001','JQBE001','JTIE001']
sub_census_2008 = census_2008[columns_2008]
#Rename columns to reflect their meaning instead of their code
sub_census_2008 = sub_census_2008.rename(columns={'JLZE001':'Total Population','JN9E011':'Male: GED Ratio','JN9E028':'Female: GED Ratio',
                                                  'JOCE001':'Income to Poverty Level Ratio','JQBE001':'Per Capita Income vs Pop','JTIE001':'Median House Value'})

#Drop the header row
sub_census_2008 = sub_census_2008.drop([0, 1])
#Convert columns to numeric and divide by the population when applicable
sub_census_2008['Male: GED Ratio'] = pd.to_numeric(sub_census_2008['Male: GED Ratio'],errors='coerce')/pd.to_numeric(sub_census_2008['Total Population'],errors='coerce')
sub_census_2008['Female: GED Ratio'] = pd.to_numeric(sub_census_2008['Female: GED Ratio'],errors='coerce')/pd.to_numeric(sub_census_2008['Total Population'],errors='coerce')
sub_census_2008['Income to Poverty Level Ratio'] = pd.to_numeric(sub_census_2008['Income to Poverty Level Ratio'],errors='coerce')/pd.to_numeric(sub_census_2008['Total Population'],errors='coerce')
sub_census_2008['Per Capita Income vs Pop'] = pd.to_numeric(sub_census_2008['Per Capita Income vs Pop'],errors='coerce')/pd.to_numeric(sub_census_2008['Total Population'],errors='coerce')

#Addoing male and female GED occurances to find overall GED occurances
sub_census_2008['GED Ratio'] = sub_census_2008['Male: GED Ratio'] + sub_census_2008['Female: GED Ratio']
sub_census_2008 = sub_census_2008.drop(['Male: GED Ratio','Female: GED Ratio'], axis=1)



### Census 2012 Processing
#Sub select the desired columns from the census data
columns_2012 = ['YEAR','STATE','COUNTY','ABAQE001','ABC4E017','ABDJE001','ABFIE001','ABITE001']
sub_census_2012 = census_2012[columns_2012]
#Rename columns to reflect their meaning instead of their code
sub_census_2012 = sub_census_2012.rename(columns={'ABAQE001':'Total Population','ABC4E017':'GED Ratio','ABDJE001':'Income to Poverty Level Ratio',
                                                  'ABFIE001':'Per Capita Income vs Pop','ABITE001':'Median House Value'})

#Drop the header row
sub_census_2012 = sub_census_2012.drop([0, 1])

#Convert columns to numeric and divide by the population when applicable
sub_census_2012['Income to Poverty Level Ratio'] = pd.to_numeric(sub_census_2012['Income to Poverty Level Ratio'],errors='coerce')/pd.to_numeric(sub_census_2012['Total Population'],errors='coerce')
sub_census_2012['Per Capita Income vs Pop'] = pd.to_numeric(sub_census_2012['Per Capita Income vs Pop'],errors='coerce')/pd.to_numeric(sub_census_2012['Total Population'],errors='coerce')
sub_census_2012['GED Ratio'] = pd.to_numeric(sub_census_2012['GED Ratio'],errors='coerce')/pd.to_numeric(sub_census_2012['Total Population'],errors='coerce')


### Census 2016 Processing
#Sub select the desired columns from the census data
columns_2016 = ['YEAR','STATE','COUNTY','AJWBE001','AJYPE017','AJYPE018','AJY4E001','AJ0EE001','AJ3QE001']
sub_census_2016 = census_2016[columns_2016]

#Rename columns to reflect their meaning instead of their code
sub_census_2016 = sub_census_2016.rename(columns={'AJWBE001':'Total Population','AJYPE017':'Highschool Diploma','AJYPE018':'GED','AJY4E001':'Income to Poverty Level Ratio',
                                                  'AJ0EE001':'Per Capita Income vs Pop','AJ3QE001':'Median House Value'})

#Drop the header row
sub_census_2016 = sub_census_2016.drop([0, 1])

#Convert columns to numeric and divide by the population when applicable
sub_census_2016['GED Ratio'] = pd.to_numeric(sub_census_2016['Highschool Diploma'],errors='coerce') + pd.to_numeric(sub_census_2016['GED'],errors='coerce')
sub_census_2016['Income to Poverty Level Ratio'] = pd.to_numeric(sub_census_2016['Income to Poverty Level Ratio'],errors='coerce')/pd.to_numeric(sub_census_2016['Total Population'],errors='coerce')
sub_census_2016['Per Capita Income vs Pop'] = pd.to_numeric(sub_census_2016['Per Capita Income vs Pop'],errors='coerce')/pd.to_numeric(sub_census_2016['Total Population'],errors='coerce')
sub_census_2016['GED Ratio'] = pd.to_numeric(sub_census_2016['GED Ratio'],errors='coerce')/pd.to_numeric(sub_census_2016['Total Population'],errors='coerce')
sub_census_2016 = sub_census_2016.drop(['Highschool Diploma','GED'], axis=1)



#Change all numeric columns to type int.
for column in sub_census_2008:
    if column not in ['COUNTY','STATE']:
        sub_census_2008[column] = pd.to_numeric(sub_census_2008[column],errors='coerce')

for column in sub_census_2012:
    if column not in ['COUNTY','STATE']:
        sub_census_2012[column] = pd.to_numeric(sub_census_2012[column],errors='coerce')

for column in sub_census_2016:
    if column not in ['COUNTY','STATE']:
        sub_census_2016[column] = pd.to_numeric(sub_census_2016[column],errors='coerce')


#Merge census data
merged_data = pd.concat([sub_census_2008,sub_census_2012,sub_census_2016],axis=0)
merged_census_data = merged_data.loc[merged_data['STATE'] == 'Virginia']



#Voting Dict

#Sub select the voting data
voting_data_dem = voting_data.loc[voting_data['party'] == 'DEMOCRAT']
voting_data_dem = voting_data_dem.loc[voting_data['mode'] == 'TOTAL']

voting_data_rep = voting_data.loc[voting_data['party'] == 'REPUBLICAN']
voting_data_dem = voting_data_dem.loc[voting_data['mode'] == 'TOTAL']

#Create dictionaries in which to store the relevant voting data
voting_dict_dem = {}
voting_dict_rep = {}

#Iterate through democrat votes, storing the data as a tuple in the dem dictionary by county and year
for index, row in voting_data_dem.iterrows():

    voting_dict_dem[(row.county_name.lower(),row.year)] = [row.totalvotes, row.candidatevotes,]


#Add the dem votes to a list in the same order as the census data
tot_vot = []
dem_vot = []
rep_vot = []
for index, row in merged_census_data.iterrows():


    county = row.COUNTY.lower().replace(' county', '')
    year = row.YEAR

    if 'city' in county and 'charles' not in county and 'james' not in county:
        county = county.replace(' city','')

    tot_vot.append(voting_dict_dem[(county, year)][0])
    dem_vot.append(voting_dict_dem[(county, year)][1])



#Iterate through republican votes, storing the data as a tuple in the dem dictionary by county and year
for index, row in voting_data_rep.iterrows():

    voting_dict_rep[(row.county_name.lower(),row.year)] = [row.totalvotes, row.candidatevotes,]

#Add the republican votes to a list in the same order as the census data
rep_vot = []
for index, row in merged_census_data.iterrows():


    county = row.COUNTY.lower().replace(' county', '')
    year = row.YEAR

    if 'city' in county and 'charles' not in county and 'james' not in county:
        county = county.replace(' city','')

    rep_vot.append(voting_dict_rep[(county, year)][1])


#Add the lists containing total, dem, and rep votes to a df
vot_df = pd.DataFrame({'Total Votes':tot_vot,'Democrat Votes':dem_vot,'Republican Votes':rep_vot})


#Merge the census and voting data
vot_census_data = pd.concat([merged_census_data.reset_index(),vot_df.reset_index()],axis=1)

print(vot_census_data.head())

#Write the combined census and voting data to a xlsx file.
with pd.ExcelWriter('Vot_Census_Data' + '.xlsx', engine='openpyxl') as writer:
    vot_census_data.to_excel(writer, index=None)

    