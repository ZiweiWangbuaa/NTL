# The python code to get the label of each zone on ArcMap 10.8
def type(ss,c,r,a,i,g):
    res = "-"
    try:
        s = c+r+a+i
        if (g/ss<0.6) and (s/ss< 0.05):
            res = "-"
        else:
            if g/ss > 0.6:
                res = "nature"
            else:
                if  (r/s>0.5):
                    res = "residential"
                elif (c/s >0.5) :
                    res = "commercial" 
                elif (a/s >0.5) :
                    res = "amenity" 
                elif (i/s >0.5):
                    res = "industrial" 
                else:
                   res = "mix" 
    except:
        pass
    return res

def type(u1,u2):
    res = u1
    if u1 == "-":
        res = u2
    return res

#3.	The python code to get the label of each point 
def find_industry(data,column,string):
    return data[(data[column].str.contains(string))
      &(data['barrier'].isnull()) 
      &(data['place'].isnull())
      &(data['highway'].isnull())
      &(~data['other_tags'].str.contains('stop'))
      &(~data['other_tags'].str.contains('station'))
      &(~data['other_tags'].str.contains('railway'))
      &(~data['other_tags'].str.contains('amenity'))
      &(~data['other_tags'].str.contains('shop'))
      &(~data['other_tags'].str.contains('government'))
      &(~data['other_tags'].str.contains('public'))
      &(~data['other_tags'].str.contains('tourism'))
      &(~data['name'].str.contains('学'))
      &(~data['other_tags'].str.contains('museum'))]

industry = find_industry(data,'other_tags','\"office\"=>\"it\"')
for string in ['产业园','工业园','厂','Plant','plant','actory','工业','电气','company','软件','煤','矿','汽车','钢','然气','燃气']:
    industry = industry.append(find_industry(data,'name',string))
    industry = industry.append(find_industry(data,'other_tags',string))
    industry = industry.append(data[(data['other_tags'].str.contains('mine'))])
    industry = industry.append(data[(data['other_tags'].str.contains('industrial'))])
    industry = industry.append(data[(data['other_tags'].str.contains('craft'))])
    industry =industry.append(data[(data['other_tags'].str.contains('generator'))])
    industry = industry.append(data[(data['man_made'].str.contains('work'))])
    industry = industry.append(data[(data['man_made'].str.contains('crane'))])
    industry = industry.drop_duplicates(subset='osm_id')



def find_commercial(data,column,string):
    return data[(data[column].str.contains(string))
      &(data['barrier'].isnull()) 
      &(data['place'].isnull())
      &(data['highway'].isnull())
      &(~data['other_tags'].str.contains('stop'))
      &(~data['other_tags'].str.contains('station'))
      &(~data['other_tags'].str.contains('railway'))
      &(~data['other_tags'].str.contains('government'))
      &(~data['other_tags'].str.contains('viewpoint'))
      &(~data['other_tags'].str.contains('public'))]
commercial = data[(data['other_tags'].str.contains('leisure'))&(~data['other_tags'].str.contains('park'))]

for string in ['\"bar\"','\"biergarten\"','cuisine','diet','\"cafe\"','\"fast_food\"','\"food_court\"','\"ice_cream\"',
'\"restaurant\"','\"pub\"','\"atm\"','\"bank\"','\"bureau_de_change\"','\"cinema\"','\"nightclub\"','\"stripclub\"','\"studio\"',
'\"swingerclub\"','\"accountant\"','\"advertising_agency\"','\"architect\"','\"company\"','\"construction_company\"',
'\"consulting\"','\"engineer\"','\"estate_agent\"','\"financial\"','\"financial_advisor\"','\"graphic_design\"','\"guide\"',
'\"insurance\"','\"logistics\"','\"moving_company\"','\"newspaper\"','\"publisher\"','\"tax_advisor\"','\"telecommunication\"',
'\"therapist\"','\"travel_agent\"','\"tutoring\"','\"bbq\"','\"shop\"','\"sport\"','\"alpine_hut\"',
'\"chalet\"','\"guest_house\"','\"hostel\"','\"hotel\"','\"theme_park\"','\"kiosk\"',
'\"camp','\"picnic_site','\"viewpoint\"','\"wilderness_hut\"','\"zoo\"','plaza','\"park\"']:
    commercial = commercial.append(find_commercial(data,'other_tags',string))
for string in ['大厦'," Mall"," mall",'广场','事务所','公园']:
    commercial = commercial.append(find_commercial(data,'name',string))
    commercial = commercial.append(find_commercial(data,'other_tags',string))
    commercial = commercial.drop_duplicates(subset='osm_id')
    commercial = commercial[~commercial.index.isin(industry.index)]


def find_amenity(data,column,string):
    return data[(data[column].str.contains(string))
      &(data['barrier'].isnull()) 
      &(data['place'].isnull())
      &(data['highway'].isnull())
      &(~data['other_tags'].str.contains('stop'))
      &(~data['other_tags'].str.contains('station'))
      &(~data['other_tags'].str.contains('railway'))
      &(~data['other_tags'].str.contains('viewpoint'))]

amenity = data[(data['other_tags'].str.contains('college'))]
for string in ['driving_school','language_school','library','research','\"training\"','school','\"traffic_park\"',
 'university','\"boat_rental\"','\"boat_sharing\"','\"car_rental\"','\"car_sharing\"','\"car_wash\"','\"compressed_air\"','\"vehicle_inspection\"',
 '\"charging_station\"','\"driver_training\"','\"ferry_terminal\"','\"fuel\"','\"grit_bin\"','\"motorcycle_parking\"',
 '\"parking\"','\"parking_entrance\"','\"parking_space\"','\"taxi\"','\"baby_hatch\"','\"clinic\"','\"dentist\"',
 '\"doctors\"','\"hospital\"','\"nursing_home\"','\"pharmacy\"','\"social_facility\"','\"veterinary\"',
 '\"arts_centre\"','\"brothel\"','\"casino\"','\"community_centre\"','\"conference_centre\"','\"events_venue\"',
 '\"exhibition_centre\"','\"fountain\"','\"gambling\"','\"love_hotel\"','\"music_venue\"','\"planetarium\"',
 '\"public_bookcase\"','\"social_centre\"','\"planetarium\"','\"public_bookcase\"','\"theatre\"','\"museum\"',
 '\"gallery\"','\"courthouse\"','\"fire_station\"','\"police\"','\"post_box\"','\"post_depot\"',
 '\"post_office\"','\"prison\"','\"ranger_station\"','\"townhall\"','\"public\"','\"administrative\"',
 '\"association\"','\"chamber\"','\"charity\"','\"courier\"','\"coworking\"','\"diplomatic\"',
 '\"educational_institution\"','\"employment_agency\"','\"energy_supplier\"','\"courier\"','\"courier\"',
 '\"forestry\"','\"foundation\"','\"geodesist\"','\"government\"','\"harbour_master\"','\"ngo\"','\"notary\"',
 '\"politician\"','\"political_party\"','\"property_management\"','\"quango\"','\"religion\"',
 '\"research\"','\"security\"','\"office\"','\"surveyor\"','\"union\"','\"visa\"','\"water_utility\"','military']:
    amenity = amenity.append(find_amenity(data,'other_tags',string))
    amenity = amenity.drop_duplicates(subset='osm_id')
    amenity = amenity[~amenity.index.isin(commercial.index)]
    amenity = amenity[~amenity.index.isin(industry.index)]

resident = data[data['other_tags'].str.contains('\"landuse\"=>\"residential\"')]
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"apartments\"')])
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"barracks\"')])
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"bungalow\"')])                                
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"cabin\"')]) 
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"detached\"')]) 
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"dormitory\"')])  
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"ger\"')]) 
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"house\"')]) 
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"houseboat\"')]) 
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"house\"')])
resident = resident.append(data[data['other_tags'].str.contains('\"building\"=>\"residential\"')])
resident= resident.drop_duplicates(subset='osm_id')
resident = resident.drop_duplicates(subset='osm_id')
resident = resident[~resident.index.isin(amenity.index)]
resident = resident[~resident.index.isin(commercial.index)]
resident = resident[~resident.index.isin(industry.index)]


