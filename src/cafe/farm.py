from dataclasses import dataclass, field
import datetime
from functools import lru_cache
import numpy as np
from typing import List, Optional, Tuple, Callable, Union, Dict
from numbers import Number
import warnings

import pandas as pd


@dataclass(frozen=True)
class Config:
    species: str
    name: str = ""
    output_per_crop: float = 1.0
    unit: str = "cuerdas"

    def __eq__(cls, other_cls):
        if cls.name and other_cls.name:
            return (
                cls.name == other_cls.name
                and cls.species == other_cls.species
                and cls.unit == other_cls.unit
            )
        return cls.species == other_cls.species and cls.unit == other_cls.unit


@lru_cache(maxsize=128)
def find_config(name: str, configs: Tuple[Config]) -> Config:
    # first check for name (to look for strategy)
    for c in configs:
        if c.name == name:
            return c
    # if none found, seek species default
    # TODO print warning about this behavior
    warnings.warn(
        (
            "Could not find canonical match"
            f"for species=`{name}`, searching for"
            "match against species instead."
        )
    )
    for c in configs:
        if c.species == name:
            return c
    raise ValueError(f"Could not find desired config for species=`{name}`")


@dataclass
class Event:
    name: str
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None
    impact: Optional[Union[float, Callable]] = 1.0
    scope: Optional[Dict] = field(default_factory=dict)

    def is_active(self, current_time=datetime.datetime.today()) -> bool:
        if not self.start:
            return True
        if not self.end:
            return True
        age = self.age(current_time)
        return age > 0 and current_time <= self.end

    def age(self, current_time=datetime.datetime.today()) -> datetime.timedelta:
        return current_time - self.start

    def years(self, current_time=datetime.datetime.today()) -> int:
        return round(self.age(current_time).days / 365.25)

    def days(self, current_time=datetime.datetime.today()) -> int:
        return self.age(current_time).days

    def mins(self, current_time=datetime.datetime.today()) -> int:
        return round(self.age(current_time).seconds / 60)

    def eval(self, *args):
        if isinstance(self.impact, Callable):
            return self.impact(*args, **self.__dict__)
        return self.impact


@dataclass
class Plot:
    num: int = 1  # number of crops
    area: float = 1.0
    plot_id: int = 0
    species: str = field(default_factory=str)
    unit: str = "cuerdas"
    origin: datetime = datetime.datetime(2020, 1, 1, 0, 0)

    @property  # TODO deprecate / change tests?
    def size(self) -> float:
        return self.area

    @property  # TODO deprecate / change tests?
    def year_planted(self):
        return self.origin.year

    @staticmethod
    def to_datetime(time) -> datetime.datetime:
        if isinstance(time, Number):  # assumes `time` = year
            return datetime.datetime(round(time), 1, 1, 0, 0)
        elif isinstance(time, datetime.datetime):
            return time
        else:
            raise ValueError(f"Please specify a valid time. Given {type(time)}")

    @classmethod
    def from_series(cls, series):
        return cls.from_density(
            density=1.0,
            plot_id=series.plotID,
            species=series.treeType,
            area=series.numCuerdas,
            unit="cuerdas",
            origin=cls.to_datetime(series.yearPlanted),
        )

    @classmethod
    def from_dict(cls, dict):
        return cls.from_series(pd.Series(dict))

    @classmethod
    def from_density(cls, density: float = 1.0, **kwargs):
        plot = cls(**kwargs)
        plot.num = np.floor(plot.area * density)
        return plot


@dataclass
class Farm:
    plot_list: List[Plot] = field(default_factory=List)

    @classmethod
    def from_csv(cls, csv_file):
        df = pd.read_csv(csv_file)
        list_of_plots = []
        for idx, series in df.iterrows():
            list_of_plots.append(Plot.from_series(series))
        return cls(list_of_plots)

    @property
    def size(self) -> float:
        return len(self.plot_list)

    @property
    def plots(self) -> List[Plot]:
        return self.plot_list

    @property
    def ids(self) -> List[str]:
        return [p.plot_id for p in self.plot_list]

    def contains(self, species: str = "") -> bool:
        return species in set(p.species for p in self.plot_list)


def predict_yield_for_farm(
    farm: Farm,
    configs: List[Config],
    events: List[Event] = None,
    time: datetime.datetime = datetime.datetime(2020, 1, 1),
) -> List[float]:
    harvests = []
    for p in farm.plots:
        name = p.species
        try:
            c = find_config(name, configs)
            harvests.append(predict_yield_for_plot(p, c, events, time))
        except ValueError as v:
            warnings.warn(
                f"Caught {v}, skipping yield prediction for plot {p.plot_id}. Yield will be 0"
            )  # TODO: make into a logger instead
            harvests.append(0)
    return harvests


def total_impact(plot: Plot, time: datetime.datetime, events: List[Event]) -> float:
    # - is it relevant to this plot? can check species, geography, etc.
    # - if so, what will be the impact to pass to the prediction function?
    # - is a strategy being applied? it has an impact too, is an event
    if not events:
        return 1.0

    relevent_events = []
    for e in events:
        # TODO more checks to determine this condition
        if e.is_active(time):
            relevent_events.append(e)

    impact = np.prod([e.eval(time) for e in relevent_events])
    return impact


def predict_yield_for_plot(
    plot: Plot,
    config: Config,
    events: Optional[List[Event]] = None,
    time: datetime.datetime = datetime.datetime(2020, 1, 1),
) -> float:
    # yield = area * crops/area * weight / crop
    # messy to compare two different classes but duck typing allows it...
    if plot.species == config.species and plot.unit == config.unit:
        impact = total_impact(plot, time, events)
        return plot.num * config.output_per_crop * impact
    raise ValueError(f"Species mismatch, {plot}, {config}")


def guate_harvest_function(
    lifespan: float = 30, mature: float = 5, retire: float = 28
) -> Callable:
    def f(time, **kwargs):
        start = kwargs["start"].year
        year = time if isinstance(time, (float, int)) else time.year
        age = year - start
        if age < mature - 1:
            return 0
        if age == mature - 1:
            return 0.2
        if age < retire:
            return 1.0
        if age < lifespan:
            return 1 - 0.25 * (lifespan - age)
        return 1.0

    return f
