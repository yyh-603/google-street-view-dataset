# Google street view dataset
## Dataset Link
[Google Drive Link](https://drive.google.com/file/d/12vRaxp1LYLD-misMaedzQJjX2BeQZr0n/view?usp=sharing)

**Only accounts with nycu.edu.tw domain are allowed to access.**

## Method
We use Google Cloud API to do data collection.
### Google API
These are the Google Cloud API we used.
#### Street View Static API
This API allows us to send a pair of geographic coordinate (lat, lon). Then there are two function of these API.

1. Check whether there is a image on (lat, lon).
2. Get the Image on (lat, lon).

the first API function is free. But the second one is not.
#### Geocoding API
This API allows us to send a pair of geographic coordinate (lat, lon). Then it will reply the address of this location.

This API is also not free.

### Mark boundary
Cause we want to collect the image of the regions in Taiwan. We manually mark a rectangular boundary of each County and City. Then we can do select a random coordinate within the boundary to get a image much more quickly.

### Python
The procedure of getting a image is:
1. select a geographic coordinate (lat, lon) randomly from the rectangular boundary of the specific region.
2. check whether there is a image on this location by API. (we do this first because this API is free).
3. check whether the address of this location is inside the specific region.
4. get the image of this location and save it to the folder.
