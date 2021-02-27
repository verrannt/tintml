from time import sleep
from rich.console import Console
from rich.progress import track, Progress, BarColumn, TimeRemainingColumn

import numpy as np

from tintml import Tint

tint = Tint()

n_datapoints = 100
n_valpoints = 10
n_epochs = 4


## LOAD DATA ##

with tint.status("Initialization"):
    sleep(0.17)
    tint.log("Read command line arguments")
    sleep(0.12)
    tint.log("Set paths")
    sleep(0.28)
    tint.log("Finished initialization")


## SET UP MODEL ##

tint.scope('Model Setup')

with tint.status("Setup Model"):
    sleep(1.7)
    tint.log("Defined model graph")
    sleep(1.2)
    tint.log("Loaded model weights")

## TRAINING ##

tint.scope("Training")
sleep(0.3)
prev_val_error = 1.
prev_train_error = 1.

for epoch_idx in range(1,n_epochs+1):

    tint.print(f"Epoch {epoch_idx}/{n_epochs}")

    # Train

    for i in tint.iter(range(n_datapoints), "Training..."):
        sleep(0.012)
    
    train_error = prev_train_error * 0.9 + np.random.normal(0,0.1)
    prev_train_error = train_error
    
    # Val

    for i in tint.iter(range(n_valpoints), "Validating..."):
        sleep(0.05)

    val_error = prev_val_error * 0.9 + np.random.normal(0,0.1)
    prev_val_error = val_error
    
    # Metrics

    tint.print_metrics({
        'Train loss': train_error,
        'Val loss': val_error,
    }, [True, True], multi_line=True)

tint.log("Finished training")


## TESTING ##

tint.scope("Testing")

with tint.status("Setting up testing"):
    sleep(1)
    tint.log("Read test data")
    sleep(1.7)

tint.log("Started testing procedure")

for i in tint.iter(range(n_datapoints), "Testing"):
    sleep(0.012)

test_error = prev_val_error + np.random.normal(0,0.1)
tint.print_metrics({
    'Test loss': test_error
}, [True])


## SAVING ##

tint.scope('Saving')

with tint.status("Saving run"):
    sleep(2)
    tint.log("Saved model weights.")
    sleep(0.8)
    tint.log("Saved metrics.")