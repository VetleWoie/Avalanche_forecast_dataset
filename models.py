import datetime
from typing import List
from pydantic import BaseModel

class IdName(BaseModel):
    Id : str
    Name: str

class MeasurementSubType(BaseModel):
    Id : int
    Name : str
    SortOrder : int
    Value : str | None

class MeasurmentType(BaseModel):
    Id : int
    Name : str
    SortOrder : int
    MeasurementSubTypes : List[MeasurementSubType]

class MeasurmentText(BaseModel):
    SortOrder : int
    Text : str

class MountainWeather(BaseModel):
    LastSavedTime : datetime.datetime
    CloudCoverId : int
    CloudCoverName : str
    Comment : str | None
    MeasurementTypes : List[MeasurmentType]
    MeasurementTexts : List[MeasurmentText]

class AvalancheProblem(BaseModel):
    AvalancheProblemId : int
    AvalancheExtId : int
    AvalancheExtName : str
    AvalCauseId : int
    AvalCauseName : str
    AvalProbabilityId : int
    AvalProbabilityName : str
    AvalTriggerSimpleId : int
    AvalTriggerSimpleName : str
    AvalTriggerSensitivityId : int
    AvalTriggerSensitivityName : str
    DestructiveSizeExtId : int
    DestructiveSizeExtName : str
    AvalPropagationId : int
    AvalPropagationName : str
    AvalancheTypeId : int
    AvalancheTypeName : str
    AvalancheProblemTypeId : int
    AvalancheProblemTypeName : str
    ValidExpositions : str
    ExposedHeight1 : int
    ExposedHeight2 : int
    ExposedHeightFill : int
    TriggerSenitivityPropagationDestuctiveSizeText : str
    DangerLevel : int
    DangerLevelName : str | None

class AvalancheAdvice(BaseModel):
    AdviceID : int
    ImageUrl : str
    Text : str | None

class AvaForecastDetailed(BaseModel):
    CountyList : List[IdName]
    MunicipalityList : List[IdName]
    PreviousWarningRegId : int | None
    DangerLevelName : str | None
    UtmZone : int
    UtmEast : float
    UtmNorth : float
    Author : str | None
    AvalancheDanger : str | None
    EmergencyWarning : str | None
    SnowSurface : str | None
    CurrentWeaklayers : str | None
    LatestAvalancheActivity : str | None
    LatestObservations : str | None
    ExposedHeightFill : int
    ExposedHeight1 : int
    MountainWeather : MountainWeather | None
    AvalancheProblems : List[AvalancheProblem] | None
    AvalancheAdvices : List[AvalancheAdvice] | None
    ExtremWeatherId : str | None
    ExtremWeatherName : str | None
    IsTendency : bool
    RegId : int
    RegionId : int
    RegionName : str
    RegionTypeId : int
    RegionTypeName : str
    DangerLevel : int
    ValidFrom : datetime.datetime
    ValidTo : datetime.datetime
    NextWarningTime : datetime.datetime
    PublishTime : datetime.datetime
    DangerIncreaseTime : datetime.datetime | None
    DangerDecreaseTime : datetime.datetime | None
    MainText : str
    LangKey : int


class Region(BaseModel):
    Id : int
    Name : str
    TypeId : int
    TypeName : str
    ValidFrom : datetime.datetime
    ValidTo : datetime.datetime