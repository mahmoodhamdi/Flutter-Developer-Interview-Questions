# Flutter Basics: Answers

1. **What is Flutter?**
   Flutter is an open-source UI software development kit created by Google. It allows developers to build natively compiled applications for mobile, web, and desktop from a single codebase.

2. **Explain the difference between Flutter and other mobile app development frameworks.**
   Flutter differs from other frameworks in several ways:
   - It uses a single codebase for multiple platforms (iOS, Android, web, desktop).
   - It has a rich set of customizable widgets for building UIs.
   - It uses Dart as its programming language, which is optimized for UI development.
   - It offers hot reload for faster development cycles.
   - It provides native performance through direct compilation to native ARM code.

3. **How do you create a basic Flutter application?**
   To create a basic Flutter application:
   1. Install Flutter SDK and set up your development environment.
   2. Run `flutter create my_app` in your terminal.
   3. Navigate to the project directory: `cd my_app`.
   4. Open the `lib/main.dart` file and modify it as needed.
   5. Run the app using `flutter run`

4. **What is the purpose of the MaterialApp widget?**
   The MaterialApp widget is the starting point for your app, and it builds upon the WidgetsApp widget by adding material-specific functionality. It sets up the top-level Navigator, which manages a stack of widgets identified by strings, also known as "routes". It also sets up the theme, title, home route, and more.

5. **How do you run a Flutter application in different environments (development, staging, production)?**
   You can use flavor configurations to run your app in different environments:
   1. Define different `main` functions for each environment.
   2. Use command-line arguments or build configurations to specify the environment.
   3. Use conditional compilation with const booleans.
   4. Utilize package configs for environment-specific settings.

6. **What is the Scaffold widget, and why is it commonly used?**
   The Scaffold widget implements the basic material design visual layout structure. It provides a default app bar, title, and a body property that holds the main content of the application. It's commonly used because it provides a consistent visual structure that follows material design guidelines.

7. **How do you create a custom theme in Flutter?**
   To create a custom theme:
   1. Create a ThemeData object with your desired colors, fonts, etc.
   2. Pass this ThemeData to the `theme` property of your MaterialApp widget.
   3. Use `Theme.of(context)` to access the theme in your widgets.

8. **Explain the lifecycle of a Flutter widget.**
   The lifecycle of a StatefulWidget includes:
   1. createState()
   2. initState()
   3. didChangeDependencies()
   4. build()
   5. didUpdateWidget()
   6. setState()
   7. deactivate()
   8. dispose()

9. **What is a StatefulWidget? How does it differ from a StatelessWidget?**
   A StatefulWidget can maintain state that might change during the lifetime of the widget. It creates a State object that holds this mutable state. A StatelessWidget, on the other hand, is immutable and its properties can't change once the widget is built.

10. **How do you manage state in a StatefulWidget?**
    State is managed in a StatefulWidget by calling setState() method. This tells the framework that the state has changed and it should rebuild the widget.

11. **What is hot reload, and how does it work in Flutter?**
    Hot reload allows you to inject updated source code files into the running Dart VM. It updates the UI almost instantly without losing the current state of the app. It works by rerunning the build() method of all widgets.

12. **How do you handle navigation between screens in Flutter?**
    Navigation in Flutter is typically handled using the Navigator widget. You can use methods like `Navigator.push()` to navigate to a new screen and `Navigator.pop()` to return to the previous screen.

13. **What is the BuildContext, and how is it used?**
    BuildContext is a handle to the location of a widget in the widget tree. It's used for obtaining theme, media query, Navigator, and other information from the widget tree.

14. **How do you handle user input in Flutter?**
    User input can be handled using various widgets like TextField, TextFormField, GestureDetector, and InkWell. You can also use callbacks like onPressed, onChanged, etc., to respond to user actions.

15. **What are Flutter widgets, and how do they work?**
    Widgets are the basic building blocks of Flutter UI. Everything in Flutter is a widget. Widgets describe what their view should look like given their current configuration and state.

16. **What is the purpose of the setState method?**
    The setState method is used to notify the framework that the internal state of an object has changed. This prompts the framework to schedule a build for this State object.

17. **How do you implement gesture detection in Flutter?**
    Gesture detection can be implemented using the GestureDetector widget. It can recognize taps, drags, and other gestures.

18. **What is the difference between Container and SizedBox?**
    Container is a convenience widget that combines common painting, positioning, and sizing widgets. SizedBox is simpler and is used to give a specific width and height to its child or to create empty space.

19. **How do you manage assets in Flutter?**
    Assets are managed by declaring them in the pubspec.yaml file under the assets section. They can then be accessed in the code using the AssetBundle.

20. **Explain how you can use the flutter doctor command.**
    The `flutter doctor` command checks your environment and displays a report of the status of your Flutter installation. It tells you if there are any dependencies you need to install or further steps you need to take to complete the setup.

21. **What is a FutureBuilder, and how is it used?**
    FutureBuilder is a widget that builds itself based on the latest snapshot of interaction with a Future. It's used to handle asynchronous operations and update the UI based on the state of the Future.

22. **How do you display a list of items in Flutter?**
    Lists can be displayed using widgets like ListView, GridView, or CustomScrollView. These widgets can build their children on demand, which is useful for displaying large or infinite lists.

23. **What is a StreamBuilder, and when would you use it?**
    StreamBuilder is similar to FutureBuilder, but it works with Streams instead of Futures. It's used when you need to build a widget based on the latest value from a stream of data.

24. **How do you create a custom widget in Flutter?**
    To create a custom widget, you can extend either StatelessWidget or StatefulWidget and override the build method to define the widget's UI.

25. **What are the different ways to style text in Flutter?**
    Text can be styled using the style property of the Text widget. You can use TextStyle to set font, size, color, weight, etc. You can also use RichText for more complex text styling.

26. **How do you create a grid layout in Flutter?**
    Grid layouts can be created using the GridView widget. You can use GridView.builder() for dynamic grids or GridView.count() for fixed-count grids.

27. **What is a GlobalKey, and how is it used?**
    GlobalKey is a key that is unique across the entire app. It's used to identify widgets, elements, or state objects across the widget tree, regardless of their position in the tree.

28. **Explain the concept of "widgets as first-class citizens" in Flutter.**
    In Flutter, everything is a widget. This means that core UI elements, layout models, and even application logic are all expressed as widgets. This approach provides consistency and flexibility in building UIs.

29. **How do you add padding and margin to a widget?**
    Padding can be added using the Padding widget. Margin can be added by wrapping a widget with a Container and using its margin property.

30. **What is the SafeArea widget, and when would you use it?**
    SafeArea is a widget that insets its child by sufficient padding to avoid intrusions by the operating system. It's used to prevent UI elements from being obscured by notches, status bars, etc.

31. **How do you implement a responsive layout in Flutter?**
    Responsive layouts can be implemented using widgets like LayoutBuilder, MediaQuery, and Flex widgets (Row, Column). You can also use packages like flutter_screenutil for more advanced responsiveness.

32. **What is the InheritedWidget, and how is it used?**
    InheritedWidget is a base class for widgets that efficiently propagate information down the tree. It's used for passing data down the widget tree without having to pass it explicitly through constructors.

33. **How do you create animations in Flutter?**
    Animations in Flutter can be created using the animation framework. This includes using AnimationController, Tween, and animated widgets like AnimatedBuilder or AnimatedWidget.

34. **Explain how the Navigator works in Flutter.**
    The Navigator manages a stack of Route objects. It provides methods to add (push) and remove (pop) routes from the stack, which corresponds to navigating between screens in the app.

35. **What is the Hero widget, and how do you use it?**
    The Hero widget is used to create animations between routes. It creates a visual connection between two widgets on different screens, making it appear as if one widget "flies" between screens.

36. **How do you use the AnimatedBuilder widget?**
    AnimatedBuilder is a widget that builds itself based on an animation. It's used to rebuild a specific part of the widget tree when an animation changes, improving performance by not rebuilding the entire tree.

37. **What is the difference between mainAxisAlignment and crossAxisAlignment?**
    mainAxisAlignment determines how children are aligned along the main axis of a Row or Column. crossAxisAlignment determines how children are aligned along the cross axis. The main axis of a Row is horizontal, while for a Column it's vertical.

38. **How do you create a drawer in Flutter?**
    A drawer can be created by using the drawer property of the Scaffold widget. The drawer is typically a Material widget that slides in horizontally from the edge of a Scaffold to show navigation links in an application.

39. **What are the best practices for organizing a Flutter project?**
    Best practices include:
    - Separating business logic from UI
    - Using feature-based folder structure
    - Following consistent naming conventions
    - Using packages for reusable code
    - Keeping widgets small and focused

40. **How do you handle errors in Flutter?**
    Errors can be handled using try-catch blocks for synchronous code and .catchError() for asynchronous code. You can also use ErrorWidget.builder to customize error display in the UI.

41. **Explain the concept of "everything is a widget" in Flutter.**
    In Flutter, all UI elements are widgets. This includes not just visible elements, but also layout models (like padding), gestures, animations, and themes. This consistent approach simplifies UI development and makes the framework more intuitive.

42. **How do you use the MediaQuery class?**
    MediaQuery.of(context) is used to get information about the current app's screen, such as size, orientation, and text scale factor. It's useful for creating responsive layouts.

43. **What is the purpose of the Expanded widget?**
    The Expanded widget is used to expand a child of a Row, Column, or Flex so that it fills the available space along the main axis. It's useful for creating flexible layouts.

44. **How do you create a form in Flutter?**
    Forms in Flutter are typically created using the Form widget along with FormField widgets like TextFormField. The Form widget provides form validation and saving functionality.

45. **What is the Flutter Inspector, and how do you use it?**
    The Flutter Inspector is a tool that helps visualize and explore Flutter widget trees. It's useful for understanding layouts, diagnosing UI issues, and inspecting property values. It's available in IDEs that support Flutter development.

46. **How do you optimize the performance of a Flutter application?**
    Performance can be optimized by:
    - Using const constructors where possible
    - Implementing efficient list views (e.g., ListView.builder)
    - Minimizing rebuilds with setState
    - Using production builds for performance testing
    - Profiling the app to identify bottlenecks

47. **Explain the use of keys in Flutter.**
    Keys in Flutter are used to preserve state when widgets move around in the widget tree. They help Flutter identify which widgets to reuse when updating the UI.

48. **What is the LayoutBuilder widget?**
    LayoutBuilder is a widget that builds a widget tree based on the parent widget's constraints. It's useful for creating responsive layouts that adapt to different screen sizes.

49. **How do you create a splash screen in Flutter?**
    A splash screen can be created by:
    1. Defining a splash screen widget
    2. Using Flutter's native splash screen feature (for native splash screens)
    3. Navigating to the main screen after a delay or when initialization is complete

50. **What is the FittedBox widget, and when would you use it?**
    The FittedBox widget sizes and positions its child within itself according to fit. It's useful when you want to scale and align a widget (or widgets) to fit the parent. You might use it when you have content that's too large for its container and you want to scale it down, or when you have content that's too small and you want to scale it up to fill the available space.

## Flutter 3.27 fundamentals (2026)

51. **What's new in Flutter 3.27 that an interviewer in 2026 expects you to know about?**
    The headline items at a 2026 interview:
    - **Impeller is the default on Android** (with Vulkan) and remains default on iOS.
    - **Material 3** is the default since 3.16.
    - **`WidgetState`** (replaces `MaterialState`) since 3.19.
    - **Wasm web build** is stable (`flutter build web --wasm`).
    - **Class modifiers** and **records/patterns** (Dart 3.x) are the default Dart toolset.
    - **`PopScope`** has replaced `WillPopScope` for back navigation.
    - **`TextScaler`** has replaced `textScaleFactor`.
    Bring up two or three of these to show currency.

52. **How has hot reload evolved, and what is the new "Detach" workflow in Flutter 3.20+?**
    Hot reload still reloads modified Dart on a running VM in <1 second, preserving state. The new addition: `flutter attach --detach` lets you detach the IDE/CLI from a running app and reattach later without rebuilding. Combined with `--ddserver` you can inspect a release-mode profile build remotely. Hot **restart** (full app restart with new code, losing state) is still the fallback when reloading is unsafe (e.g. constructor changes, top-level state).

53. **What is the Flutter SDK's `--flavor` flag, and how does it differ from build modes?**
    A **flavor** selects an Android product flavor / iOS scheme — typically `dev`, `staging`, `prod` — each with different bundle IDs, Firebase configs, icons, base URLs. A **build mode** (`debug`, `profile`, `release`) selects compilation options. The two are orthogonal: you can build `flutter run --flavor staging --profile` to performance-test against staging APIs.

54. **What is `flutter_lints` 4.x, and which rules does it enforce that the default doesn't?**
    `flutter_lints` is the official lint package added to every new Flutter project. v4 (Flutter 3.16+) tightened several rules: `prefer_const_constructors`, `avoid_print`, `no_logic_in_create_state`, `use_key_in_widget_constructors`. Add stricter linting via `very_good_analysis` for production codebases.

55. **How do you integrate AI features (Gemini, Claude) into a Flutter app safely?**
    Three patterns:
    1. **Direct client-side API calls** — fastest to prototype, but **leaks your API key** in the shipped binary. Avoid for production.
    2. **Proxy via your backend** — your server holds the API key, the client calls your server, your server calls the model. Add per-user rate limits and a billing cap.
    3. **Vertex AI / Firebase AI Logic** — Google's managed proxy with built-in App Check; no backend required, no key in client. Use `google_generative_ai` package for streaming response handling.

    ```dart
    final model = GenerativeModel(model: 'gemini-1.5-flash', apiKey: backendIssuedToken);
    final response = await model.generateContent([Content.text(prompt)]);
    ```

    Always: enable Firebase App Check, never embed user PII in prompts without consent, and treat model output as untrusted text (sanitize before rendering as HTML/markdown).

56. **What is the official Flutter team's recommendation on Material 2 vs Material 3 in 2026?**
    Use Material 3. M2 is in maintenance — no new features. Existing apps can opt out (`useMaterial3: false`) during migration but should plan to flip the flag. New apps should ship M3 from day one.

57. **How does the new `flutter create --platforms` flag give you control over generated platforms?**
    `flutter create --platforms=ios,android my_app` generates only those platform folders, keeping the project lean. Add a platform later with `flutter create --platforms=web .` from inside the project. Helps reduce build complexity for teams that don't target all platforms.

58. **What is the `--release` vs `--profile` vs `--debug` build mode trade-off?**
    - **Debug** — assertions on, hot reload available, no AOT compilation. Slowest at runtime; never measure performance in this mode.
    - **Profile** — AOT compiled, profiling extension API enabled, assertions off. Use for performance work and shipping to internal testers.
    - **Release** — AOT compiled, fully optimized, no profiling extension. Ship to stores in this mode.

    Web has only debug and release; profile maps to release with profiling.

59. **How do you ship a single Flutter codebase to phone, foldable, tablet, web, and desktop?**
    Three layers:
    1. **Layout** — `LayoutBuilder` + `MediaQuery` + `flutter_adaptive_scaffold` for screen-size-aware UIs (rail vs nav-bar, master-detail vs stack).
    2. **Interaction** — `mouse_region`, hover effects, keyboard shortcuts via `Shortcuts` + `Actions`, right-click menus.
    3. **Platform** — `Platform.isAndroid` / `defaultTargetPlatform` checks only where the platform contract differs (file pickers, deep links, system back).

60. **What is the Flutter team's guidance on Riverpod vs BLoC vs Provider in 2026?**
    The team itself remains *neutral on state management*. Reality on the ground:
    - **Provider** — still the simplest entry, good for small apps or teams new to Flutter.
    - **Riverpod 2.x** — fastest-growing, code-generation friendly, strong type safety, dominant for new greenfield projects.
    - **BLoC 9.x** — strong choice for teams that already know the pattern from Angular/React-Redux backgrounds; great for complex event-driven flows.
    Pick by team familiarity and app complexity, not by hype. The interview answer is "I'd ask about the team's existing stack first, then recommend based on app complexity."