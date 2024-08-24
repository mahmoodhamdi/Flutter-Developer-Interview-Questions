# Flutter Widgets: Answers

1. **What is a widget in Flutter?**
   A widget in Flutter is a basic building block of the user interface. Everything visible in a Flutter app is a widget, from buttons and text to layouts and animations.

2. **Explain the difference between a StatelessWidget and a StatefulWidget.**
   A StatelessWidget is immutable and cannot change its state during the lifetime of the widget. A StatefulWidget can maintain state that might change during the widget's lifetime, requiring the widget to be redrawn.

3. **How do you create a custom widget in Flutter?**
   To create a custom widget, you can extend either StatelessWidget or StatefulWidget and override the build method to define the widget's UI.

4. **What is the Container widget, and how is it used?**
   Container is a convenience widget that combines common painting, positioning, and sizing widgets. It's often used to style and position its child widget.

5. **How do you create a list of widgets in Flutter?**
   You can create a list of widgets using ListView, Column, or Row widgets, depending on your layout needs. For long lists, ListView.builder is more efficient.

6. **What is the purpose of the Text widget?**
   The Text widget is used to display a string of text with a single style. It can be customized with various properties like style, textAlign, and overflow.

7. **How do you create a button in Flutter?**
   Buttons can be created using widgets like ElevatedButton, TextButton, or OutlinedButton. Each has different default styles and can be customized.

8. **What is the Column widget, and how is it different from the Row widget?**
   Column arranges its children in a vertical array, while Row arranges them horizontally. Both are used for linear layouts in different directions.

9. **How do you create a form in Flutter using the Form widget?**
   The Form widget is used with FormField widgets (like TextFormField) to create a form. It provides form validation and submission functionality.

10. **What is the ListView widget, and how is it used?**
    ListView is a scrollable list of widgets arranged linearly. It's used to display a scrolling list of repeated elements.

11. **How do you use the Stack widget in Flutter?**
    Stack allows you to overlay widgets on top of each other. Children can be positioned relative to the stack's edges using Positioned widgets.

12. **What is the Expanded widget, and how is it used in layouts?**
    Expanded is used within Row, Column, or Flex to create a flexible child that will expand to fill available space along the main axis.

13. **How do you use the Padding widget in Flutter?**
    Padding is used to add empty space around a widget. It takes a child widget and an EdgeInsets to specify the padding.

14. **What is the GridView widget, and how is it different from ListView?**
    GridView displays children in a 2D array, while ListView is linear. GridView is used for creating scrollable grids of widgets.

15. **How do you use the SizedBox widget in Flutter?**
    SizedBox is used to give a specific width and height to its child, or to create empty space when used without a child.

16. **What is the Align widget, and how is it used?**
    Align is used to align its child within itself and optionally size itself based on the child's size. It's useful for positioning widgets within their parents.

17. **How do you create a scrollable widget in Flutter?**
    Scrollable widgets can be created using SingleChildScrollView for a single child, or ListView/GridView for multiple children.

18. **What is the Flexible widget, and how is it different from Expanded?**
    Flexible allows a child of Row or Column to flex its size. Unlike Expanded, it doesn't force the child to fill all available space.

19. **How do you use the Wrap widget in Flutter?**
    Wrap is used to display its children in multiple horizontal or vertical runs. It's useful when you want to create a layout that automatically wraps to the next line.

20. **What is the Image widget, and how is it used to display images?**
    Image widget is used to display images from various sources (asset, file, network, memory). It has properties to control how the image is displayed and scaled.

21. **How do you create a navigation drawer in Flutter?**
    A navigation drawer is created using the Drawer widget, typically set as the drawer property of a Scaffold.

22. **What is the Drawer widget, and how do you use it?**
    Drawer is a panel that slides in horizontally from the edge of a Scaffold to show navigation links. It's commonly used for app navigation.

23. **How do you implement a tabbed interface in Flutter?**
    Tabbed interfaces are implemented using TabController, TabBar, and TabBarView widgets, often within a DefaultTabController.

24. **What is the TabBar widget, and how is it used?**
    TabBar displays a horizontal row of tabs. It's typically used in conjunction with TabBarView to create a tabbed interface.

25. **How do you create a floating action button in Flutter?**
    A floating action button is created using the FloatingActionButton widget, typically set as the floatingActionButton property of a Scaffold.

26. **What is the FloatingActionButton widget, and how is it different from a regular button?**
    FloatingActionButton is a circular button that floats above the content, typically used for a promoted action. It has a distinct appearance compared to regular buttons.

27. **How do you use the Icon widget in Flutter?**
    The Icon widget is used to display a glyph from a font described in an IconData, such as material design icons.

28. **What is the AppBar widget, and how is it used to create a top app bar?**
    AppBar is used to create a material design app bar, typically placed at the top of the screen. It can include a title, actions, and other widgets.

29. **How do you create a custom app bar in Flutter?**
    A custom app bar can be created by using the AppBar widget and customizing its properties, or by creating a completely custom widget to replace the AppBar.

30. **What is the BottomNavigationBar widget, and how is it used for bottom navigation?**
    BottomNavigationBar is used to display 3-5 navigation destinations at the bottom of an app. It's typically used with Scaffold's bottomNavigationBar property.

31. **How do you create a custom bottom navigation bar in Flutter?**
    A custom bottom navigation bar can be created by using the BottomNavigationBar widget and customizing its appearance, or by creating a completely custom widget.

32. **What is the Card widget, and how is it used to create cards?**
    Card is a material design card that can be used to present related information as a single unit. It has rounded corners and a shadow by default.

33. **How do you create a dialog in Flutter using the AlertDialog widget?**
    AlertDialog is used to create a dialog that interrupts the user with urgent information, details, or actions. It's typically shown using showDialog.

34. **What is the SimpleDialog widget, and how is it different from AlertDialog?**
    SimpleDialog offers the user a choice from a set of options. Unlike AlertDialog, it doesn't have actions at the bottom and is used for simpler selection tasks.

35. **How do you use the SnackBar widget in Flutter?**
    SnackBar is used to show a brief message at the bottom of the screen. It's typically displayed using the ScaffoldMessenger.showSnackBar method.

36. **What is the BottomSheet widget, and how is it used?**
    BottomSheet is a modal interface that slides up from the bottom of the screen. It can be persistent or modal and is used to show additional content or options.

37. **How do you create a dropdown menu in Flutter using the DropdownButton widget?**
    DropdownButton is used to create a dropdown menu. It takes a list of DropdownMenuItem widgets as its items and handles selection.

38. **What is the Checkbox widget, and how is it used in forms?**
    Checkbox is used to toggle the state of a single option. It's often used in forms or settings to enable or disable options.

39. **How do you use the Radio widget in Flutter?**
    Radio is used to select one option from a set of mutually exclusive options. It's typically used in a group with other Radio widgets.

40. **What is the Slider widget, and how is it used for range selection?**
    Slider is used to select a value from a continuous or discrete set of values. It's useful for adjusting settings like volume or brightness.

41. **How do you use the Switch widget in Flutter?**
    Switch is used to toggle the on/off state of a single setting. It's often used in settings or configuration screens.

42. **What is the ListTile widget, and how is it used to create list items?**
    ListTile is a convenient widget for creating items in a list. It can contain leading and trailing icons, as well as up to 3 lines of text.

43. **How do you create a progress indicator in Flutter using the CircularProgressIndicator widget?**
    CircularProgressIndicator shows progress as a circular animation. It's used to indicate that an operation is in progress.

44. **What is the LinearProgressIndicator widget, and how is it different from CircularProgressIndicator?**
    LinearProgressIndicator shows progress as a horizontal line. Unlike CircularProgressIndicator, it's linear and typically used for operations with a known duration.

45. **How do you use the Tooltip widget in Flutter?**
    Tooltip is used to provide additional information when a widget is long-pressed. It displays a short message in a popup.

46. **What is the GestureDetector widget, and how is it used to detect gestures?**
    GestureDetector is used to detect various user gestures like taps, drags, and scales. It wraps another widget and provides callbacks for different gestures.

47. **How do you create a custom icon button in Flutter?**
    A custom icon button can be created by combining an Icon widget with a button widget like IconButton, or by creating a completely custom widget.

48. **What is the Divider widget, and how is it used to separate content?**
    Divider is used to create a thin horizontal line, often used to separate content in lists or layouts.

49. **How do you use the ListView.builder widget to create dynamic lists?**
    ListView.builder is used to create a scrollable, linear array of widgets that are built on demand. It's efficient for long or infinite lists.

50. **What is the DataTable widget, and how is it used to display tabular data?**
    DataTable is used to display rows of information, typically used to present structured data. It includes features like sorting and selection.
