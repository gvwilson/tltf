# A Tiny Little Testing Framework

Testing software isn't the most fun you're ever going to have,
but the right tools can make it much less onerous,
and we can learn a lot about how to design software
from looking at how testing tools work.

## It's All Just Dictionaries

How and where do Python and other languages store variables?
The answer is, "In a dictionary."
Run the Python interpreter and call the `globals` function:

```
>>> globals()
{
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': <class '_frozen_importlib.BuiltinImporter'>,
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': <module 'builtins' (built-in)>
}
```

`globals` returns a copy of the dictionary that Python uses
to store all the variables at the top (global) level of your program.
Since we just started the interpreter,
what we get are the variables that Python defines automatically:
it uses double underscores like `__name__` for these variables,
but they're just string keys in a dictionary.

Let's define a variable of our own:

```
>>> my_variable = 123
>>> globals()
{
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': <class '_frozen_importlib.BuiltinImporter'>,
    '__spec__': None,
    '__annotations__': {},
    '__builtins__': <module 'builtins' (built-in)>,
    'my_variable': 123
}
```

There's our variable `my_variable` and its value.

There's another function called `locals` that returns a dictionary full of
all the variables defined in the current (local) scope.
Let's create a function that takes a parameter,
creates a local variable,
and then shows what's in scope:

```python
def show_off(some_parameter):
    some_variable = some_parameter * 2
    print("local values", locals())

show_off("hello")
```
```txt
local values {'some_parameter': 'hello', 'some_variable': 'hellohello'}
```

## Functions Are Just Objects

The second thing we need to understand is that
a function is just another kind of object:
while a string object holds characters
and an image object holds pixels,
a function object holds instructions.
When we write:

```python
def example():
    print("in example")
```

what we're actually doing is saying,
"Please create an object containing the instructions to print a string
and assign it to the variable `example`."
Here's proof:

```python
alias = example
alias()
```
```text
in example
```

We can also assign to the original variable:

```python
def replacement():
    print("in replacement")

example = replacement
example()
```
```text
in replacement
```

Like other objects,
functions have attributes.
We can use `dir` (short for "directory") to get a list of their names:

```python
def example():
    "Docstring for example."
    print("in example")

print(dir(example))
```
```text
[
    '__annotations__', '__builtins__', '__call__', '__class__'
    '__closure__', '__code__', '__defaults__', '__delattr__'
    '__dict__', '__dir__', '__doc__', '__eq__', '__format__' '__ge__',
    '__get__', '__getattribute__', '__globals__' '__gt__', '__hash__',
    '__init__', '__init_subclass__' '__kwdefaults__', '__le__',
    '__lt__', '__module__', '__name__' '__ne__', '__new__',
    '__qualname__', '__reduce__', '__reduce_ex__' '__repr__',
    '__setattr__', '__sizeof__', '__str__', '__subclasshook__'
]
```

I don't know what all of these do,
but `__doc__` holds the documentation string (docstring) for the function
and `__name__` holds its original name:

```
print("docstring:", example.__doc__)
print("name:", example.__name__)
```
```text
docstring: Docstring for example.
name: example
```

## So What?

If a program's variables are stored in a dictionary,
we can iterate over them.
Let's do that to find all the functions whose names start with `test_`:

```python
def test_addition():
    assert 2 + 2 == 4

def test_multiplication():
    assert 3 * 3 == 9

def test_remainder():
    assert 15 % 4 == 0 # this is wrong

def find_tests():
    result = []
    for (name, func) in globals().items():
        if name.startswith("test_"):
            result.append(func)
    return result

print("all the test functions", find_tests())
```
```text
all the test functions [
    <function test_addition at 0x1008d7d90>,
    <function test_multiplication at 0x1009fb010>,
    <function test_remainder at 0x1009fb0a0>
]
```

Remember, a function is just another kind of object in Python:
when we print the function out,
Python shows us its name and its address in memory because---well,
I'm not really sure why,
but it does.
Anyway,
if we have a function we can call it,
which means we can find all the `test_` functions in this file
and call them one by one.

We can do more than just call functions:
we can check if they run to completion or raise an exception
and report that:

```python
def test_addition():
    assert 2 + 2 == 4

def test_multiplication():
    assert 3 * 3 == 9

def test_remainder():
    assert 15 % 4 == 0 # this is wrong

def run_tests():
    for (name, func) in globals().items():
        if name.startswith("test_"):
            try:
                func()
                print(func.__name__, "passed")
            except AssertionError:
                print(func.__name__, "failed")

run_tests()
```
```text
test_addition passed
test_multiplication passed
test_remainder failed
```

> Notice that all the `test_` functions can be called with no arguments.
> If some of them required arguments,
> we'd have to know what it expected and then call it with the right number of values.
> On the other hand,
> if we say that test functions all have the same signature (i.e., parameter list),
> we can call them interchangeably.

## Introducing Pytest

[Pytest][pytest] is a widely used tool for testing Python programs.
It can do a lot of complex things,
but its core is no different from the code we've just seen.
If you install it with `pip install pytest` or `conda install pytest`
and then run `pytest` on the command line without any arguments,
it:

1.  searches recursively in and below your directory for Python files;
2.  looks inside those files for functions called `test_*`,
    such as `test_add` or `test_mul`;
3.  runs each of those functions; and
4.  reports which ones passed and failed.

We can prove this works by creating a file called `test_example.py`:

```python
def test_this():
    assert len("this") == 4

def test_that():
    assert len("that") == 0 # this is wrong
```

Notice that this file only *defines* the functions;
it doesn't call them.
If we tell `pytest` to run just this file,
it tells us that one test passed and one failed
(it prints `.F` to mean "first test passed, second failed"):

```console
$ pytest test_example.py
```
```text
============================= test session starts ==============================
platform darwin -- Python 3.10.4, pytest-7.1.2, pluggy-1.0.0
rootdir: /Users/gvwilson/tiny/tltf
collected 2 items

test_example.py .F                                                       [100%]

=================================== FAILURES ===================================
__________________________________ test_that ___________________________________

    def test_that():
>       assert len("that") == 0 # this is wrong
E       AssertionError: assert 4 == 0
E        +  where 4 = len('that')

test_example.py:5: AssertionError
=========================== short test summary info ============================
FAILED test_example.py::test_that - AssertionError: assert 4 == 0
========================= 1 failed, 1 passed in 0.01s ==========================
```

If we run `pytest` *without* specifying a filename,
it looks in *all* the Python files it can find in or below the current directory
for test functions:

```console
$ pytest
```
```text
find_test.py ..F        [ 37%]
run_test.py ..F         [ 75%]
test_example.py .F      [100%]

...lots more output with details...
```

By convention,
people put their tests in a `tests` directory under the root directory of their project
and call those files `test_*.py`.

## Exercises

1.  Modify `run_test.py` so that `run_tests`
    reports the number of passing and failing tests
    instead of printing each test's name and status as it runs.

2.  Modify `run_test.py` so that if a testing function's docstring contains `test:skip`
    that test is *not* run.
    Instead, `run_tests` prints the function's name and the word "skipped"
    instead of "passed" or "failed".
    For example, this test should be skipped:

    ```
    def test_division():
        "test:skip because we haven't implement division"
        assert 2/2 == 1
    ```

3.  Modify `run_test.py` so that if the user specifies the name(s)
    of one or more tests on the command line,
    only those tests are run.
    For example, `python run_tests.py test_add test_mul` should only run two tests.
    What should the program do if the test the user has asked for doesn't exist?

[pytest]: https://docs.pytest.org/
