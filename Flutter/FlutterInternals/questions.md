# Flutter Internals: Questions

1. Explain the Flutter rendering process.
2. What is the role of the RenderObject in Flutter?
3. How does Flutter handle layouts?
4. Explain the concept of "widgets as first-class citizens" in Flutter.
5. What is the Element tree in Flutter?
6. How does the BuildContext relate to the widget tree?
7. What is the purpose of the State object in Flutter?
8. How does Flutter manage the widget lifecycle?
9. What is the difference between a StatefulWidget and a StatelessWidget?
10. How does Flutter perform hot reload?
11. What is the RenderBox class in Flutter?
12. How does Flutter handle gestures?
13. What is the Layer tree in Flutter?
14. How does Flutter render animations?
15. Explain the concept of "composition over inheritance" in Flutter.
16. How does Flutter achieve high performance on both iOS and Android?
17. What is the WidgetsBinding class in Flutter?
18. How does Flutter handle asynchronous events?
19. Explain the InheritedWidget and how it works.
20. How does Flutter manage the state of a widget?
21. What is the Ticker class in Flutter?
22. How does Flutter handle image rendering?
23. What is the SchedulerBinding class in Flutter?
24. How does Flutter manage memory?
25. What is the FlutterEngine, and how does it work?
26. How does Flutter communicate with platform-specific code?
27. What is the PlatformChannel, and how is it used?
28. How does Flutter handle text rendering?
29. What is the Dart VM, and how does it relate to Flutter?
30. How does Flutter manage widget keys?
31. Explain the PointerEvent system in Flutter.
32. How does Flutter handle accessibility?
33. What is the MainAxisAlignment and CrossAxisAlignment in Flutter layouts?
34. How does Flutter manage focus and input?
35. What is the FocusNode, and how is it used?
36. How does Flutter handle platform-specific styling?
37. What is the TextPainter class in Flutter?
38. How does Flutter manage fonts and typography?
39. Explain the RenderPipeline in Flutter.
40. How does Flutter handle internationalization (i18n)?
41. What is the CompositedTransformTarget widget?
42. How does Flutter manage network requests?
43. What is the Semantics tree in Flutter?
44. How does Flutter handle transitions between screens?
45. Explain the GestureBinding in Flutter.
46. How does Flutter handle custom painting?
47. What is the Picture class in Flutter?
48. How does Flutter handle shader effects?
49. How does Flutter integrate with other native modules?
50. What is the ImageStream class in Flutter?

## Impeller rendering & engine internals (2026)

51. What is Impeller, and why did Flutter introduce it as a replacement for Skia?
52. How does Impeller differ from Skia in terms of shader compilation jank?
53. What is the engine's "platform thread" vs "UI thread" vs "raster thread" — and what runs on each?
54. How does the `--enable-impeller` flag work on Android, and what is the rollout status?
55. What is "shader warm-up", and why is it less critical on Impeller than on Skia?
56. How does Impeller render text differently, and what is the role of system font fallback?
57. What is the `TextScaler` API (Flutter 3.16+), and how does it replace `textScaleFactor`?
58. How does the new Flutter image-decoder pipeline avoid blocking the UI thread?
59. What is `RasterCache`, and how do `RepaintBoundary` widgets interact with it under Impeller?
60. How would you diagnose a rendering performance issue using DevTools 2.x and Impeller's tracing output?
