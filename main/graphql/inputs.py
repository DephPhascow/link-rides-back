from datetime import date
from typing import Optional
from strawberry_django import input, partial
from strawberry.file_uploads import Upload


from main.models import TaxiInfoModel

@input(TaxiInfoModel)
class TaxiInfoInput:
    first_name: str
    last_name: str
    car_brand: str
    car_model: str
    car_color: str
    car_number: str
    year: int
    series_license: str
    country_license: str
    date_get_license: date
    license_valid_until: date
    # photo_license: Upload
    
@partial(TaxiInfoModel)
class TaxiInfoUpdate:
    first_name: Optional[str]
    last_name: Optional[str]
    car_brand: Optional[str]
    car_model: Optional[str]
    car_color: Optional[str]
    car_number: Optional[str]
    year: Optional[int]
    series_license: Optional[str]
    country_license: Optional[str]
    date_get_license: Optional[date]
    license_valid_until: Optional[date]
    photo_license: Optional[Upload]