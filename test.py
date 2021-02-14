from time import sleep
from rich.console import Console
from rich.progress import track, Progress, BarColumn, TimeRemainingColumn

import numpy as np

from tintml import Tint

tint = Tint()

n_datapoints = 100
n_valpoints = 10
n_epochs = 3


## LOAD DATA ##

with tint.status("Initialization"):
    sleep(0.17)
    tint.log("Read command line arguments")
    sleep(0.12)
    tint.log("Set paths")
    sleep(0.28)
    tint.log("Finished initialization")

## TRAINING ##

tint.scope("Training")
sleep(0.3)
prev_val_error = 1.
prev_train_error = 1.

tint.track("Train Loss")

for epoch_idx in range(1,n_epochs+1):

    tint.print(f"Epoch {epoch_idx}/{n_epochs}")

    for i in tint.iter(range(n_datapoints), "Training..."):
        sleep(0.012)
    
    tint.

    train_error = prev_train_error * 0.9 + np.random.normal(0,0.1)
    if train_error == prev_train_error or epoch_idx==1:
        color = "white"
        arrow = ""
    elif train_error < prev_train_error:
        color = "green"
        arrow = ":arrow_lower_right:"
    else:
        color = "red"
        arrow = ":arrow_upper_right:"
    console.print(f"train_loss:\t[{color}]{train_error:.3f} {arrow}[/{color}]")
    prev_train_error = train_error
    
    progress = Progress(
        "[progress.description]{task.description}",
        "{task.completed}/{task.total}",
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
        transient=True,
    )
    
    with progress:
        val_task = progress.add_task(f"[cyan]Validating...", total=n_valpoints)

        for i in range(n_valpoints):
            progress.advance(val_task)
            sleep(0.2)

    val_error = prev_val_error * 0.9 + np.random.normal(0,0.1)
    if val_error == prev_val_error or epoch_idx==1:
        color = "white"
        arrow = ""
    elif val_error < prev_val_error:
        color = "green"
        arrow = ":arrow_lower_right:"
    else:
        color = "red"
        arrow = ":arrow_upper_right:"
    console.print(f"val_loss:\t[{color}]{val_error:.3f} {arrow}[/{color}]")
    prev_val_error = val_error

console.log("Finished training")


## TESTING ##

console.print("\n~~ Testing ~~", style="bold yellow")

with console.status("[green] Setting up testing") as status:
    sleep(1)
    console.log("Read test data")
    sleep(0.5)
    console.log("Applied data augmentations")

console.log("Testing model on unseen data...")

progress = Progress(
    "[progress.description]{task.description}",
    "{task.completed}/{task.total}",
    BarColumn(),
    "[progress.percentage]{task.percentage:>3.0f}%",
    TimeRemainingColumn(),
    transient=True,
)

with progress:

    test_task = progress.add_task(f"[cyan]Predicting...  ", total=n_datapoints)

    for i in range(n_datapoints):
        progress.advance(test_task)
        sleep(0.012)

test_error = prev_val_error + np.random.normal(0,0.1)
console.print(f"test_loss:\t[{color}]{test_error:.3f}[/{color}]")
