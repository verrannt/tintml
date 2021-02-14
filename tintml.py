from rich.progress import BarColumn, TimeRemainingColumn, Progress, TextColumn
from rich.console import Console

import math
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class Tracker():

    def __init__(self, steps:int, label:str):
        self.steps = steps
        self.label = label

        self.progress = Progress(
            "[progress.description]{task.description}",
            "{task.completed}/{task.total}",
            BarColumn(),
            "[progress.percentage]{task.percentage:>3.0f}%",
            TimeRemainingColumn(),
            transient=True,
        )
        
        self.task = self.progress.add_task(
            "[cyan]{}...  ".format(self.label), total=self.steps)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def advance(self):
        self.progress.advance(self.task)

def iter(
    iterable,
    label: str = "Working...",
    steps: int = None,
):

    progress = Progress(
        "[progress.description]{task.description}",
        "{task.completed}/{task.total}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        transient=True,
    )

    with progress:
        yield from progress.track(
            iterable, total=steps, description=label, update_period=0.1
        )

#class Console():
#    def __init__(self):
#        self.console = Console()
#
#    def section(title):
#        console.print("\n{}\n".format(title), style='bold yellow')
#
#    def print(message):
#        self.console.print(message)
#
#    def log(message):
#        self.console.log(message)

class Console(Console):
    def __init__(self):
        super().__init__()
        self.prev_values = None

    def print_metrics(self, metric_dict, down_is_better, multi_line=False):

        for i, k in enumerate(metric_dict.keys()):
            # No change
            if not self.prev_values or math.isclose(metric_dict[k], self.prev_values[k], rel_tol=1e-3):
                color = "white"
                arrow = " "
            # Improvement
            elif self.compare(metric_dict[k], self.prev_values[k], down_is_better[i]):
                color = "green"
                arrow = self.get_arrow(True, down_is_better[i])
            # Worsened
            else:
                color = "red"
                arrow = self.get_arrow(False, down_is_better[i])
            if multi_line:
                self.print(f"{k}:\t[{color}]{metric_dict[k]:.3f} {arrow}[/{color}]")
            else:
                self.print(f"{k}: [{color}]{metric_dict[k]:.3f} {arrow}[/{color}]", end='  ')
        if not multi_line:
            print()

        self.prev_values = metric_dict
    
    def compare(self, val1, val2, down_is_better):
        if down_is_better:
            return val1 < val2
        else: 
            return val1 > val2

    def get_arrow(self, improvement:bool, down_is_better:bool):
        if improvement:
            return ":arrow_lower_right:" if down_is_better else ":arrow_upper_right:"
        else: 
            return ":arrow_upper_right:" if down_is_better else ":arrow_lower_right:"


class Tint():

    def __init__(self):
        self.console = Console()
        self.current_scope = None
        self.metrics = Metric()

    def print(self, something):
        self.console.print(something)

    def scope(self, title:str):
        self.current_scope = title
        self.console.print("\n{}\n".format(title), style='bold yellow')

    def status(self, title:str):
        return self.console.status("[green]{}".format(title))

    def log(self, message:str):
        self.console.log(message)

class Metrics():
    def __init__(self):
        self.metric_dict = dict()

    def track(self, name:str):
        self.metrics[name] = None

    def update(self, name:str, value:float):
        self.metrics[name] = value

    def print(self):
        