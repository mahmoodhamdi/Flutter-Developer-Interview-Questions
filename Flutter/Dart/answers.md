# Flutter Dart: Answers

1. **What is Dart, and how is it used in Flutter?**
   - Dart is a client-optimized programming language developed by Google. It is used in Flutter to build fast, cross-platform mobile, desktop, and web applications. Dart is designed to be easy to learn, efficient, and supports strong typing and object-oriented programming.

2. **Explain the main features of Dart.**
   - Dart has several key features:
     - **Strong typing**: Ensures that types are checked at compile-time.
     - **Null safety**: Helps prevent null reference errors.
     - **Asynchronous programming**: Supports async/await for handling asynchronous operations.
     - **Rich standard library**: Includes a wide range of built-in classes and functions.
     - **Cross-platform support**: Runs on mobile, desktop, and web platforms.
     - **Garbage collection**: Automatically manages memory allocation and deallocation.

3. **What is a var keyword in Dart, and how is it used?**
   - The var keyword in Dart is used to declare a variable without explicitly specifying its type. The type is inferred based on the assigned value. Example:

     ```dart
     var name = 'John'; // Dart infers that 'name' is of type String.
     ```

4. **How do you declare a constant in Dart using the const keyword?**
   - You can declare a constant in Dart using the const keyword. Constants are compile-time constants and must be initialized with a constant value. Example:

     ```dart
     const pi = 3.14159;
     ```

5. **What is the difference between final and const in Dart?**
   - final and const both declare variables that cannot be reassigned. However:
     - final: The value is set at runtime and cannot be changed afterward.
     - const: The value is set at compile-time and is immutable.

6. **How do you define a function in Dart?**
   - A function in Dart is defined using the `returnType functionName(parameters) { ... }` syntax. Example:

     ```dart
     int add(int a, int b) {
       return a + b;
     }
     ```

7. **What are named parameters in Dart, and how are they different from positional parameters?**
   - Named parameters are parameters that are passed using their name, making the function call more readable. Positional parameters are passed based on their position in the function signature. Example of named parameters:

     ```dart
     void greet({String? name, int? age}) {
       print('Hello $name, you are $age years old.');
     }
     ```

8. **How do you use default parameter values in Dart functions?**
   - Default values for parameters can be provided by assigning a value in the function signature. Example:

     ```dart
     void greet({String name = 'Guest'}) {
       print('Hello $name');
     }
     ```

9. **What is a class in Dart, and how do you define one?**
   - A class in Dart is a blueprint for creating objects. It encapsulates data for the object and methods to manipulate that data. Example:

     ```dart
     class Person {
       String name;
       int age;

       Person(this.name, this.age);
     }
     ```

10. **How do you create an instance of a class in Dart?**
    - You can create an instance of a class using the 'new' keyword or directly. Example:

      ```dart
      var person = Person('John', 25); // or new Person('John', 25);
      ```

11. **What is a constructor in Dart, and how do you define one?**
    - A constructor is a special method that is used to initialize objects of a class. It is defined with the same name as the class. Example:

      ```dart
      class Person {
        String name;
        int age;

        Person(this.name, this.age); // Constructor
      }
      ```

12. **How do you define a named constructor in Dart?**
    - A named constructor allows you to provide additional constructors with different names. Example:

      ```dart
      class Person {
        String name;
        int age;

        Person(this.name, this.age);

        Person.withAge(this.age) {
          name = 'Unknown';
        }
      }
      ```

13. **What is inheritance in Dart, and how is it implemented?**
    - Inheritance allows a class to inherit properties and methods from another class. It's implemented using the `extends` keyword. Example:

      ```dart
      class Employee extends Person {
        double salary;

        Employee(String name, int age, this.salary) : super(name, age);
      }
      ```

14. **How do you override a method in Dart?**
    - To override a method, you use the `@override` annotation and redefine the method in the subclass. Example:

      ```dart
      class Employee extends Person {
        @override
        void greet() {
          print('Hello Employee');
        }
      }
      ```

15. **What is polymorphism in Dart, and how is it implemented?**
    - Polymorphism allows methods to do different things based on the object it is acting upon, typically through method overriding. It is implemented by having multiple classes that extend the same superclass and override its methods.

16. **How do you use mixins in Dart?**
    - Mixins allow you to reuse code across multiple classes. You use the `with` keyword to apply a mixin to a class. Example:

      ```dart
      mixin Walkable {
        void walk() {
          print('Walking...');
        }
      }

      class Person with Walkable {}
      ```

17. **What are abstract classes in Dart, and how are they used?**
    - Abstract classes are classes that cannot be instantiated and are used to define a common interface for subclasses. They can have both abstract methods (without implementation) and regular methods. Example:

      ```dart
      abstract class Animal {
        void makeSound(); // Abstract method

        void breathe() {
          print('Breathing...');
        }
      }
      ```

18. **How do you implement an interface in Dart?**
    - In Dart, any class can act as an interface. You implement an interface using the `implements` keyword. Example:

      ```dart
      class Dog implements Animal {
        @override
        void makeSound() {
          print('Bark');
        }

        @override
        void breathe() {
          print('Panting...');
        }
      }
      ```

19. **What is the this keyword in Dart, and how is it used?**
    - The this keyword refers to the current instance of the class. It is used to access class members and differentiate between instance variables and parameters with the same name.

20. **How do you handle exceptions in Dart using the try-catch block?**
    - You handle exceptions using `try-catch`. Example:

      ```dart
      try {
        var result = 10 ~/ 0;
      } catch (e) {
        print('Error: $e');
      }
      ```

21. **What is the throw keyword in Dart, and how is it used to raise exceptions?**
    - The throw keyword is used to raise an exception. Example:

      ```dart
      if (age < 18) {
        throw Exception('Age must be 18 or above');
      }
      ```

22. **How do you use Future and async-await in Dart for asynchronous programming?**
    - Future is used to represent a potential value or error that will be available at some point. async and await are used to handle asynchronous code more synchronously. Example:

      ```dart
      Future<void> fetchData() async {
        var data = await fetchFromServer();
        print(data);
      }
      ```

23. **What is the await keyword in Dart, and how is it used?**
    - The await keyword is used to pause the execution of an async function until a Future is completed. Example:

      ```dart
      var result = await someAsyncFunction();
      ```

24. **How do you use Stream in Dart for handling data streams?**
    - Streams are used to handle a sequence of asynchronous events. You can listen to a stream using stream.listen() Example:

      ```dart
      Stream<int> numberStream = Stream.fromIterable([1, 2, 3]);
      numberStream.listen((number) {
        print(number);
      });
      ```

25. **What is the yield keyword in Dart, and how is it used in generator functions?**
    - The yield keyword is used in generator functions to produce a value each time the function is called. Example:

      ```dart
      Stream<int> numberGenerator() async* {
        yield 1;
        yield 2;
        yield 3;
      }
      ```

26. **How do you implement a getter and setter in Dart?**
    - Getters and setters are used to control access to class properties. Example:

      ```dart
      class Rectangle {
        double _width;

        double get width => _width;

        set width(double value) {
          _width = value;
        }
      }
      ```

27. **What is the late keyword in Dart, and how is it used?**
    - The late keyword is used to declare a non-nullable variable that is initialized after its declaration. Example:

      ```dart
      late String description;

      void initialize() {
        description = 'Initialized';
      }
      ```

28. **How do you use extension methods in Dart?**
    - Extension methods add new functionality to existing libraries. Example:

      ```dart
      extension StringExtension on String {
        String capitalize() {
          return this[0].toUpperCase() + this.substring(1);
        }
      }
      ```

29. **What are closures in Dart, and how are they used?**
    - A closure is a function that has access to variables in its lexical scope, even after the scope has closed. Example:

      ```dart
      Function makeAdder(int addBy) {
        return (int i) => addBy + i;
      }

      var add2 = makeAdder(2);
      print(add2(3)); // 5
      ```

30. **How do you implement a singleton pattern in Dart?**
    - Singleton is a design pattern that restricts a class to a single instance. Example:

      ```dart
      class Singleton {
        Singleton._privateConstructor();

        static final Singleton _instance = Singleton._privateConstructor();

        factory Singleton() {
          return _instance;
        }
      }
      ```

31. **What is a factory constructor in Dart, and how is it different from a regular constructor?**
    - A factory constructor can return an instance of the class or a different class. It is used for implementing design patterns like singleton. Example:

      ```dart
      class Logger {
        static final Logger _instance = Logger._internal();

        factory Logger() {
          return _instance;
        }

        Logger._internal();
      }
      ```

32. **How do you use typedef in Dart for defining function types?**
    - typedef is used to create a custom function type. Example:

      ```dart
      typedef IntOperation = int Function(int a, int b);

      int add(int a, int b) => a + b;
      ```

33. **What is the ?? (null-aware operator) in Dart, and how is it used?**
    - The ?? operator returns the expression on the right if the expression on the left is null. Example:

      ```dart
      String name = null ?? 'Guest'; // 'Guest' will be assigned to name.
      ```

34. **How do you handle null safety in Dart?**
    - Dart uses null safety to prevent null reference errors. Variables can be declared as non-nullable by default, and nullable types are indicated with a `?`. Example:

      ```dart
      String? name; // Nullable
      String nonNullableName = 'John'; // Non-nullable
      ```

35. **What is the ?. (null-aware access) operator in Dart, and how is it used?**
    - The ?. operator allows you to call a method or access a property on an object only if it is non-null. Example:

      ```dart
      String? name;
      print(name?.toUpperCase()); // Will not throw an error if name is null.
      ```

36. **How do you use forEach in Dart to iterate over a collection?**
    - forEach is used to iterate over elements in a collection. Example:

      ```dart
      var numbers = [1, 2, 3];
      numbers.forEach((number) {
        print(number);
      });
      ```

37. **What is the Map data structure in Dart, and how is it used?**
    - A Map in Dart is a collection of key-value pairs. Example:

      ```dart
      var map = {'name': 'John', 'age': 25};
      print(map['name']); // Access value by key
      ```

38. **How do you use the List data structure in Dart?**
    - List is an ordered collection of items. Example:

      ```dart
      var numbers = [1, 2, 3];
      numbers.add(4); // Add an element
      ```

39. **What is the Set data structure in Dart, and how is it different from List?**
    - A Set is an unordered collection of unique items, while a List can contain duplicates. Example:

      ```dart
      var numbers = {1, 2, 3};
      numbers.add(1); // No effect, as 1 is already in the set
      ```

40. **How do you use the Iterable class in Dart?**
    - Iterable is an abstract class representing a collection that can be iterated. Example:

      ```dart
      Iterable<int> numbers = [1, 2, 3];
      for (var number in numbers) {
        print(number);
      }
      ```

41. **What is the enum keyword in Dart, and how is it used to define enumerations?**
    - An enum is used to define a set of named values.
      - Example:

       ```dart
      enum Colors { red, green, blue }
      ```

42. **How do you create a custom annotation in Dart?**
    - Custom annotations are created by defining a class and using @ to apply the annotation. Example:

      ```dart
      class MyAnnotation {
        final String description;

        const MyAnnotation(this.description);
      }

      @MyAnnotation('This is a custom annotation')
      class MyClass {}
      ```

43. **What is the const constructor in Dart, and how is it different from a regular constructor?**
    - A const constructor creates compile-time constants, while a regular constructor creates instances at runtime. Example:

      ```dart
      class Point {
        final int x, y;

        const Point(this.x, this.y); // const constructor
      }
      ```

44. **How do you use the assert statement in Dart for debugging?**
    - The assert statement is used to check for conditions during development. If the condition is false, it throws an error. Example:

      ```dart
      int age = 15;
      assert(age >= 18, 'Age must be 18 or older.');
      ```

45. **What is the is keyword in Dart, and how is it used for type checking?**
    - The is keyword checks if an object is of a specific type. Example:

      ```dart
      if (person is Student) {
        print('Person is a student');
      }
      ```

46. **How do you implement generics in Dart?**
    - Generics allow you to create classes, methods, and functions that can operate on different data types. Example:

      ```dart
      class Box<T> {
        T content;

        Box(this.content);
      }
      ```

47. **What is a dynamic type in Dart, and how is it different from Object?**
    - dynamic allows a variable to hold any type, with type checking deferred until runtime. Object is the base class for all types but still has type checking at compile-time. Example:

      ```dart
      dynamic variable = 'Hello'; // Can be any type
      Object object = 'Hello'; // Type-checked at compile-time
      ```

48. **How do you use the async keyword in Dart for asynchronous functions?**
    - The async keyword is used to declare a function that will perform asynchronous operations. Example:

      ```dart
      Future<void> fetchData() async {
        var data = await getData();
        print(data);
      }
      ```

49. **What is the deferred keyword in Dart, and how is it used for lazy loading?**
    - deferred is used for lazy loading libraries, meaning they are loaded only when needed. Example:

      ```dart
      import 'package:some_package/some_lib.dart' deferred as someLib;

      Future<void> loadLibrary() async {
        await someLib.loadLibrary();
        someLib.someFunction();
      }
      ```

50. **How do you implement an iterator in Dart?**
    - An iterator is implemented by defining a class that implements the Iterator interface and providing methods like moveNext and current. Example:

      ```dart
      class NumberIterator implements Iterator<int> {
        int _current = 0;
        final int _max;

        NumberIterator(this._max);

        @override
        int get current => _current;

        @override
        bool moveNext() {
          _current++;
          return _current <= _max;
        }
      }
      ```

## Dart 3.x — Modern features (2026)

51. **What are records in Dart 3, and when should you reach for one instead of a class?**
    Records are anonymous, immutable, value-typed aggregates. They are useful for returning multiple values, structural data passing, and ad-hoc tuples without declaring a class. Two records with the same shape and equal fields are `==` equal — no `hashCode`/`==` boilerplate needed.

    ```dart
    // Positional and named fields can be mixed.
    ({String name, int age}) parseUser(String csv) {
      final parts = csv.split(',');
      return (name: parts[0], age: int.parse(parts[1]));
    }

    final user = parseUser('Aisha,29');
    print('${user.name} is ${user.age}');
    ```

    Reach for a class when behavior, invariants, or named identity matter. Reach for a record when the shape *is* the meaning.

52. **How does pattern matching work in Dart 3 with `switch` expressions and `if-case`?**
    Patterns destructure values and bind variables in one step. `switch` is now an expression (returns a value) and supports record, list, map, object, and constant patterns. `if-case` runs a single pattern test.

    ```dart
    String describe(Object o) => switch (o) {
      (int x, int y) when x == y => 'diagonal at $x',
      [int first, ..., int last] => 'list $first..$last',
      {'name': String name} => 'map with name $name',
      Rectangle(width: var w, height: var h) => '$w x $h rect',
      _ => 'other',
    };

    if (response case {'status': 200, 'body': String body}) {
      print('OK: $body');
    }
    ```

53. **What are class modifiers (`base`, `final`, `interface`, `sealed`, `mixin class`) and what does each guarantee?**
    Dart 3 added explicit modifiers so libraries can control how their classes are subclassed *outside* the defining library:
    - `base` — must be extended (not implemented) outside the library; preserves invariants of the implementation.
    - `interface` — must be implemented (not extended); the class becomes purely a contract for outside code.
    - `final` — cannot be extended or implemented outside the library; closed for outside subtyping.
    - `sealed` — implicitly abstract + final + listable; the compiler knows the closed set of subtypes (great for exhaustive `switch`).
    - `mixin class` — usable both as a regular class and as a mixin.

    ```dart
    sealed class Shape {}
    final class Circle extends Shape { final double r; Circle(this.r); }
    final class Square extends Shape { final double side; Square(this.side); }

    double area(Shape s) => switch (s) {
      Circle(:final r) => 3.14159 * r * r,
      Square(:final side) => side * side,
    }; // exhaustive — no default needed.
    ```

54. **What is an extension type (Dart 3.3+), and how does it differ from `extension`?**
    An extension type wraps an existing type with a new static type and zero runtime cost (no allocation, no boxing). Unlike a regular `extension`, it can hide the underlying type and prevent accidental mixing.

    ```dart
    extension type UserId(int value) {
      bool get isAnonymous => value == 0;
    }

    void grant(UserId id) { /* ... */ }
    grant(UserId(42));        // OK
    // grant(42);             // compile error — int is not UserId
    ```

    Use it for newtype-style typing (IDs, currency, units) without runtime overhead.

55. **How do you exhaustively handle a `sealed` class hierarchy with a `switch` expression?**
    Because the compiler sees the closed set of subtypes, a `switch` expression over a `sealed` type is exhaustive without a default arm. Missing a subtype is a compile-time error — refactor safety you can't get from enums plus `is` checks.

    ```dart
    sealed class AuthState {}
    final class LoggedOut extends AuthState {}
    final class LoggingIn extends AuthState {}
    final class LoggedIn extends AuthState { final String token; LoggedIn(this.token); }

    Widget render(AuthState s) => switch (s) {
      LoggedOut() => const LoginButton(),
      LoggingIn() => const CircularProgressIndicator(),
      LoggedIn(:final token) => HomeScreen(token: token),
    };
    ```

56. **How do `late final` variables differ from `final` and `const`?**
    - `const` — compile-time constant; value is known at compilation.
    - `final` — assigned once at construction time; value is known at object creation.
    - `late final` — assigned once, but on first read instead of construction; useful for expensive initialization that depends on `this`, or for non-nullable fields whose value isn't available at construction time.

    ```dart
    class Profile {
      late final String fullName = _computeFullName();  // computed on first read
      late final List<Order> orders;                    // assigned later, exactly once
      String _computeFullName() => '$_first $_last';
      // ...
    }
    ```

57. **What is the difference between named records like `({int x, int y})` and positional records like `(int, int)`?**
    Positional records use field positions: `(int, int)` is accessed via `.$1`, `.$2`. Named records use field names: `({int x, int y})` is accessed via `.x`, `.y`. Records can mix both.

    ```dart
    (int, int) origin() => (0, 0);
    final o = origin();
    print(o.$1);            // 0

    ({double lat, double lng}) home() => (lat: 30.0, lng: 31.0);
    final h = home();
    print(h.lat);           // 30.0
    ```

    Equality and `toString` are structural in both cases.

58. **How do you destructure a record or a list with patterns in a single statement?**
    Dart supports destructuring in variable declarations and parameters via patterns.

    ```dart
    final (name, age) = ('Aisha', 29);          // record destructuring
    final [first, ..., last] = [1, 2, 3, 4];     // list pattern with rest
    final {'lat': lat, 'lng': lng} = position;   // map destructuring

    // Inline in a switch:
    int sumPair(Object o) => switch (o) {
      (int a, int b) => a + b,
      _ => 0,
    };
    ```

59. **When is a `sealed` class preferred over an enum for modeling state?**
    Use an enum when variants are *plain markers*. Use a `sealed` class when variants *carry data*, when you need exhaustive matching with payloads, or when you want subtype-specific methods.

    ```dart
    // Enum: no payload.
    enum FeedSort { newest, top, controversial }

    // Sealed: payloads + exhaustive switch.
    sealed class FeedState {}
    final class FeedLoading extends FeedState {}
    final class FeedError extends FeedState { final Object error; FeedError(this.error); }
    final class FeedData extends FeedState { final List<Post> posts; FeedData(this.posts); }
    ```

60. **How does Dart's sound null safety differ from the older optional-types model?**
    Sound null safety means the type system is *sound*: a non-nullable type at compile time is guaranteed not to be null at run time, no exceptions. The previous "optional types" model in older Dart was advisory — you could store null in any type. Sound null safety brings three practical changes: variables must be initialized before use, the `?` and `!` operators are explicit, and the runtime can omit some null checks for performance.

    ```dart
    String name = 'Aisha';        // non-nullable
    String? maybeName;            // nullable
    final length = maybeName?.length ?? 0;  // safe access
    final shout = maybeName!.toUpperCase(); // throws if null — explicit risk
    ```
