# Abstract

## Overview

Most of the Abstract Base Interfaces implemented for each of the modules are fairly identical. There are nuances in each of the REST API and WSS API implementations which cause some differences to occur. Any differences that do occur will be noted and or outlined to clarify what they are based on implementation.

## AbstractAPI

```python
AbstractAPI()
```

The AbstractAPI defines the REST API URI path utilized by AbstractMessenger.


## AbstractAuth

```python
AbstractAuth()
```

The AbstractAuth defines the REST API Authentication method utilized by AbstractMessenger.

## AbstractMessenger

```python
AbstractMessenger(auth: AbstractAuth)
```

The AbstractMessenger defines the requests adapter utilized to facilitate communication with the REST API.

## AbstractSubscriber

```python
AbstractSubscriber(messenger: AbstractMessenger)
```

The AbstractSubscriber is utilized by inheriting classes that define scoped methods utilized by AbstractClient.

## AbstractClient

```python
AbstractClient(messenger: AbstractMessenger)
```

The AbstractClient defines a friendly interface for utilizing the given REST API.
