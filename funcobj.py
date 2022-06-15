def example():
    print("in example")

alias = example
alias()

def replacement():
    print("in replacement")

example = replacement
example()
