import datetime
import logging
import warnings
from dataclasses import dataclass, field
from functools import lru_cache, wraps
from numbers import Number
from typing import Callable, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd
import timedelta

_logger = logging.getLogger(__name__)


def maybe_time_like(cls):
    """
    Wrapper to add temporal properties and methods to a class.
    """

    @wraps(cls, updated=())
    @dataclass
    class temporal(cls):
        # start: Optional[datetime.datetime] = datetime.datetime(2020, 1, 1, 0, 0)
        start: Optional[datetime.datetime] = None
        end: Optional[datetime.datetime] = None

        @property
        def year_planted(self):
            return self.start.year

        def age(self, current_time=datetime.datetime.today()) -> datetime.timedelta:
            if not self.start:
                raise ValueError("Start time undefined, age indeterminable.")
            return current_time - self.start

        def years(self, current_time=datetime.datetime.today()) -> int:
            return int(timedelta.Timedelta(self.age(current_time)).total.days / 365.25)

        def days(self, current_time=datetime.datetime.today()) -> int:
            return timedelta.Timedelta(self.age(current_time)).total.days

        def mins(self, current_time=datetime.datetime.today()) -> int:
            return timedelta.Timedelta(self.age(current_time)).total.minutes

    return temporal


@dataclass(frozen=True)
class Config:
    """
    Stores information about crop yields per species / varietal name
    """

    species: str
    name: str = ""
    output_per_crop: float = 1.0
    unit: str = "cuerdas"

    def __eq__(self, other_cls):
        if self.name and other_cls.name:
            return (
                self.name == other_cls.name
                and self.species == other_cls.species
                and self.unit == other_cls.unit
            )
        return self.species == other_cls.species and self.unit == other_cls.unit


@maybe_time_like
@dataclass
class Plot:
    """
    Stores information about a farmer's plot.

    What is planted, how much, where, to whom does it belong? etc.
    """

    num: int = 1  # number of crops
    area: float = 1.0
    plot_id: int = 0
    species: str = field(default_factory=str)
    unit: str = "cuerdas"

    @property  # TODO deprecate / change tests?
    def size(self) -> float:
        return self.area

    @staticmethod
    def to_datetime(time) -> datetime.datetime:
        if isinstance(time, Number):  # assumes `time` = year
            return datetime.datetime(round(time), 1, 1, 0, 0)
        elif isinstance(time, datetime.datetime):
            return time
        else:
            raise ValueError(f"Please specify a valid time. Given {type(time)}")

    @classmethod
    def from_series(cls, series: pd.Series, **kwargs):
        """
        Instantiates class from a ``pandas.Series`` object.

        This method primarily exists for backwards compatibility.

        Args:
            data (dict): Plot density (trees/unit area)
            **kwargs: Arbitrary keyword arguments.

        Returns:
            plot (Plot): ``Plot`` object.
        """
        return cls.from_density(
            density=1.0,
            plot_id=series.plotID,
            species=series.treeType,
            area=series.numCuerdas,
            unit="cuerdas",
            start=cls.to_datetime(series.yearPlanted),
        )

    @classmethod
    def from_dict(cls, data: Dict, **kwargs):
        """
        Instantiates class using a ``dict`` object.

        This method primarily exists for backwards compatibility.

        Args:
            data (dict): Plot density (trees/unit area)
            **kwargs: Arbitrary keyword arguments.

        Returns:
            plot (Plot): ``Plot`` object.
        """
        return cls.from_series(pd.Series(data))

    @classmethod
    def from_density(cls, density: float = 1.0, **kwargs):
        """
        Instantiates class using a ``density`` argument instead of
        the number of trees.

        Args:
            density (float): Plot density (trees/unit area)
            **kwargs: Arbitrary keyword arguments.

        Returns:
            plot (Plot): ``Plot`` object.
        """
        plot = cls(**kwargs)
        plot.num = np.floor(plot.area * density)
        return plot


@dataclass
class Farm:
    """
    Container class for a collection of ``Plot`` objects.
    """

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


@maybe_time_like
@dataclass
class Event:
    """
    Stores information about events which impact harvest expectations.
    """

    name: str
    impact: Optional[Union[float, Callable]] = 1.0
    scope: Optional[Union[bool, Dict]] = field(default_factory=dict)

    def is_active(
        self,
        current_time: datetime.datetime = datetime.datetime.today(),
        plot: Optional[Plot] = None,
    ) -> bool:
        """
        Performs checks on scope of event to determine whether or not this
        event will have an impact on the harvest.
        """
        time_check = self._check_time_window(current_time)
        # TODO: add more checks involving scope
        scope_check = self._check_scope(plot)
        return time_check and scope_check

    def _check_time_window(self, current_time=datetime.datetime.today()) -> bool:
        """
        Determines if event is occurring at a specified time.
        """
        if not self.start:
            return True
        if not self.end:
            return True
        age_in_mins = self.mins(current_time)
        return age_in_mins > 0 and current_time <= self.end

    def _check_scope(self, plot: Optional[Plot] = None):
        """
        Checks whether event is relevant / active with respect to the event scope.
        This determination can be based on species and location data of a plot.
        """
        if isinstance(self.scope, bool):
            return self.scope
        if not self.scope:
            _logger.warning("Scope definition missing, assuming inactive.")
            return False
        if not plot:
            _logger.warning("Plot definition missing, assuming inactive.")
            return False
        if self.scope["type"] == "species":
            return self.scope["def"] == plot.species
        if self.scope["type"] in ("geo", "gps", "area"):  # TODO: naming choices
            raise NotImplementedError("Geographic scope not yet implemented.")
        return False

    def eval(self, *args, **kwargs):
        if isinstance(self.impact, Callable):
            return self.impact(*args, **kwargs, **self.__dict__)
        return self.impact


@lru_cache(maxsize=128)
def find_config(name: str, configs: Tuple[Config]) -> Config:
    """
    Looks up a varietal by name in a collection of
    `Configs`. If name not found, will return config for
    the species instead, but throw an error if missing.

    Args:
        name (str): Name of varietal or species to look up
        configs (Tuple[Config]): registry of configs

    Returns:
        config (Config): relevant config entry

    Raises:
        KeyError: `name` could not be found in `configs`
    """
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


def guate_harvest_function(
    lifespan: float = 30, mature: float = 5, retire: float = None
) -> Callable:
    """
    Defines piecewise-linear function which approximates the growth patterns
    of coffee trees according to the coffee cooperative for which this simulation
    was first written.
    """
    if not retire:
        retire = lifespan - 2
    assert retire < lifespan
    assert mature < retire

    def growth(time: Union[datetime.datetime, float], plot: Plot, **kwargs):
        birth_year = plot.year_planted
        current_year = time if isinstance(time, (float, int)) else time.year
        age = current_year - birth_year
        if age < mature - 1:
            return 0
        if age == mature - 1:
            return 0.2
        if age < retire:
            return 1.0
        if age <= lifespan:
            return 1.0 - 0.25 * (age - retire)
        _logger.info("Replanting same species.")
        return growth(current_year - lifespan - 1, plot)

    return growth


def total_impact(plot: Plot, time: datetime.datetime, events: List[Event]) -> float:
    """
    Determines which events are relevant and multiplies all the associated impacts
    together in order to define the "total impact" of these events on a particular plot.
    """
    # - is it relevant to this plot? can check species, geography, etc.
    # - if so, what will be the impact to pass to the prediction function?
    # - is a strategy being applied? it has an impact too, is an event
    if not events:
        _logger.warning("Events empty")
        return 1.0

    relevant_events = []
    for e in events:
        # TODO more checks to determine this condition
        if e.is_active(plot=plot, current_time=time):
            relevant_events.append(e)
            _logger.debug(f"Found relevant event {e}")
    impact = np.prod([e.eval(time=time, plot=plot) for e in relevant_events])
    return impact


def predict_yield_for_plot(
    plot: Plot,
    config: Config,
    events: Optional[List[Event]] = None,
    time: datetime.datetime = datetime.datetime(2020, 1, 1),
) -> float:
    """
    Predicts yields for a given plot, set of events, and collection of configs
    at a specified time.
    """
    # yield = area * crops/area * weight / crop
    # messy to compare two different classes but duck typing allows it...
    if plot.species == config.species and plot.unit == config.unit:
        impact = total_impact(plot=plot, time=time, events=events)
        return plot.num * config.output_per_crop * impact
    raise ValueError(f"Species mismatch, {plot}, {config}")


def predict_yield_for_farm(
    farm: Farm,
    configs: List[Config],
    events: Optional[List[Event]] = None,
    time: datetime.datetime = datetime.datetime(2020, 1, 1),
) -> List[float]:
    if events and not isinstance(events, list):  # TODO: add tests for this
        events = list(events)
    harvests = []
    for p in farm.plots:
        # print(f"Processing Plot {p.plot_id}")
        name = p.species
        try:
            c = find_config(name, configs)
            harvests.append(
                predict_yield_for_plot(plot=p, config=c, events=events, time=time)
            )
        except ValueError as v:
            _logger.warn(
                f"Caught {v}, skipping yield prediction for plot {p.plot_id}. Yield will be 0"
            )
            harvests.append(0)
    return harvests
