from rich.progress import BarColumn, TimeRemainingColumn, Progress, TextColumn
from rich.console import Console

import math
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Tint():

    def __init__(self):
        self.console = Console()
        self.current_scope = None
        self.metric_dict = dict()
        self.longest_metric = 0
        self.log = self.console.log

    def print(self, something, end='\n'):
        self.console.print(something, end=end)

    def scope(self, title:str):
        self.current_scope = title
        self.console.print("\n{}".format(title), style='bold yellow')

    def status(self, title:str):
        return self.console.status("[green]{}".format(title))

    #def log(self, message:str):
    #    return self.console.log(message)

    def print_metrics(self, metric_dict, down_is_better, multi_line=False):

        for i, k in enumerate(metric_dict.keys()):
            
            if len(k) > self.longest_metric:
                self.longest_metric = len(k)

            # No change (if metric is new or within certain range of 
            # previous value)
            if not k in self.metric_dict or math.isclose(
                    metric_dict[k], self.metric_dict[k], rel_tol=1e-3):
                color = "white"
                arrow = " "
            
            # Metric has improved compared to previous value
            elif self.compare(metric_dict[k], self.metric_dict[k], down_is_better[i]):
                color = "green"
                arrow = self.get_arrow(True, down_is_better[i])
            
            # Metric has worsened compared to previous value
            else:
                color = "red"
                arrow = self.get_arrow(False, down_is_better[i])
            
            n_blanks = " " * (self.longest_metric + 1 - len(k))

            if multi_line:
                self.print(f"{k}:{n_blanks}[{color}]{metric_dict[k]:.3f} {arrow}[/{color}]")
            else:
                self.print(f"{k}: [{color}]{metric_dict[k]:.3f} {arrow}[/{color}]", end=' ')

            # Overwrite previous values
            self.metric_dict[k] = metric_dict[k]

        if not multi_line:
            print()
    
    def get_metrics(self):
        return self.metric_dict

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

    def iter(
        self,
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
        