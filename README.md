# TintML

**Bring color to your machine learning projects!**

![](https://raw.githubusercontent.com/verrannt/tintml/main/assets/tintml-screenshot-3.png)

Tint spices up your machine learning projects by bringing colors to your terminal. Apart from looking awesome, Tint makes it easier to disentangle the information printed by your scripts.


## How To Use Tint

To use Tint, simply copy the file `tintml.py` into your project's root directory, and add

```py
from tintml import Tint
```

to the top of your script. In order to access all of Tint's functions, instantiate it as:

```py
tint = Tint()
```

Tint has five main functions that can be easily incorporated into your scripts and allow Tint to render colorful outputs. These are:

### Print

`print` is to be used like the ordinary Python print statement, and replaces some of the colours used. `printh` prints the text it's provided with in bold yellow, which is useful for headlines when entering a new part of the script. For example, you can use `printh` when processing data, training or testing your model, to differentiate the different parts of the script visually. 

```py
# Enter the 'Training' part of your script
tint.printh('Training')

for i in range(1, n_epochs+1):
    tint.print(f'Epoch {i}/{n_epochs}')

    # ... do your computations
```

### Log

`log` prints status messages onto the terminal. It takes a text that is printed onto the terminal together with the current time and the current line number of the executed file.

```py
tint.log('Defined model graph')
```

### Status

With `status`, you can pin a notification of what's currently being done to the script's output. Just wrap the code during execution of which you want to show the status message in a `with tint.status()` statement, like so:

```py
with tint.status('Processing'):
    # ... do something
    tint.log('Finished Part 1')
    # ... do some more
    tint.log('Finished Part 2')
```

### Print Metrics

Tint also allows you to print metrics you obtain during training or testing of your models to the terminal. It even keeps track of their values and shows you if the values have improved or not!

To print metrics, simply call `print_metrics` for each iteration of your training loop, or whenever you want to show your metrics. `print_metrics` accepts three arguments:

* `metric_dict`: This is a dictionary denoting the metrics you want to print. The keys will be names as shown in the terminal, and the values the corresponding values of the respective metric. Tint automatically keeps track internally whether the metric has improved or worsened as compared to the last time `print_metrics` was called.
* `low_is_better`: A list of boolean values that denotes whether for a given metric a lower value or higher value is preferred. For example, you may want to maximize the accuracy of your classifier, or minimize some loss function. This has to be handed to Tint so that it nows how to color the output. The list has to have the same number of elements as there are key-value-pairs in `metric_dict`.
* `multi_line`: Whether the metrics should be printed in one line after each other, or every metric should be printed in a new line.

`print_metrics` is easy to use. Here's an example:

```py
for epoch in range(1,n_epochs+1):

    # Train
    for i in range(n_datapoints):
        train_loss = train_step()
    
    # Validate
    for i in range(n_valpoints):
        val_loss = val_step()

    # Print Metrics
    tint.print_metrics({
        'Train loss': train_error,
        'Val loss': val_error,
    }, low_is_better=[True, True], multi_line=True)
```

### Iter: Progress Notifier

Tint also provides a way to track the progress of an iterator as it may be used in a for-loop when your model is processing data. To use it, simply wrap your iterator with `tint.iter` and give it an appropriate name:

```py
for i in tint.iter(range(n_datapoints), 'Training...'):
    train_loss = train_step()
```

## Example

See the provided `example_run.py` script for an artificial ML training script to highlight the usage of Tint. It does not compute anything and just sleeps a while at each execution step, but may act as inspiration for how to incorporate Tint into your project. You can run it with `python example_run.py` to see Tint in action.

## Tensorflow Specifics

Please note that Tensorflow renders a lot of status messages from its C++ backend onto the terminal output. These aren't always necessary and make the output look pretty confusing. Luckily, Tint can automatically disable these message by raising the minimum log level for the Tensorflow C++ backend. This only comes into effect if you import Tint *before* importing any Tensorflow libraries in your script. Thus, if you need the Tensorflow status messages, simpy import Tint *after* importing your Tensorflow libraries.

## Acknowledgements

Tint is just me using [Rich](https://github.com/willmcgugan/rich) to bring color to my machine learning projects. Thus, all kudos go to [Will McGugan](https://github.com/willmcgugan), the creator of Rich! In fact, apart from `print_metrics`, Tint is just a wrapper around some of Rich's functionality, and is deliberately lacking any customization possibilities so you can focus on doing ML. Rich on the other hand is a wonderful library full of features, so please go check it out!