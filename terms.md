**ABCs = abstract base classes**

**DRY = don't repeat yourself**

**ECDSA = Elliptic Curve Digital Signature Algorithm**

**Mock = replacing a part of a system with mock objects**

Mock objects are typically intended to be objects that are used in place of the real implementation.
Mock objects are sometimes called test doubles, spies, fakes, or stubs.

**Mock drift = the interface being mocked changes, while the mock in the test code doesn't.**

**Monkey patch = a technique used to dynamically update the behavior of a piece of code at run-time**

**MRO = Method Resolution Order**

MRO determines the sequence of inheritances of attributes and methods
```python
MyClass.__mro__
```

**nop = no operation**

**ORM = Object-Relational Mapping** 

**RAII = Resource acquisition is initialization**

Used in Python with the context manager with two special methods: `__enter__` and `__exit__`.

**REST = Representational State Transfer**

**SOLID = a set of five design principles proposed by Robert C. Martin**

- *Single responsibility principle* (SRP) =
Each class should have one job or responsibility, 
and that job should be encapsulated within that class.

- *Open-closed principle* (OCP) =
Software entities, such as classes and modules, should be open 
for extension (through inheritance or interfaces to accommodate 
new requirements and behaviors) but closed for modification.

- *Liskov substitution principle* (LSP) = 
If a program uses objects of a superclass, then the substitution of them with objects
of a subclass should not change the correctness and expected behavior of the program.

- *Interface segregation principle* (ISP) =
A class should not be forced to implement interfaces it does not use.
In the context of Python, this implies that a class shouldn't be forced 
to inherit and implement methods that are irrelevant to its purpose.

- *Dependency inversion principle* (DIP) =
High-level modules should not depend directly on low-level modules.
Instead, both should depend on abstractions or interfaces.

The DIP is closely linked to the *loose coupling* principle by promoting a design
where components interact through interfaces rather than concrete implementations.

**SSH = Secure Shell Protocol**

SSH is commonly used to remotely manage Unix systems.

**structural duck typing**

If an object walks like a duck and quacks like a duck, it's a duck, regardless of its actual inheritance hierarchy.

**UUID = Universally Unique Identifier**

**YAGNI, YagNi = "You Aren't Gonna Need It"**

"Always implement things when you actually need them, never when you just foresee that you need them" 
https://c2.com/xp/YouArentGonnaNeedIt.html
