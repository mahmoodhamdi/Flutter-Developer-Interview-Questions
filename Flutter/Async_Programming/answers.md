# Flutter Async Programming: Interview Answers

1. **Future vs Stream in Dart?**
   Future represents a single async operation, while Stream is a sequence of async events over time.

2. **Creating a Future in Dart?**

   ```dart
   Future<String> fetchData() async {
     return await http.get('https://api.example.com/data');
   }
   ```

3. **Purpose of async and await?**
   `async` marks a function as asynchronous, `await` waits for a Future to complete.

4. **Handling errors in async code?**
   Use try-catch blocks:

   ```dart
   try {
     await fetchData();
   } catch (e) {
     print('Error: $e');
   }
   ```

5. **Completer in Dart?**
   Used to create and complete a Future manually:

   ```dart
   final completer = Completer<String>();
   completer.complete('Done');
   ```

6. **Creating a Stream in Dart?**

   ```dart
   Stream<int> countStream(int max) async* {
     for (int i = 1; i <= max; i++) {
       yield i;
     }
   }
   ```

7. **Single vs broadcast streams?**
   Single subscription streams can only be listened to once, broadcast streams allow multiple listeners.

8. **Using StreamBuilder in Flutter?**

   ```dart
   StreamBuilder<int>(
     stream: countStream(10),
     builder: (context, snapshot) {
       if (snapshot.hasData) {
         return Text('${snapshot.data}');
       }
       return CircularProgressIndicator();
     },
   )
   ```

9. **FutureBuilder in Flutter?**
   Builds widgets based on the latest snapshot of interaction with a Future:

   ```dart
   FutureBuilder<String>(
     future: fetchData(),
     builder: (context, snapshot) {
       if (snapshot.hasData) {
         return Text(snapshot.data!);
       }
       return CircularProgressIndicator();
     },
   )
   ```

10. **Cancelling a stream subscription?**

    ```dart
    final subscription = stream.listen((data) {
      print(data);
    });
    subscription.cancel();
    ```

11. **async* and sync* functions?**
    `async*` defines an asynchronous generator (returns Stream), `sync*` defines a synchronous generator (returns Iterable).

12. **Using await with multiple futures?**

    ```dart
    final result1 = await fetchData1();
    final result2 = await fetchData2();
    ```

13. **StreamTransformer?**
    Modifies or filters stream events:

    ```dart
    stream.transform(StreamTransformer.fromHandlers(
      handleData: (data, sink) {
        sink.add('Number: $data');
      },
    )).listen(print);
    ```

14. **Handling timeouts in async code?**

    ```dart
    try {
      await fetchData().timeout(Duration(seconds: 5));
    } on TimeoutException catch (e) {
      print('Operation timed out');
    }
    ```

15. **then method in Future?**
    Handles successful Future completion:

    ```dart
    fetchData().then((result) {
      print('Data: $result');
    }).catchError((error) {
      print('Error: $error');
    });
    ```

16. **Chaining async operations?**

    ```dart
    fetchData1()
      .then((result1) => fetchData2(result1))
      .then((result2) => fetchData3(result2));
    ```

17. **async package?**
    Provides additional utilities for Futures and Streams, like AsyncCache and LazyStream.

18. **Implementing Future.delayed?**

    ```dart
    Future.delayed(Duration(seconds: 2), () {
      print('Delayed operation');
    });
    ```

19. **rxdart package?**
    Extends Dart's Stream API with ReactiveX-inspired operators:

    ```dart
    final subject = BehaviorSubject<int>();
    subject.add(1);
    subject.stream.listen(print);
    ```

20. **Handling HTTP requests asynchronously?**

    ```dart
    Future<String> fetchData() async {
      final response = await http.get(Uri.parse('https://api.example.com/data'));
      if (response.statusCode == 200) {
        return response.body;
      } else {
        throw Exception('Failed to load data');
      }
    }
    ```

21. **Future.wait?**
    Waits for multiple Futures to complete:

    ```dart
    final results = await Future.wait([fetchData1(), fetchData2(), fetchData3()]);
    ```

22. **Handling multiple streams with MergeStream?**

    ```dart
    final mergedStream = MergeStream([stream1, stream2, stream3]);
    mergedStream.listen(print);
    ```

23. **StreamController?**
    Creates and manages a Stream:

    ```dart
    final controller = StreamController<int>();
    controller.add(1);
    controller.stream.listen(print);
    controller.close();
    ```

24. **Lazy loading with Stream?**

    ```dart
    Stream<int> lazyNumbers() async* {
      for (int i = 1; i <= 5; i++) {
        await Future.delayed(Duration(seconds: 1));
        yield i;
      }
    }
    ```

25. **StreamSubscription?**
    Represents a subscription to a Stream:

    ```dart
    final subscription = stream.listen(
      (data) => print('Data: $data'),
      onError: (error) => print('Error: $error'),
      onDone: () => print('Stream is done'),
    );
    ```

26. **Creating a never-completing Future?**

    ```dart
    Future<void> neverComplete() => Completer<void>().future;
    ```

27. **await for with streams?**
    Iterates over a Stream asynchronously:

    ```dart
    await for (final value in countStream(5)) {
      print(value);
    }
    ```

28. **Completer for manual future completion?**

    ```dart
    Completer<String> completer = Completer<String>();
    Future<String> future = completer.future;
    completer.complete('Done');
    ```

29. **Future.microtask?**
    Schedules a task in the microtask queue, higher priority than regular event queue:

    ```dart
    Future.microtask(() => print('Microtask'));
    ```

30. **Stream.periodic?**
    Creates a periodic stream:

    ```dart
    Stream.periodic(Duration(seconds: 1), (i) => i).take(5).listen(print);
    ```

31. **FutureOr type?**
    Represents a value that can be either a Future<T> or T:

    ```dart
    FutureOr<int> getValue(bool immediate) {
      return immediate ? 42 : Future.value(42);
    }
    ```

32. **Async/await with providers?**

    ```dart
    class DataProvider extends ChangeNotifier {
      Future<void> fetchData() async {
        // Fetch data
        notifyListeners();
      }
    }
    ```

33. **Async programming benefits?**
    Improves app responsiveness by allowing non-blocking execution of time-consuming operations.

34. **Error handling in async functions?**

    ```dart
    try {
      await fetchData();
    } catch (e) {
      print('Error: $e');
    }
    ```

35. **Zone in Dart?**
    Provides a way to persist context across async operations and handle uncaught errors.

36. **Custom stream with StreamTransformer?**

    ```dart
    Stream<String> transformNumbers(Stream<int> stream) {
      return stream.transform(StreamTransformer<int, String>.fromHandlers(
        handleData: (int data, EventSink<String> sink) {
          sink.add('Number: $data');
        },
      ));
    }
    ```

37. **Stream.listen?**
    Subscribes to a stream and handles its events:

    ```dart
    stream.listen(
      (data) => print('Received: $data'),
      onError: (error) => print('Error: $error'),
      onDone: () => print('Stream is done'),
    );
    ```

38. **Handling event streams in Flutter?**
    Use StreamBuilder or StreamProvider to rebuild UI based on stream events.

39. **StreamBuilder's initialData?**
    Provides an initial value before the stream emits its first event:

    ```dart
    StreamBuilder<int>(
      stream: countStream,
      initialData: 0,
      builder: (context, snapshot) => Text('Count: ${snapshot.data}'),
    )
    ```

40. **Converting Stream to Future?**

    ```dart
    Future<List<int>> streamToFuture(Stream<int> stream) => stream.toList();
    ```

41. **async keyword usage?**
    Used to define asynchronous functions that contain await expressions or return a Future.

42. **Countdown timer with Future?**

    ```dart
    Future<void> countdown(int seconds) async {
      for (int i = seconds; i > 0; i--) {
        print(i);
        await Future.delayed(Duration(seconds: 1));
      }
    }
    ```

43. **StreamController's add method?**
    Adds events to a stream controlled by a StreamController:

    ```dart
    final controller = StreamController<int>();
    controller.add(1);
    ```

44. **Stream emitting values based on user input?**

    ```dart
    final controller = StreamController<String>();
    TextField(onChanged: controller.add);
    controller.stream.listen(print);
    ```

45. **StreamTransformer in data manipulation?**
    Used to modify, filter, or transform stream events.

46. **Combining multiple futures?**

    ```dart
    final results = await Future.wait([fetchUser(), fetchPosts(), fetchComments()]);
    ```

47. **Stream.where for filtering?**

    ```dart
    final evenNumbers = numberStream.where((number) => number % 2 == 0);
    ```

48. **Progress indicator for async tasks?**
    Use StreamBuilder with a progress stream to update a LinearProgressIndicator.

49. **Async vs synchronous programming?**
    Async allows concurrent operations without blocking, sync executes sequentially and blocks until each operation completes.

50. **Background tasks in Flutter?**
    Use packages like workmanager or flutter_background_service to schedule and execute background tasks, even when the app is not in the foreground.
