# TintML

## Bring color to your machine learning projects!

Tint spices up your machine learning projects by bringing colors to your terminal. Apart from looking awesome, Tint makes it easier to disentangle the information printed by your scripts.

![](https://raw.githubusercontent.com/verrannt/tintml/main/assets/tintml-screenshot-1.png)

To use Tint, simply copy the file `tintml.py` file into your project's root directory, and add

```py
from tintml import Tint
```

to the top of you training script. In order to access all of Tint's functions, instantiate it as:

```py
tint = Tint()
```

## How To Use Tint

Tint has five main functions that can be easily incorporated into your scripts and allow Tint to render colorful outputs. These are:

* `scope`: Print yellow bold text, usable for headlines
* `status`: Print a status message underneath



## Tensorflow Specifics

Tensorflow renders a lot of status messages from its C++ backend onto the terminal output. These aren't always necessary and make the output look pretty confusing. Luckily, Tint can automatically disable these message by raising the minimum log level for the Tensorflow C++ backend. This only comes into effect if you import Tint *before* importing any Tensorflow libraries in your script. Thus, if you need the Tensorflow status messages, simpy import Tint *after* importing your Tensorflow libraries.

## Acknowledgements

