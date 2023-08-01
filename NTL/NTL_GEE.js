var genDateRange = function(year,month) {
    var startDate = ee.Date.fromYMD(year, month, 1);
    var end = startDate.advance(1, 'month').advance(-1, 'day');
    var dateList = [startDate.format('YYYY-MM-dd'), end.format('YYYY-MM-dd')]; 
    return dateList
  }
  
var getRes = function(V){
    var provNames = V.aggregate_array('UFZ');
    var L = V.aggregate_array(ind);
    var featureList = ee.List.sequence(0, L.size().subtract(1))
      .map(function (index) {
        var name = ee.String(provNames.get(index));
        var value = ee.Number(L.get(index));
        return ee.Feature(null, { 'UFZ': name, ind: value });
      });
      return featureList
  }
  
var preprocessImage = function(image) {
    var kernel = ee.Kernel.square(1);
    // Mask out pixels with values less than the dark radiance threshold
    var maskedImage = image.updateMask(image.gt(minNTL));
    // Find the maximum value in the 3x3 neighborhood for pixels with values greater than the maximum threshold
    var maxMaskedImage = image.updateMask(image.gt(maxNTL))
                              .focal_max({kernel: kernel, iterations: 10})
                              .updateMask(maskedImage.lt(maxNTL));
  
    // Replace pixels with values greater than the maximum threshold with the maximum value in their 3x3 neighborhood
    maskedImage = maskedImage.where(maskedImage.gt(maxNTL), maxMaskedImage);
    maskedImage = maskedImage.where(maskedImage.gt(maxNTL), maxNTL);
    return maskedImage.copyProperties(image, image.propertyNames());
  };
  
var oncevalue = function(shp,year,month) {
    var DateRange = genDateRange(year,month)
    var collection = ee.ImageCollection("NOAA/VIIRS/001/VNP46A2")  
      .filterDate(DateRange[0],DateRange[1])
      .select([ind])
      .map(preprocessImage)
      .map(function(image) {
        return image
          .clip(shp)
          .reproject('EPSG:4326', null, scale);
      });

var Values = shp.map(function (province) {
      var ntls = collection.filterBounds(province.geometry()).mean()
      .reduceRegion({
          reducer: reducer,
          geometry: province.geometry(),
          crs:'EPSG:4326',
          scale: scale,
          maxPixels: 1e32,
          tileScale:1.5,
        });
      return province.set(ind, ntls.get(ind));
    });
    return Values
  };

var savetoDrive = function(provsWithLights,folder,filename ) {
    Export.table.toDrive({
      collection: provsWithLights,
      folder:folder ,
      description: filename,
      fileNamePrefix: filename,
      fileFormat: "CSV"
    });
  }

var pn = 'BJ'
var minNTL = 0.3; // dark radiation threshold
var maxNTL = 450.42; // max：Guangdong，2018
var reducer = ee.Reducer.mean();
var scale = 30;
var ind = 'DNB_BRDF_Corrected_NTL'
var username = 'YOUR USERNAME'

for (var year=2016; year<=2022; year++){
    var year1 = year + 1
    var shp = ee.FeatureCollection('users/'+'/'+pn+'_UFZ_'+year1+'_D');
    for (var month = 1; month <= 12; month++) {
      var provsWithLights = getRes(oncevalue(shp,year,month));
      savetoDrive(ee.FeatureCollection(provsWithLights),"Pro_mean_"+ind,pn+year+"-"+month)   
    }
  
  }