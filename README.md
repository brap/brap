# brap

Brap is a dependency injection container for Python3.


[![Build Status](https://travis-ci.org/brap/brap.svg?branch=master)](https://travis-ci.org/Incognito/brap)


## Features!

* All the usual reasons you want to use DI
* Detect circular dependencies
* Detect missing dependencies
* ProviderInterface promotes simple ecosystem interoperability
* Inject via constructor
* Inject via method calls
* Define parameters into the container (Useful for a filesystem path or similar ideas)
* Factories, for when you don't want the same instance
* You get a reason to say "brap" in real life

## Usage

Create a container

```python
    from brap import Container

    container = Container()
```

Brap contains services and parameters.


## Defining Services

Services are instances that are unlikely to be created multiple times. A
templating service used by a framework that only has one instance is an example
(however, you may decide to create multiple instances for very specific reasons)

Something like a "User" object which represents a row in your user table in the
database is not a service object.

A lambda is used so the container can look up other parameters in that container
at time of creation.


```python
    from brap import Container

    # Ideally, the classes would be in a different file and imported here
    class ERBFileParser(object):
        pass

    class TemplateEngine(object):
        def __init__(self, parser):  # We want to inject the ERB parser here
            self._parser = parser

    container = Container()  # Create one instance of a container

    container.set(
        'file_parser',  # no magic here, string can be anything
        ERBFileParser  # Do not invoke constructor
    )

    container.set(
        'template_engine',
        TemplateEngine,
        lambda c: c('file_parser')  # Reference to service injected to TemplateEngine
    )
```

If you are ready to use the template engine, use the same instance of container
from above to get (the container is not global).


```python
    template_engine = container.get('template_engine')

    rendered_template = template_engine.render('some_ruby_template.erb', {
        name: "Rick Deckard"
        credit_card_number: "5221 2624 8015 6007"
        cv2_code: "117"
        expiry: "1219"
    })
```

If your service requires injection-via-method that can be done by adding a method calling list:

```
    class Foo(object):
        def injectMethod(self, parser):

    container.set(
        'template_engine',
        TemplateEngine,
        lambda c: c()  # No constructor parameters in this example
        [
            ('injectMethod', lambda c: c('file_parser'))  # List method calls here
        ]
    )
```

If your service requires injection-via-kwarg simply specify it in your lambda:

```
    class Foo(object):
        def __init__(self, some_kwarg):

    container.set(
        'template_engine',
        TemplateEngine,
        lambda c: c(some_kwarg='file_parser')  # Reference by kwarg in lambda
    )
```

## Defining Factory Services

Factories are no longer directly part of brap.

They can be accomplished by creating a function which returns a new instance,
or adding a compiler which will create them for you.


## Setting Parameters

Parameters are just like services, except they are not callable


```python
    container.set('database_password', 'swordfish')
```


This lets you do useful things such as:


```python
    container.set(
        'database_connection',
        Database,
        lambda c: c('database_password')
    )
```


## Defining Functions As Services

As it is hard to determine if a function is pure, all functions will execute
each time with each parameter set instead of memoizing.

```python
    def some_function(x)
        return x+1

    container.set('x_value', 100)

    container.set(
        'fn_ser',
        some_function
        lambda c: c('x_value')
    )

    container.get('fn_ser')  # Returns 101
    container.get('fn_ser')  # Also returns 101
```

For your own sanity, please be careful to not create impure functions with side
efects.


## Providing Configuration to a Container

One of the big advantages of picking a DI container is the reusability of a set
of services.

If you have an encapsulated concept that could in theory become a package, you
may wish to define a simple provider interface:


```python
    from brap import Container

    vendor_container = Container()

    thirdPartyContainer.set(
        'file_parser',  # no magic here, string can be anything
        ERBFileParser,  # Class we're using
        lambda c: c('file_path_parameter')  # Services/parameters injected into constructor
    )

    thirdPartyContainer.set(
        'template_engine',
        TemplateEngine,
        lambda c: c('file_parser')
    )
```


Now in some other code base you can load all that configuration up:


```python
    container.set('file_path_parameter', '/path/to/templates')
    container.merge(vendor_container)
    rendered_template = container.get('template_engine').render('template.erb', {})
```

This will only introduce new values in the container that were part of the
vendor_container, existing keys will not be over-written, vendor_container is
not modified.
