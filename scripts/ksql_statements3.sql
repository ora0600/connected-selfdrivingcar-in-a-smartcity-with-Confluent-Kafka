CREATE STREAM connectedcar_s WITH (VALUE_FORMAT='json') AS 
SELECT car.selfdrivingcar as selfdrivingcar,
       car.ROWTIME AS CAR_TS, 
       city.ROWTIME AS CITY_TS, 
       car.CARGROUP AS cargroup, 
       car.LATITUDE as latitude,
       car.LONGITUDE as longitude,
       city.providerkey as provider,
       CASE
         WHEN (car.latitude=city.latitude and car.longitude=city.longitude) THEN city.message
         ELSE '' 
       END as message
    FROM selfdrivingcar_s car 
          LEFT JOIN smartcity_t city ON (car.selfdrivingcar=city.selfdrivingcar)
    emit changes;