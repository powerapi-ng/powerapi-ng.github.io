PowerAPI is a middleware toolkit for building software-defined power meters.
Software-defined power meters are configurable software libraries that can
estimate the power consumption of software in real-time.
As a middleware toolkit, PowerAPI offers the capability of assembling power
meters _«à la carte»_ to accommodate user requirements.
If you want to build your own power meter using PowerAPI, we provide a step by
step guide.

# Creating your own formula

To develop a formula you have to consider the following parts :

- The configuration parameters needed by the actor
- The dispatching rule of the reports to the different formula actors
- The behavior of the formula actor

We provide a [dummy formula](https://github.com/powerapi-ng/dummy-formula) that
contain the template to develop your own formula.
Next we provide a guide on developing your own formula using that template.

## Starting

To develop a formula there is two major tasks. How to handle the formula actor,
and the behavior of the formula actor.

The first thing you need to decide is what will your formula receive as
inputs, how it will treat it and what will it return.
Once you've decide this part you need to extract the parameters needed by the
formula actor.
In the next of this guide we will treat the handling of the formula actor then
we will provide some advices on how to develop your formula actor.

## Handling the actor

Once you've decided the parameters the formula actor will need, we need to build
the chain to pass them from the configuration file to the actor.

First we need to build the parser that will extract the parameters from the
configuration file.
For that part we are working on `generate_dummy_parser` in `__main__.py`.
For each parameters `arg` you should add the following lines :

```python
    parser.add_argument(
        "arg",  # name of the arg
        help="help on arg",  # help to display when --help is used
        type=None,  # type expected
        default=None,  # Default value if not specified
    )
```

Once the configuration is retrieved from the configuration file it is necessary
to check it.
For that we use a `DummyConfigValidator` that will check that each mandatory
arguments are present and that each arguments have the correct type.

At this moment the configuration is a Dictionary, it will be transformed to a
`DummyFormulaConfig` (in `context.py`) to be passed to the actor.
You should put each parameters needed in the formula actor as attribute of that
class.

In addition of the configuration you need to specify the dispatch rule of
`route_table`. This rule decide which report is send to which formula actor.
If you choose SENSOR, reports with the same sensor field will be send to the
same actor. If you choose SOCKET the sort will be made on the `sensor` field.

## Your formula

Now that you actor will receive its parameters, you need to build it.
Your actor will be initialized two times, one as an object and one as an actor.
You first need to define all the attributes as `None` is the `__init__`.
The supervisor will then call ` _initialization` with a `StartMessage`
containing the configuration.

The `receiveMsg_Report(self,message)` method will be used each time a report is
send to the formula actor.
Once you have treated your reports and produced the output reports, send them
to the pushers using the following commands :

```python
for name, pusher in self.pushers.items():
    self.log_debug('send ' + str(report) + ' to ' + name)
    self.send(pusher, report)
```
