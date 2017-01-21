#brap

Brap is a dependency injection container for Python3.


[![Build Status](https://travis-ci.org/Incognito/brap.svg?branch=master)](https://travis-ci.org/Incognito/brap)


##Usage

Create a container

```python
    from brap import Container

    container = Container()
```

Brap contains services and parameters.


##Defining Services

Services are instances that are unlikely to be created multiple times. A
templating service used by a framework that only has one instance is an example
(however, you may decide to create multiple instances for very specific reasons)

Something like a "User" object which represents a row in your user table in the
database is not a service object.

A lambda is used so the container can look up other parameters in that container
at time of creation.


```python
    from brap import Container

    container = Container()

    container.set(
        'file_parser',  # no magic here, string can be anything
        lambda container: ERBFileParser()
    )

    container.set(
        'template_engine', 
        lambda container: TemplateEngine(container.get('file_parser'))
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


##Defining Factory Services

A factory is just like a service, except when you call the factory it will
return a new instance (instead of providing a reference to the single instance
registered in the container).


```python
    container.factory(
        'uuid',
        lambda container: uuid.uuid4()
    )

    container.get('uuid')  # Returns new uuid
```



##Setting Parameters

Parameters are just like services, except they are not callable


```python
    container.set('database_password', 'swordfish')
```


This lets you do things such as:


```python
    container.set(
        'database_connection', 
        lambda container: Database(container.get('database_password'))
    )
```

##Extending a Container

One of the big advantages of picking a DI container is the reusability of a set
of services.

If you have an encapsulated concept that could in theory become a package, you
may wish to define a simple provider interface:



```python
    from brap import ProviderInterface

    class ERBTemplateEngineProvider(ProviderInterface):
        def register(self, container):
            container.set(
                'file_parser',  # no magic here, string can be anything
                lambda container: ERBFileParser(
                    container.get('file_path_parameter')
                )
            )

            container.set(
                'template_engine', 
                lambda container: TemplateEngine(container.get('file_parser'))
            )
```


Now in some other code base you can load all that configuration up:


```python
    container.set('file_path_parameter', '/path/to/templates')
    container.register(ERBTemplateEngineProvider())
    rendered_template = template_engine.render('template.erb', {})
```
