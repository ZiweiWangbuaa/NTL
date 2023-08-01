
var minNTL = 0.3; // dark radiation threshold
var maxNTL = 450.42; //max: Guangdong，2018
var scale = 300;
var ind = 'DNB_BRDF_Corrected_NTL';
var username = 'YOUR USERNAME'
var shp = ee.FeatureCollection('users/'+username+'/CHN_adm1');
var provinceName = 'Zhejiang';
var filter = ee.Filter.eq('NAME_1', provinceName);
var shp = shp.filter(filter);

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

var collection = ee.ImageCollection("NOAA/VIIRS/001/VNP46A2")  
  .filterDate("2017-01-01", "2017-12-31")
  .select([ind])
  .map(preprocessImage)
  .map(function(image) {
    return image
      .clip(shp)
      .reproject('EPSG:4326', null, scale);
  });

// Get the mean NTL value
var ntls = collection.filterBounds(shp.geometry()).mean();

Export.image.toDrive({
  image: ntls,
  folder: 'YearNTL',
  scale: scale,
  fileNamePrefix: provinceName+"2017",
  region: shp.geometry(),
  maxPixels: 1e13,
  crs: 'EPSG:4326',
  fileFormat: 'GeoTIFF',
  description:  provinceName+"2017",
});
