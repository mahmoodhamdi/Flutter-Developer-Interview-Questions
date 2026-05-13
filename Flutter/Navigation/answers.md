# Flutter Navigation: Answers

1. **What is Navigator, and how does it work in Flutter?**  
   The Navigator is a widget that manages a stack of Route objects. It provides methods for navigating between these routes, such as pushing a new route onto the stack or popping the current route off.

2. **How do you push a new route in Flutter?**  
   You can push a new route using the `Navigator.push` method, like this:  

   ```dart
   Navigator.push(context, MaterialPageRoute(builder: (context) => NewScreen()));
   ```

3. **What is the MaterialPageRoute, and how is it used?**  
   `MaterialPageRoute` is a route that uses a material design transition when navigating. It is commonly used with the Navigator to create a route that slides in from the right.

4. **How do you use named routes in Flutter?**  
   Named routes can be defined in the `MaterialApp` widget using the `routes` property. You can then navigate using `Navigator.pushNamed(context, '/routeName');`.

5. **What is Navigator.pop, and when would you use it?**  
   `Navigator.pop` removes the current route from the stack, returning to the previous route. It is typically used when you want to go back to the previous screen.

6. **How do you pass data between routes in Flutter?**  
   You can pass data when pushing a route by including it in the constructor of the new screen, like this:  

   ```dart
   Navigator.push(context, MaterialPageRoute(builder: (context) => NewScreen(data: myData)));
   ```

7. **What is the difference between push and pushReplacement?**  
   `push` adds a new route on top of the current one, while `pushReplacement` removes the current route and replaces it with a new one.

8. **How do you create a custom transition between routes?**  
   To create a custom transition, you can define a class that extends `PageRouteBuilder` and override the `buildTransitions` method.

9. **What is onGenerateRoute, and how does it help with dynamic routing?**  
   `onGenerateRoute` is a callback that provides a way to handle named routes dynamically. It can be used to generate routes based on specific logic or conditions.

10. **How do you intercept the system back button in Flutter, and what is the difference between `WillPopScope` (deprecated) and `PopScope`?**
    `WillPopScope` is deprecated in modern Flutter. The replacement is `PopScope`, which decouples the *decision to pop* from the *side effect after pop*. Two reasons drove the change: (1) Android predictive back gestures require knowing if a pop is allowed *before* the gesture finishes, which the `Future<bool>`-based `onWillPop` could not provide, and (2) `PopScope` works uniformly across iOS swipe-back, Android predictive back, and explicit `Navigator.pop`.

    ```dart
    // Modern (Flutter 3.12+):
    PopScope(
      canPop: !hasUnsavedChanges,
      onPopInvokedWithResult: (didPop, result) async {
        if (didPop) return;
        final shouldLeave = await showDialog<bool>(
          context: context,
          builder: (_) => const _DiscardChangesDialog(),
        );
        if (shouldLeave ?? false) {
          if (context.mounted) Navigator.pop(context);
        }
      },
      child: const _MyForm(),
    );
    ```

    Key points: set `canPop: false` to block the pop, then handle the user's confirmation inside `onPopInvokedWithResult`. Setting `canPop: true` lets the pop proceed and the callback runs as a notification. `onPopInvoked` (without `WithResult`) is the older signature and is being phased out.

11. **What is the Hero widget, and how is it used in navigation?**  
    The Hero widget is used to create a smooth transition between two screens. It animates the widget with the same `tag` value from one screen to another.

12. **How do you navigate to a new screen without the back button?**  
    You can use `pushAndRemoveUntil` to navigate to a new screen and remove all previous routes from the stack, effectively preventing the back navigation.

13. **What is pushNamed, and how does it differ from push?**  
    `pushNamed` is used for navigating to a route by its name, while `push` requires a `Route` object. `pushNamed` simplifies navigation for routes defined in the `MaterialApp`.

14. **How do you implement nested navigation in Flutter?**  
    Nested navigation can be implemented by using multiple `Navigator` widgets. Each `Navigator` can manage its own stack of routes independently.

15. **What is pushAndRemoveUntil, and how does it work?**  
    `pushAndRemoveUntil` pushes a new route and removes all previous routes until the specified condition is met, allowing for complex navigation flows.

16. **How do you use RouteObserver to listen to route changes?**  
    `RouteObserver` is used to subscribe to navigation changes. You can create a `RouteObserver` instance and provide it to the `Navigator` to listen for changes in the route stack.

17. **What is NavigatorState, and how is it used?**  
    `NavigatorState` represents the state of a Navigator widget. It is used to perform operations such as pushing or popping routes programmatically.

18. **How do you create a bottom navigation bar with BottomNavigationBar?**  
    You can use the `BottomNavigationBar` widget in conjunction with a `StatefulWidget` to manage the selected index and update the displayed screen accordingly.

19. **What is modalBottomSheet, and how is it used for navigation?**  
    A `modalBottomSheet` is a sliding panel that appears from the bottom of the screen. It can be used for navigation by providing additional options or actions related to the current context.

20. **How do you implement drawer-based navigation in Flutter?**  
    You can use the `Drawer` widget within a `Scaffold` to provide a side navigation menu. It allows users to navigate between different screens.

21. **What is pushReplacementNamed, and how does it differ from pushNamed?**  
    `pushReplacementNamed` navigates to a new named route while removing the current route from the stack, while `pushNamed` simply adds a new route.

22. **How do you use Navigator.of(context).push with a custom PageRoute?**  
    You can define a custom `PageRoute` and use `Navigator.of(context).push` to navigate to it, allowing for custom transitions and behaviors.

23. **What is TransitionBuilder, and how does it enhance navigation?**  
    `TransitionBuilder` allows you to define custom animations and transitions when navigating between routes, enhancing the visual experience.

24. **How do you manage state between multiple navigation stacks?**  
    You can use state management solutions like Provider or Bloc to maintain state across different navigation stacks.

25. **What is IndexedStack, and how does it relate to navigation?**  
    `IndexedStack` allows you to manage multiple children but only displays one at a time. It is useful for tab-based navigation where you want to preserve the state of each tab.

26. **How do you implement deep linking in Flutter?**  
    Deep linking can be implemented using the `uni_links` package or by configuring your app's routing to handle incoming URLs.

27. **What is NavigatorObserver, and how is it used?**  
    `NavigatorObserver` allows you to listen to route changes and can be used to log navigation events or implement analytics.

28. **How do you use PageView for swipeable navigation?**  
    `PageView` allows users to swipe between different pages. You can create a horizontal or vertical scrollable view of pages.

29. **What is CustomScrollView, and how does it integrate with navigation?**  
    `CustomScrollView` allows you to create complex scrollable layouts, and it can integrate with navigation by using slivers to manage different scrollable areas.

30. **How do you use Offstage to manage navigation without rebuilding widgets?**  
    `Offstage` allows you to keep widgets in the widget tree but not display them. It can be useful for managing navigation without losing the state of a widget.

31. **What is fadeInTransition, and how is it implemented?**  
    `fadeInTransition` is a custom transition that gradually fades in a new route. It can be implemented by overriding the `buildTransitions` method in a custom `PageRoute`.

32. **How do you manage navigation in a Flutter Web app?**  
    Flutter Web apps can manage navigation using named routes and the browser's history API, allowing users to navigate using the back and forward buttons.

33. **What is SafeArea, and how does it relate to navigation?**  
    `SafeArea` ensures that content is displayed within the safe boundaries of a device, preventing overlaps with system UI elements like notches and status bars.

34. **How do you implement a tab-based navigation system?**  
    You can implement a tab-based navigation system using `TabBar` and `TabBarView`, managing the active tab's index to switch between views.

35. **What is AnimatedSwitcher, and how does it enhance navigation?**  
    `AnimatedSwitcher` is used to animate widget transitions when switching between different widgets. It can enhance navigation by providing visual feedback.

36. **How do you handle navigation for different screen sizes and orientations?**  
    You can use media queries to adapt the layout and navigation based on the device's screen size and orientation, ensuring a responsive design.

37. **What is FutureBuilder, and how is it used in async navigation?**  
    `FutureBuilder` is used to build widgets based on the state of a `Future`. It can be useful for loading data before navigating to a new screen.

38. **How do you implement routing guards in Flutter?**  
    Routing guards can be implemented by using `onGenerateRoute` to check conditions before allowing navigation to a particular route.

39. **What is the Navigator key, and how is it used for global navigation?**  
    The Navigator key allows you to access the Navigator state globally, enabling navigation from anywhere in the app without needing the context.

40. **How do you manage nested navigation within a TabBar?**  
    You can use multiple `Navigator` widgets, each managing its own stack of routes, and nest them within the `TabBar`'s tabs.

41. **What is SlideTransition, and how is it used in navigation?**  
    `SlideTransition` animates the movement of a widget in or out of view, and can be used to create custom transitions between routes.

42. **How do you implement a navigation drawer with multiple levels?**  
    You can create a `Drawer` widget with nested `List

View` or `ExpansionTile` widgets to manage multiple levels of navigation.

43. **What is RouteSettings, and how does it help with navigation?**  
    `RouteSettings` holds information about a route, such as its name and arguments. It can be used for analytics or conditional navigation.

44. **How do you use CustomPageRoute to create custom page transitions?**  
    You can extend `PageRouteBuilder` to create a `CustomPageRoute`, overriding the transition methods to define custom animations.

45. **What is pushReplacementUntil, and how does it differ from pushAndRemoveUntil?**  
    `pushReplacementUntil` replaces the current route and pushes a new one until a condition is met, while `pushAndRemoveUntil` removes routes until a condition is met before pushing.

46. **How do you handle navigation with Bloc or Provider?**  
    You can integrate navigation with state management solutions like Bloc or Provider by listening for changes in state and navigating accordingly.

47. **What is get_it, and how is it used in navigation?**  
    `get_it` is a service locator for managing dependencies. It can be used to provide navigation-related services globally in your app.

48. **How do you manage navigation state in a Flutter app?**  
    Navigation state can be managed using a combination of `Navigator`, `RouteObserver`, and state management libraries to keep track of the current route and its data.

49. **What is routeAnimation, and how is it implemented?**  
    `routeAnimation` refers to the visual effects that occur during navigation. It can be implemented by customizing `PageRoute` transitions.

50. **How do you test navigation flows in a Flutter app?**
    You can test navigation flows by using integration tests or widget tests that simulate user interactions and verify the resulting routes.

## go_router 14.x — declarative navigation (2026)

51. **What is `go_router`, and why has it become the de facto routing solution for Flutter?**
    `go_router` is a declarative URL-based router that sits on top of Flutter's Navigator 2.0 RouterDelegate. It solves three problems that hand-rolled Navigator 2.0 code suffers from: (1) verbose `RouteInformationParser` and `RouterDelegate` boilerplate, (2) ad-hoc deep-link parsing, and (3) inconsistent web URL synchronization. It's officially endorsed by the Flutter team and is the basis of `package:flutter/router.dart` examples.

    ```dart
    final router = GoRouter(
      initialLocation: '/',
      routes: [
        GoRoute(path: '/', builder: (_, __) => const HomePage()),
        GoRoute(
          path: '/posts/:id',
          builder: (_, state) => PostPage(id: state.pathParameters['id']!),
        ),
      ],
    );

    MaterialApp.router(routerConfig: router);
    ```

52. **How do you define routes with `GoRouter` and `GoRoute`?**
    `GoRoute` declares a path pattern plus a builder. Paths use `:param` for path parameters and read query parameters via `state.uri.queryParameters`. Sub-routes nest via `routes:`.

    ```dart
    GoRoute(
      path: '/users/:userId',
      builder: (context, state) => UserPage(state.pathParameters['userId']!),
      routes: [
        GoRoute(
          path: 'posts/:postId',          // → /users/:userId/posts/:postId
          builder: (c, s) => PostPage(
            userId: s.pathParameters['userId']!,
            postId: s.pathParameters['postId']!,
          ),
        ),
      ],
    );
    ```

53. **How do nested routes work in `go_router` (e.g. tab shell with stacked pages per tab)?**
    Use `StatefulShellRoute.indexedStack` to host independent navigation stacks per tab — each tab keeps its own back history while the bottom navigation stays visible.

    ```dart
    StatefulShellRoute.indexedStack(
      builder: (context, state, navigationShell) =>
        ScaffoldWithNavBar(navigationShell: navigationShell),
      branches: [
        StatefulShellBranch(routes: [
          GoRoute(path: '/home', builder: (_, __) => const HomeTab()),
        ]),
        StatefulShellBranch(routes: [
          GoRoute(path: '/search', builder: (_, __) => const SearchTab()),
        ]),
        StatefulShellBranch(routes: [
          GoRoute(path: '/profile', builder: (_, __) => const ProfileTab()),
        ]),
      ],
    );
    ```

54. **How do you implement type-safe navigation with `go_router_builder`?**
    `go_router_builder` generates strongly typed `*Route` classes from annotated route declarations so you call `PostRoute(id: '42').go(context)` instead of stringly-typed `context.go('/posts/42')`. Path-parameter types are enforced at compile time.

    ```dart
    @TypedGoRoute<PostRoute>(path: '/posts/:id')
    class PostRoute extends GoRouteData {
      const PostRoute({required this.id});
      final String id;
      @override
      Widget build(BuildContext context, GoRouterState state) => PostPage(id: id);
    }

    // Usage:
    PostRoute(id: '42').go(context);
    ```

55. **How does `go_router` handle deep links and the system back stack on Android predictive back?**
    Each incoming intent (custom URL scheme, App Links, Universal Links) is parsed as a URL string and matched against the route tree — the matched stack becomes the back stack. Combined with `PopScope(canPop: ..., onPopInvokedWithResult: ...)` on screens that need to block back, predictive back gestures animate correctly because `go_router` reports `canPop()` to the framework synchronously.

56. **How do you guard routes with redirects (auth, onboarding gating)?**
    Provide a `redirect` callback on `GoRouter` or on a specific `GoRoute`. Return the path to redirect to, or `null` to allow the navigation. Listen to auth state via `refreshListenable` so the router re-evaluates when login status changes.

    ```dart
    GoRouter(
      refreshListenable: GoRouterRefreshStream(authStateChanges),
      redirect: (context, state) {
        final loggedIn = ref.read(authProvider).isLoggedIn;
        final goingToLogin = state.matchedLocation == '/login';
        if (!loggedIn && !goingToLogin) return '/login';
        if (loggedIn && goingToLogin) return '/';
        return null;
      },
      routes: [...],
    );
    ```

57. **What is `ShellRoute` / `StatefulShellRoute.indexedStack`, and when do you use each?**
    - `ShellRoute` — a single, shared `Scaffold`-like shell wrapping its child routes. Use when you have one piece of chrome (e.g. an app bar with a logo) shared across pages but no need for per-tab back stacks.
    - `StatefulShellRoute.indexedStack` — multiple parallel navigation stacks (one per branch). Use for bottom navigation, persistent tabs, or master-detail layouts where each tab/pane must remember its own back history.

58. **How do you pass complex objects between routes (path params vs query params vs extra)?**
    - **Path parameters** (`/post/:id`) — small primitive identifiers; visible in the URL; deep-linkable.
    - **Query parameters** (`?ref=feed`) — optional metadata; URL-visible.
    - **`extra`** (`context.go('/checkout', extra: cart)`) — arbitrary Dart object. *Not* serialized into the URL, so not deep-linkable. Use only for transient state where the receiving screen can fall back to fetching by ID if `extra` is null (cold start, restoration).

59. **How do you display modal sheets and dialogs as routes so deep links and back behave correctly?**
    Use `pageBuilder` with a custom `Page<T>` — `ModalBottomSheetRoute` or `DialogRoute` wrapped as a Page. This makes the modal appear in the route stack, so back pops it and deep links can open it directly.

    ```dart
    GoRoute(
      path: '/post/:id/share',
      pageBuilder: (context, state) => ModalBottomSheetPage(
        child: SharePostSheet(id: state.pathParameters['id']!),
      ),
    );
    ```

60. **How do you test a `go_router` tree without booting the full app?**
    Construct the router in your test with the routes under test and pump it inside a `MaterialApp.router`. Use `goRouter.go('/path')` to navigate and `find.byType` to assert the right page rendered. Mock auth / data providers via `ProviderScope` overrides if needed.

    ```dart
    testWidgets('redirects to /login when logged out', (tester) async {
      final router = buildTestRouter(loggedIn: false);
      await tester.pumpWidget(MaterialApp.router(routerConfig: router));
      router.go('/profile');
      await tester.pumpAndSettle();
      expect(find.byType(LoginPage), findsOneWidget);
    });
    ```
