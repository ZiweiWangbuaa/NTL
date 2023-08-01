### The SQL code to get the label of each polygon on ArcMap 10.8
def deftype(aeroway, amenity, building, craft, historic, landuse, leisure, man_made, military, natural, office, place, shop, sport, tourism, Shape_Area)
    if (( leisure !=' ' ) or (landuse=='commercial') or (building=='commercial') or  (( tourism !=' ') and ( tourism !='museum')) or  ( sport !=' ' )  or  ( shop !=' ' )  or (amenity == 'bar')or (amenity == 'biergarten')or (amenity =='cuisine')or (amenity == 'cafe')or (amenity == 'fast_food')or (amenity == 'food_court')or (amenity == 'ice_cream')or (amenity == 'restaurant')or (amenity == 'pub')or (amenity == 'atm')or (amenity == 'bank')or (amenity == 'bureau_de_change')or (amenity == 'cinema')or (amenity == 'nightclub')or (amenity == 'stripclub')or (amenity == 'studio')or (amenity == 'swingerclub')or (amenity == 'accountant')or (amenity == 'advertising_agency')or (amenity == 'architect')or (amenity == 'construction_company')or (amenity == 'consulting')or (amenity == 'engineer')or (amenity == 'estate_agent')or (amenity == 'financial_advisor')or (amenity == 'graphic_design')or (amenity == 'guide')or (amenity == 'insurance')or (amenity == 'logistics')or (amenity == 'moving_company')or (amenity == 'newspaper')or (amenity == 'car_wash')or (amenity == 'fuel')or (amenity == 'gambling')or (amenity == 'nightclub') or (amenity == 'theatre')or (amenity == 'bbq') or (landuse=='retail')or (building=='retail')or (building=='hotel') or (building=='stadium') or (building=='office') ) and (Shape_Area>0):
        type = 'commercial'
    elif  ((landuse=='residential')  or (place=='neighbourhood') or (place=='village')or (building=='apartments')or(building=='residential')or (building=='house'))and (Shape_Area>0):
        type = 'residential'
    elif ((tourism=='museum') or (
(amenity !=' ') and (amenity != 'bar')and(amenity!= 'biergarten')and (amenity !='cuisine')and (amenity != 'cafe')and (amenity !='fast_food')and (amenity !='food_court')and (amenity!= 'ice_cream')and (amenity !='restaurant')and (amenity != 'pub')and (amenity !='atm')and (amenity!= 'bank')and (amenity !='bureau_de_change')and (amenity != 'cinema')and (amenity != 'nightclub')and (amenity != 'stripclub')and (amenity != 'studio')and (amenity != 'swingerclub')and (amenity != 'accountant')and (amenity !='advertising_agency')and (amenity != 'architect')and (amenity != 'construction_company')and (amenity != 'consulting')and (amenity!='engineer')and (amenity!= 'estate_agent')and (amenity != 'financial_advisand')and (amenity != 'graphic_design')and (amenity!= 'guide')and (amenity !='insurance')and (amenity!= 'logistics')and (amenity != 'moving_company')and (amenity != 'newspaper')and (amenity!= 'car_wash')and (amenity != 'fuel')and (amenity != 'gambling')and (amenity != 'nightclub') and (amenity !='theatre')and (amenity!= 'bbq')  
)or (military!=' ') or (office=='government') or
  (landuse=='embassy_compoundor')or (building=='public') or (building=='hospital') or (building=='hospital') or (building=='temple') or (building=='school') or (building=='dormitory') or (building=='garage') or (building=='church') or (building=='kindergarten') or (building=='college') or (aeroway!=' '))and (Shape_Area>0):
        type = 'amenity'
    elif ((landuse == 'quarry') or (landuse=='industrial') or (building=='industrial') or (building=='warehouse') )and (Shape_Area>0):
        type = 'industrial'
    elif natural!=' ':
        type = 'nature'
    else:
        type = 'other'
    return type



