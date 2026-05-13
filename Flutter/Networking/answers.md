# Flutter Networking: Answers

1. **What is the http package used for in Flutter?**
   The `http` package is used to make HTTP requests to APIs, allowing Flutter apps to communicate with web services.

2. **How do you make a GET request using the http package?**
   You can make a GET request using the following code:

   ```dart
   import 'package:http/http.dart' as http;

   Future<void> fetchData() async {
     final response = await http.get(Uri.parse('https://api.example.com/data'));
     if (response.statusCode == 200) {
       // Process the response
     } else {
       throw Exception('Failed to load data');
     }
   }
   ```

3. **How do you handle errors when making API calls?**
   Use a try-catch block to handle errors and check the response status code. For example:

   ```dart
   try {
     final response = await http.get(Uri.parse('https://api.example.com/data'));
     if (response.statusCode != 200) {
       throw Exception('Failed to load data');
     }
   } catch (error) {
     // Handle error
   }
   ```

4. **What is the difference between GET and POST requests?**
   GET requests retrieve data from the server, while POST requests send data to the server. GET requests include parameters in the URL, whereas POST requests include data in the body.

5. **How can you send JSON data in a POST request?**
   You can send JSON data by encoding the data and specifying the content type:

   ```dart
   import 'dart:convert';

   Future<void> postData() async {
     final response = await http.post(
       Uri.parse('https://api.example.com/data'),
       headers: {'Content-Type': 'application/json'},
       body: json.encode({'key': 'value'}),
     );
   }
   ```

6. **What are headers, and how do you use them in requests?**
   Headers are key-value pairs sent with HTTP requests to provide additional information. You can specify headers in a request like this:

   ```dart
   final response = await http.get(
     Uri.parse('https://api.example.com/data'),
     headers: {'Authorization': 'Bearer token'},
   );
   ```

7. **How do you handle response data from an API call?**
   You can handle response data by decoding it and converting it into a model:

   ```dart
   if (response.statusCode == 200) {
     final data = json.decode(response.body);
     // Convert data to model
   }
   ```

8. **What is the purpose of the Dio package?**
   Dio is a powerful HTTP client for Dart that provides advanced features like interceptors, request cancellation, file downloading, and more.

9. **How do you implement request timeouts using Dio?**
   You can set a timeout when creating the Dio instance:

   ```dart
   Dio dio = Dio(BaseOptions(
     connectTimeout: 5000, // 5 seconds
     receiveTimeout: 3000, // 3 seconds
   ));
   ```

10. **How can you handle pagination in API responses?**
    You can handle pagination by sending parameters for the page and limit in your API requests:

    ```dart
    final response = await http.get(
      Uri.parse('https://api.example.com/data?page=1&limit=10'),
    );
    ```

11. **What is the role of the connectivity package?**
    The `connectivity` package is used to check the network connectivity status of the device, allowing you to determine if the app can access the internet.

12. **How do you perform a PUT request using the http package?**
    You can perform a PUT request like this:

    ```dart
    final response = await http.put(
      Uri.parse('https://api.example.com/data/1'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'key': 'new value'}),
    );
    ```

13. **What are interceptors in Dio, and how are they used?**
    Interceptors in Dio allow you to intercept requests and responses before they are processed, useful for logging, modifying requests, or handling errors.

14. **How do you download files using Dio?**
    You can download files using Dio’s `download` method:

    ```dart
    await dio.download('https://example.com/file.pdf', 'local/path/file.pdf');
    ```

15. **How do you upload files using http?**
    You can upload files using the `http.MultipartRequest` class:

    ```dart
    var request = http.MultipartRequest('POST', Uri.parse('https://api.example.com/upload'));
    request.files.add(await http.MultipartFile.fromPath('file', 'path/to/file'));
    final response = await request.send();
    ```

16. **What is the purpose of the flutter_secure_storage package in networking?**
    The `flutter_secure_storage` package is used to securely store sensitive data, such as API tokens, ensuring they are not exposed.

17. **How do you cancel a network request in Dio?**
    You can cancel requests by using a `CancelToken`:

    ```dart
    CancelToken cancelToken = CancelToken();
    dio.get('https://api.example.com/data', cancelToken: cancelToken);
    cancelToken.cancel('Request canceled');
    ```

18. **What is the difference between synchronous and asynchronous HTTP requests?**
    Synchronous requests block the execution until a response is received, while asynchronous requests allow the program to continue running while waiting for the response.

19. **How do you create a custom HTTP client with Dio?**
    You can create a custom HTTP client by extending the Dio class and adding custom functionality as needed.

20. **How do you test network calls in Flutter?**
    You can test network calls by using mock HTTP responses with packages like `http_mock_adapter` or `mockito`.

21. **What is the significance of status codes in HTTP?**
    Status codes indicate the result of an HTTP request, helping you understand if the request was successful or if there was an error (e.g., 200 for success, 404 for not found).

22. **How do you handle SSL pinning in Flutter?**
    SSL pinning can be implemented using the `flutter_ssl_pinning` package to validate the server's SSL certificate.

23. **What are WebSockets, and how can they be used in Flutter?**
    WebSockets provide a full-duplex communication channel over a single TCP connection, allowing real-time data transfer in Flutter apps.

24. **How do you use GraphQL in Flutter?**
    You can use the `graphql_flutter` package to interact with GraphQL APIs, enabling queries and mutations.

25. **What is the purpose of using the http package’s Request class?**
    The `Request` class allows you to create more complex HTTP requests, providing more control over the request configuration.

26. **How do you implement caching for API responses?**
    You can implement caching by storing responses in local storage and checking for cached data before making a new request.

27. **What is the json_serializable package, and how is it used?**
    The `json_serializable` package automates JSON serialization and deserialization, simplifying the conversion of model classes.

28. **How can you monitor network activity in Flutter?**
    You can monitor network activity by using logging interceptors in Dio or by integrating tools like Flipper.

29. **What are some best practices for making network requests in Flutter?**
    - Use asynchronous programming.
    - Handle errors gracefully.
    - Implement caching where appropriate.
    - Secure sensitive data.

30. **How do you parse XML data from an API in Flutter?**
    You can use the `xml` package to parse XML data into a manageable format:

    ```dart
    import 'package:xml/xml.dart';

    var document = XmlDocument.parse(response.body);
    ```

31. **How do you authenticate API requests using tokens?**
    You can include tokens in the headers of your requests:

    ```dart
    headers: {'Authorization': 'Bearer your_token'},
    ```

32. **What is the difference between http.get() and http.read()?**
    `http.get()` retrieves the full response including headers, while `http.read()` retrieves only the response body.

33. **How do you refresh tokens in a Flutter app?**
    You can refresh tokens by making a request to a refresh endpoint using the existing refresh token.

34. **How do you implement retry logic for network requests?**
    You can implement retry logic using a loop with a delay or using Dio's retry interceptor.

35. **How can you use async and await for networking calls?**
    Use the `async` keyword in your function signature and the `await` keyword before the network call:

    ```dart
    Future<void> fetchData() async {
      final response = await http.get(Uri.parse('https://api.example.com/data'));
    }
    ```

36. **What is the purpose of the http.Response class?**
    The `http.Response` class represents the response from an HTTP request, including the status code, headers, and body.

37. **How do you use query parameters in a GET request?**
    You can add query parameters using the `Uri` constructor:

    ```dart
    final response = await http.get(Uri.parse('https://api.example.com/data?param=value'));
    ```

38. **How can you handle multipart requests in Flutter?**
    You can handle multipart requests using the `http.MultipartRequest` class, which allows you to send files along with other data.

39. **What is the role of the http.MultipartFile class?**
    The `http.Multipart

File` class is used to represent files in multipart requests, allowing you to upload files to a server.

40. **How do you set default headers for all requests in Dio?**
    You can set default headers in the Dio instance like this:

    ```dart
    Dio dio = Dio(BaseOptions(headers: {'Authorization': 'Bearer token'}));
    ```

41. **How can you convert a response body to a model object?**
    You can decode the JSON response and use a factory constructor to create a model object:

    ```dart
    final data = json.decode(response.body);
    MyModel myModel = MyModel.fromJson(data);
    ```

42. **What are some common security measures when making network requests?**
    - Use HTTPS to encrypt data.
    - Validate SSL certificates.
    - Store sensitive data securely.

43. **How do you handle network connectivity issues in your app?**
    You can use the connectivity package to check for network status and display messages to the user.

44. **What is the role of the http.Client class?**
    The `http.Client` class provides a way to make HTTP requests and manage connections, allowing you to implement custom behavior.

45. **How can you create a REST API client in Flutter?**
    You can create a REST API client by wrapping HTTP calls in a class and providing methods for each endpoint.

46. **What are the limitations of using the http package?**
    The `http` package lacks advanced features like interceptors, cancellation, and custom response handling compared to packages like Dio.

47. **How do you implement OAuth 2.0 in a Flutter app?**
    You can implement OAuth 2.0 by using the authorization code flow, redirecting users to the login page, and exchanging the code for tokens.

48. **What is the retrofit package, and how does it help with networking?**
    Retrofit is a type-safe HTTP client that simplifies API requests by defining methods for API endpoints using annotations.

49. **How can you log HTTP requests and responses for debugging?**
    You can log requests and responses using Dio interceptors or by implementing logging in your API client.

50. **How do you use flutter_bloc with networking for state management?**
    You can use `flutter_bloc` to manage the state of your network requests, handling loading, success, and error states in a structured manner.

## Modern networking patterns (2026)

51. **What is `dio 5.x`, and which problems does it solve that the built-in `http` package doesn't?**
    `dio` is a feature-rich HTTP client. Compared to the SDK `http` package, it adds: interceptors (auth, logging, retry), automatic `FormData` and JSON serialization, request cancellation via `CancelToken`, file upload progress, connection-pool management, and per-request timeout settings. For anything beyond simple GET/POST, reach for `dio`.

    ```dart
    final dio = Dio(BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: 5.seconds,
      receiveTimeout: 10.seconds,
    ));
    ```

52. **How do you set up an authenticated `Dio` client with refresh-token retry logic?**
    Use a `QueuedInterceptor` to add the bearer header, and a second interceptor that catches `401`, refreshes the token, and replays the original request.

    ```dart
    dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (opts, handler) {
          opts.headers['Authorization'] = 'Bearer ${tokenStore.access}';
          handler.next(opts);
        },
        onError: (err, handler) async {
          if (err.response?.statusCode == 401) {
            await tokenStore.refresh();
            final retry = await dio.fetch(err.requestOptions);
            return handler.resolve(retry);
          }
          handler.next(err);
        },
      ),
    );
    ```

    Use a `Mutex` to ensure parallel 401s don't trigger multiple refresh calls.

53. **What is `RetryInterceptor` (and exponential backoff), and when should you reach for it?**
    `package:dio_smart_retry` (or your own interceptor) catches transient failures (network down, 5xx) and re-fires the request after a delay that grows exponentially (`1s, 2s, 4s, ...`). Use it for *safe* operations (GET, idempotent PUTs). **Don't** retry POST without an idempotency-key header — you could double-charge a payment.

54. **How do you cancel an in-flight request when the user navigates away?**
    Pass a `CancelToken` to the request and call `.cancel()` from `dispose`.

    ```dart
    class _SearchPageState extends State<SearchPage> {
      final _cancel = CancelToken();
      Future<void> _search(String q) async {
        final r = await dio.get('/search', queryParameters: {'q': q}, cancelToken: _cancel);
        // ...
      }
      @override
      void dispose() {
        _cancel.cancel('page disposed');
        super.dispose();
      }
    }
    ```

55. **What is the right way to model REST responses with `freezed` + `json_serializable` in 2026?**
    `freezed` generates immutable data classes with `==`, `hashCode`, `copyWith`, sealed-style unions, and a `fromJson` constructor (with `json_serializable` as the JSON layer). It eliminates pages of boilerplate and produces compile-time-exhaustive switch matches.

    ```dart
    @freezed
    class User with _$User {
      const factory User({
        required String id,
        required String name,
        String? avatarUrl,
      }) = _User;
      factory User.fromJson(Map<String, Object?> j) => _$UserFromJson(j);
    }
    ```

    Combined with `dio`'s `Response<Map>` and a small mapper, you get type-safe responses with zero hand-written boilerplate.

56. **How does `Dio`'s `transformer` differ from an interceptor, and when do you customize each?**
    - **Interceptor** — pre/post-process the request lifecycle (auth, logging, retry, error mapping).
    - **Transformer** — convert between the wire format and Dart objects (custom JSON decoder, msgpack, protobuf).
    Use a transformer when you replace the *serialization*, an interceptor when you customize *behavior*.

57. **How do you implement file upload with progress reporting on a slow network?**
    `dio.post(..., onSendProgress: ...)` reports byte-level progress; build a `FormData` with the file part.

    ```dart
    final form = FormData.fromMap({
      'file': await MultipartFile.fromFile(path, filename: 'photo.jpg'),
      'caption': 'Sunset',
    });
    final resp = await dio.post('/uploads', data: form,
      onSendProgress: (sent, total) => emit(UploadProgress(sent / total)));
    ```

    For very large files, prefer chunked uploads (split client-side, server-side stitch) for restartability.

58. **What is `graphql_flutter` vs `ferry`, and when does a GraphQL client beat a REST + DTO setup?**
    - `graphql_flutter` — easiest entry; widget-based query/mutation API.
    - `ferry` — code-generated, type-safe; pairs with `gql` and `built_value` for compile-time-checked queries.
    GraphQL beats REST when: clients need different field subsets, you want a single endpoint, or you have many backend microservices to aggregate. REST + DTOs win on simple CRUD and on caching infrastructure (CDN-friendly).

59. **How do you write integration tests against a real backend without flaky CI?**
    Use a *contract-tested* mock server such as `wiremock` or `mockoon` that records and replays HTTP cassettes captured against the real backend. Run the cassette in CI; periodically refresh against staging. This gives realistic responses (including error shapes) without depending on network for every CI run.

60. **How do you secure HTTPS traffic against MITM on Android 7+ via Network Security Config?**
    Ship a Network Security Config XML that:
    - Disables `cleartextTrafficPermitted` for production builds.
    - Pins your backend certificates (`<pin-set>`).
    - Restricts trust to the system CA store (no user-installed CAs).

    ```xml
    <!-- android/app/src/main/res/xml/network_security_config.xml -->
    <network-security-config>
      <domain-config cleartextTrafficPermitted="false">
        <domain includeSubdomains="true">api.example.com</domain>
        <pin-set>
          <pin digest="SHA-256">AAAA...=</pin>
          <pin digest="SHA-256">BBBB...=</pin>
        </pin-set>
      </domain-config>
    </network-security-config>
    ```

    Reference it in `AndroidManifest.xml` and rotate pins regularly. Apply equivalent App Transport Security rules in `Info.plist` on iOS.
