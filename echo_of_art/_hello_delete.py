


class Foo:
  def __init__(self)->None:
    print("__init__")
  def __del__(self)->None:
    print("__del__")

try:
  foo = Foo()
  raise "foo"
finally:
  print("finally")

print("after finally")
