# Flutter Clean Architecture: Answers

## Basic Concepts

### 1. **What is Clean Architecture and why should we use it in Flutter applications?**

Clean Architecture is a software design pattern introduced by Robert C. Martin (Uncle Bob) that separates the application into independent layers, each with distinct responsibilities. The main goal is to create a system that is independent of frameworks, UI, databases, and external agencies.

**Key principles:**
- Independence of frameworks
- Testability
- Independence of UI
- Independence of database
- Independence of any external agency

**Why use it in Flutter:**
- Makes code more maintainable and scalable
- Easier to test each layer independently
- Allows easy switching of state management solutions, databases, or APIs
- Better team collaboration with clear separation of concerns
- Reduces coupling between business logic and UI

```dart
// Example structure:
// lib/
//   features/
//     authentication/
//       data/
//         datasources/
//         models/
//         repositories/
//       domain/
//         entities/
//         repositories/
//         usecases/
//       presentation/
//         bloc/
//         pages/
//         widgets/
```

**When to use:**
- Medium to large applications
- Projects with complex business logic
- Applications requiring high testability
- Long-term maintainable projects
- Projects with multiple developers

---

### 2. **What are the main layers in Clean Architecture and what is the responsibility of each layer?**

Clean Architecture consists of three main layers:

**1. Presentation Layer:**
```dart
// presentation/pages/user_page.dart
class UserPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<UserBloc, UserState>(
      builder: (context, state) {
        if (state is UserLoading) {
          return CircularProgressIndicator();
        } else if (state is UserLoaded) {
          return Text(state.user.name);
        } else if (state is UserError) {
          return Text(state.message);
        }
        return Container();
      },
    );
  }
}

// presentation/bloc/user_bloc.dart
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser getUser;

  UserBloc({required this.getUser}) : super(UserInitial()) {
    on<GetUserEvent>((event, emit) async {
      emit(UserLoading());
      final result = await getUser(event.userId);
      result.fold(
        (failure) => emit(UserError(failure.message)),
        (user) => emit(UserLoaded(user)),
      );
    });
  }
}
```

**Responsibilities:**
- UI components (Widgets)
- State management (BLoC, GetX, Riverpod)
- User input handling
- Displaying data from domain layer

**2. Domain Layer:**
```dart
// domain/entities/user.dart
class User {
  final String id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });
}

// domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
  Future<Either<Failure, List<User>>> getUsers();
}

// domain/usecases/get_user.dart
class GetUser {
  final UserRepository repository;

  GetUser(this.repository);

  Future<Either<Failure, User>> call(String id) {
    return repository.getUser(id);
  }
}
```

**Responsibilities:**
- Business logic
- Entities (core business objects)
- Use Cases (business operations)
- Repository interfaces
- No dependencies on outer layers

**3. Data Layer:**
```dart
// data/models/user_model.dart
class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}

// data/datasources/user_remote_data_source.dart
abstract class UserRemoteDataSource {
  Future<UserModel> getUser(String id);
}

class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final Dio dio;

  UserRemoteDataSourceImpl(this.dio);

  @override
  Future<UserModel> getUser(String id) async {
    final response = await dio.get('/users/$id');
    return UserModel.fromJson(response.data);
  }
}

// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;
  final UserLocalDataSource localDataSource;

  UserRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final user = await remoteDataSource.getUser(id);
      await localDataSource.cacheUser(user);
      return Right(user);
    } on ServerException {
      return Left(ServerFailure());
    } on CacheException {
      return Left(CacheFailure());
    }
  }
}
```

**Responsibilities:**
- Data retrieval from external sources (API, Database)
- Data persistence (caching)
- Data models and serialization
- Repository implementations
- Data source implementations

---

### 3. **What is the Dependency Rule in Clean Architecture?**

The Dependency Rule states that source code dependencies must point only inward toward higher-level policies. Inner layers should not know anything about outer layers.

**The Rule:**
- Nothing in an inner circle can know anything about something in an outer circle
- Data formats declared in an outer circle should not be used by an inner circle
- Dependencies flow inward: Presentation → Domain ← Data

```dart
// ❌ WRONG: Domain layer depending on Data layer
// domain/usecases/get_user.dart
class GetUser {
  final UserRemoteDataSourceImpl dataSource; // Wrong! Domain shouldn't know about Data layer

  GetUser(this.dataSource);
}

// ✅ CORRECT: Domain layer defines interface, Data layer implements it
// domain/repositories/user_repository.dart
abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
}

// domain/usecases/get_user.dart
class GetUser {
  final UserRepository repository; // Correct! Uses abstraction from Domain layer

  GetUser(this.repository);

  Future<Either<Failure, User>> call(String id) {
    return repository.getUser(id);
  }
}

// data/repositories/user_repository_impl.dart
class UserRepositoryImpl implements UserRepository {
  // Data layer depends on Domain layer interface
  @override
  Future<Either<Failure, User>> getUser(String id) async {
    // Implementation
  }
}
```

**Visual representation:**
```
┌─────────────────────────────────────┐
│     Presentation Layer              │
│  (UI, State Management, Pages)      │
│         ↓ depends on ↓              │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│       Domain Layer                  │
│  (Entities, UseCases, Interfaces)   │
│         ↑ implemented by ↑          │
└─────────────────────────────────────┘
           ↑
┌─────────────────────────────────────┐
│         Data Layer                  │
│  (Repositories, DataSources, Models)│
└─────────────────────────────────────┘
```

**Key Points:**
- Domain layer is independent and at the center
- Both Presentation and Data layers depend on Domain
- Domain layer defines interfaces, outer layers implement them
- Enables testability and flexibility

---

### 4. **What are the key benefits of implementing Clean Architecture in Flutter projects?**

**1. Testability:**
```dart
// Easy to test Use Cases in isolation
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late GetUser getUser;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    getUser = GetUser(mockRepository);
  });

  test('should return User when repository call is successful', () async {
    // Arrange
    final testUser = User(id: '1', name: 'Test', email: 'test@test.com');
    when(() => mockRepository.getUser('1'))
        .thenAnswer((_) async => Right(testUser));

    // Act
    final result = await getUser('1');

    // Assert
    expect(result, Right(testUser));
    verify(() => mockRepository.getUser('1')).called(1);
  });
}
```

**2. Maintainability:**
```dart
// Easy to modify one layer without affecting others
// Change from Dio to Http without touching Domain or Presentation
class UserRemoteDataSourceImpl implements UserRemoteDataSource {
  final http.Client client; // Changed from Dio to http.Client

  @override
  Future<UserModel> getUser(String id) async {
    final response = await client.get(
      Uri.parse('https://api.example.com/users/$id'),
    );
    return UserModel.fromJson(json.decode(response.body));
  }
}
```

**3. Scalability:**
```dart
// Easy to add new features following the same structure
// features/
//   authentication/
//   products/
//   orders/
//   cart/
// Each feature follows the same three-layer structure
```

**4. Independence:**
```dart
// Easy to switch state management solutions
// From BLoC to GetX without changing Domain layer
class UserController extends GetxController {
  final GetUser getUser;

  UserController({required this.getUser});

  final user = Rx<User?>(null);
  final isLoading = false.obs;

  Future<void> fetchUser(String id) async {
    isLoading.value = true;
    final result = await getUser(id);
    result.fold(
      (failure) => Get.snackbar('Error', failure.message),
      (userData) => user.value = userData,
    );
    isLoading.value = false;
  }
}
```

**5. Reusability:**
```dart
// Use Cases can be reused across different parts of the app
class ProfilePage extends StatelessWidget {
  final GetUser getUser; // Injected Use Case

  // Use Case can also be used in SettingsPage, EditProfilePage, etc.
}
```

**6. Team Collaboration:**
```dart
// Different team members can work on different layers simultaneously
// Developer A: Works on UI (Presentation)
// Developer B: Works on API integration (Data)
// Developer C: Works on business logic (Domain)
```

**Summary of Benefits:**
- Easier to test
- Easier to maintain
- Easier to scale
- Framework independent
- Database independent
- UI independent
- Facilitates team collaboration
- Reduces coupling
- Increases code reusability

---

### 5. **How does Clean Architecture differ from MVC and MVVM patterns?**

**MVC (Model-View-Controller):**
```dart
// Traditional MVC in Flutter
class User {
  String name;
  String email;
}

class UserView extends StatelessWidget {
  final UserController controller;

  @override
  Widget build(BuildContext context) {
    return Text(controller.user.name);
  }
}

class UserController {
  User user;

  void fetchUser() {
    // Mix of business logic and API calls
    http.get('api/users/1').then((response) {
      user = User.fromJson(response.body);
    });
  }
}
```

**MVVM (Model-View-ViewModel):**
```dart
// MVVM pattern
class UserViewModel extends ChangeNotifier {
  User? _user;
  User? get user => _user;

  Future<void> fetchUser() async {
    // Still mixes data fetching with business logic
    final response = await http.get('api/users/1');
    _user = User.fromJson(response.body);
    notifyListeners();
  }
}

class UserView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Consumer<UserViewModel>(
      builder: (context, viewModel, child) {
        return Text(viewModel.user?.name ?? '');
      },
    );
  }
}
```

**Clean Architecture:**
```dart
// 1. Domain Layer - Pure business logic
class User {
  final String id;
  final String name;
  final String email;

  const User({required this.id, required this.name, required this.email});
}

abstract class UserRepository {
  Future<Either<Failure, User>> getUser(String id);
}

class GetUser {
  final UserRepository repository;

  GetUser(this.repository);

  Future<Either<Failure, User>> call(String id) {
    return repository.getUser(id);
  }
}

// 2. Data Layer - Data handling
class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }
}

class UserRepositoryImpl implements UserRepository {
  final UserRemoteDataSource remoteDataSource;

  UserRepositoryImpl(this.remoteDataSource);

  @override
  Future<Either<Failure, User>> getUser(String id) async {
    try {
      final userModel = await remoteDataSource.getUser(id);
      return Right(userModel);
    } catch (e) {
      return Left(ServerFailure());
    }
  }
}

// 3. Presentation Layer - UI and State
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser getUser;

  UserBloc({required this.getUser}) : super(UserInitial());
}

class UserPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return BlocBuilder<UserBloc, UserState>(
      builder: (context, state) {
        // UI implementation
      },
    );
  }
}
```

**Key Differences:**

| Aspect | MVC | MVVM | Clean Architecture |
|--------|-----|------|-------------------|
| **Layers** | 3 (Model, View, Controller) | 3 (Model, View, ViewModel) | 3+ (Presentation, Domain, Data) |
| **Business Logic** | Mixed in Controller | Mixed in ViewModel | Separated in Use Cases |
| **Testability** | Limited | Better | Excellent |
| **Dependencies** | Bidirectional | Unidirectional | Strict inward dependency |
| **Data Access** | Direct in Model | Direct in Model | Abstracted through Repository |
| **Independence** | Framework dependent | Framework dependent | Framework independent |
| **Scalability** | Limited | Good | Excellent |

**When to use each:**
- **MVC**: Simple apps, rapid prototyping
- **MVVM**: Medium complexity apps, good separation of UI and logic
- **Clean Architecture**: Complex apps, high testability requirements, long-term projects

---

### 6. **What is Separation of Concerns and how does Clean Architecture achieve it?**

Separation of Concerns (SoC) is a design principle that states that each module or layer should be responsible for a specific concern and should not overlap with other concerns.

**How Clean Architecture achieves SoC:**

**1. Layer Separation:**
```dart
// Each layer has distinct responsibilities

// PRESENTATION LAYER - Concerns: UI, User Input, State
// presentation/bloc/product_bloc.dart
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  final GetProducts getProducts;

  ProductBloc({required this.getProducts}) : super(ProductInitial()) {
    on<LoadProductsEvent>(_onLoadProducts);
  }

  Future<void> _onLoadProducts(
    LoadProductsEvent event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await getProducts();
    result.fold(
      (failure) => emit(ProductError(failure.message)),
      (products) => emit(ProductLoaded(products)),
    );
  }
}

// DOMAIN LAYER - Concerns: Business Logic, Business Rules
// domain/usecases/get_products.dart
class GetProducts {
  final ProductRepository repository;

  GetProducts(this.repository);

  Future<Either<Failure, List<Product>>> call() {
    // Business logic can be added here
    // e.g., filtering, validation, business rules
    return repository.getProducts();
  }
}

// domain/entities/product.dart
class Product {
  final String id;
  final String name;
  final double price;

  const Product({
    required this.id,
    required this.name,
    required this.price,
  });

  // Business logic methods
  bool isExpensive() => price > 100;

  double calculateDiscount(double percentage) {
    return price * (1 - percentage / 100);
  }
}

// DATA LAYER - Concerns: Data Fetching, Caching, Serialization
// data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;
  final ProductLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  ProductRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<Product>>> getProducts() async {
    if (await networkInfo.isConnected) {
      try {
        final products = await remoteDataSource.getProducts();
        await localDataSource.cacheProducts(products);
        return Right(products);
      } on ServerException {
        return Left(ServerFailure());
      }
    } else {
      try {
        final cachedProducts = await localDataSource.getCachedProducts();
        return Right(cachedProducts);
      } on CacheException {
        return Left(CacheFailure());
      }
    }
  }
}

// data/datasources/product_remote_data_source.dart
abstract class ProductRemoteDataSource {
  Future<List<ProductModel>> getProducts();
}

class ProductRemoteDataSourceImpl implements ProductRemoteDataSource {
  final Dio dio;

  ProductRemoteDataSourceImpl(this.dio);

  @override
  Future<List<ProductModel>> getProducts() async {
    final response = await dio.get('/products');
    return (response.data as List)
        .map((json) => ProductModel.fromJson(json))
        .toList();
  }
}
```

**2. Single Responsibility for Each Class:**
```dart
// Each class has ONE reason to change

// Concern: Validate email format
class EmailValidator {
  bool isValid(String email) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
  }
}

// Concern: User authentication business logic
class LoginUser {
  final AuthRepository repository;
  final EmailValidator emailValidator;

  LoginUser({
    required this.repository,
    required this.emailValidator,
  });

  Future<Either<Failure, User>> call(String email, String password) async {
    if (!emailValidator.isValid(email)) {
      return Left(ValidationFailure('Invalid email format'));
    }

    if (password.length < 6) {
      return Left(ValidationFailure('Password too short'));
    }

    return await repository.login(email, password);
  }
}

// Concern: Managing authentication state
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUser loginUser;
  final LogoutUser logoutUser;

  AuthBloc({
    required this.loginUser,
    required this.logoutUser,
  }) : super(AuthInitial());
}

// Concern: Displaying login UI
class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // UI implementation
  }
}
```

**3. Dependency Inversion:**
```dart
// High-level modules don't depend on low-level modules
// Both depend on abstractions

// High-level (Domain)
abstract class PaymentRepository {
  Future<Either<Failure, PaymentResult>> processPayment(PaymentDetails details);
}

// Low-level (Data) - implements the abstraction
class PaymentRepositoryImpl implements PaymentRepository {
  final StripeDataSource stripeDataSource;

  @override
  Future<Either<Failure, PaymentResult>> processPayment(
    PaymentDetails details,
  ) async {
    // Implementation
  }
}

// Easy to switch payment providers without changing domain logic
class PayPalRepositoryImpl implements PaymentRepository {
  final PayPalDataSource payPalDataSource;

  @override
  Future<Either<Failure, PaymentResult>> processPayment(
    PaymentDetails details,
  ) async {
    // Different implementation, same interface
  }
}
```

**Benefits of SoC in Clean Architecture:**
- Each layer can be developed independently
- Easy to locate bugs (know which layer to check)
- Changes in one concern don't affect others
- Better code organization
- Improved testability
- Easier to understand and maintain

---

### 7. **When should you use Clean Architecture in a Flutter project and when might it be overkill?**

**When to Use Clean Architecture:**

**1. Complex Business Logic:**
```dart
// Example: E-commerce app with complex pricing logic
class CalculateProductPrice {
  final PricingRepository repository;

  CalculateProductPrice(this.repository);

  Future<Either<Failure, double>> call({
    required Product product,
    required User user,
    String? couponCode,
  }) async {
    double price = product.basePrice;

    // Apply member discount
    if (user.isMember) {
      price = price * 0.9; // 10% member discount
    }

    // Apply coupon
    if (couponCode != null) {
      final coupon = await repository.validateCoupon(couponCode);
      price = coupon.fold(
        (failure) => price,
        (validCoupon) => price * (1 - validCoupon.discount),
      );
    }

    // Apply seasonal discount
    if (await repository.isSeasonalSale()) {
      price = price * 0.85; // 15% seasonal discount
    }

    // Apply tax
    final tax = await repository.getTaxRate(user.country);
    price = price * (1 + tax);

    return Right(price);
  }
}
```

**2. Multiple Data Sources:**
```dart
// Example: App that needs online and offline support
class ArticleRepositoryImpl implements ArticleRepository {
  final ArticleRemoteDataSource remoteDataSource;
  final ArticleLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  @override
  Future<Either<Failure, List<Article>>> getArticles() async {
    if (await networkInfo.isConnected) {
      try {
        final articles = await remoteDataSource.getArticles();
        await localDataSource.cacheArticles(articles);
        return Right(articles);
      } catch (e) {
        return Left(ServerFailure());
      }
    } else {
      try {
        final cachedArticles = await localDataSource.getCachedArticles();
        return Right(cachedArticles);
      } catch (e) {
        return Left(CacheFailure());
      }
    }
  }
}
```

**3. High Testability Requirements:**
```dart
// Clean Architecture makes unit testing easy
void main() {
  late GetUserProfile getUserProfile;
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    getUserProfile = GetUserProfile(mockRepository);
  });

  test('should return user profile when repository succeeds', () async {
    // Test implementation
  });

  test('should return failure when repository fails', () async {
    // Test implementation
  });
}
```

**4. Long-term Projects:**
- Projects expected to last 2+ years
- Projects with expected feature additions
- Projects with multiple developers
- Enterprise applications

**5. Multiple Platforms:**
```dart
// Business logic can be shared across platforms
// domain/usecases/ - same for mobile, web, desktop
// data/repositories/ - same for all platforms
// Only presentation layer differs per platform
```

**When It's Overkill:**

**1. Simple CRUD Apps:**
```dart
// Simple todo app - Clean Architecture might be too much
// Simple approach is sufficient:
class TodoProvider extends ChangeNotifier {
  List<Todo> _todos = [];

  Future<void> fetchTodos() async {
    final response = await http.get('api/todos');
    _todos = (json.decode(response.body) as List)
        .map((json) => Todo.fromJson(json))
        .toList();
    notifyListeners();
  }

  void addTodo(Todo todo) {
    _todos.add(todo);
    notifyListeners();
  }
}
```

**2. Prototypes or MVPs:**
```dart
// When you need to validate an idea quickly
// Use simpler architecture, refactor later if needed
```

**3. Small Teams (1-2 developers):**
- Overhead of maintaining multiple layers might not be worth it
- Communication is easier with fewer developers
- Can use simpler patterns like MVVM

**4. Simple Display Apps:**
```dart
// App that just displays static content or simple lists
class NewsListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<News>>(
      future: http.get('api/news').then((response) =>
        (json.decode(response.body) as List)
            .map((json) => News.fromJson(json))
            .toList()),
      builder: (context, snapshot) {
        // Display news
      },
    );
  }
}
```

**5. Apps with No Business Logic:**
- Settings pages
- Information display apps
- Simple calculators

**Decision Matrix:**

| Factor | Use Clean Architecture | Avoid Clean Architecture |
|--------|----------------------|--------------------------|
| **Project Size** | > 20 screens | < 10 screens |
| **Team Size** | 3+ developers | 1-2 developers |
| **Business Logic** | Complex | Simple or none |
| **Duration** | Long-term (2+ years) | Short-term (< 6 months) |
| **Testing** | High requirements | Low requirements |
| **Data Sources** | Multiple | Single |
| **Scalability** | High growth expected | Limited growth |

**Recommendation:**
Start with a simpler architecture. If you find yourself needing:
- More testability
- Better separation
- Easier scalability
- Multiple data sources

Then migrate to Clean Architecture. It's easier to move from simple to complex than to start with unnecessary complexity.

---

### 8. **What are the main challenges when implementing Clean Architecture in Flutter?**

**1. Learning Curve:**
```dart
// Challenge: Developers need to understand multiple concepts

// Concepts to learn:
// - Layer separation
// - Dependency injection
// - Repository pattern
// - Use cases
// - Entity vs Model
// - Error handling with Either
// - Testing strategies

// Example: New developer confusion
// ❌ Common mistake - putting business logic in BLoC
class UserBloc extends Bloc<UserEvent, UserState> {
  final http.Client client;

  UserBloc(this.client) : super(UserInitial()) {
    on<GetUserEvent>((event, emit) async {
      // ❌ Business logic and data fetching in BLoC
      final response = await client.get('/users/${event.id}');
      final user = User.fromJson(json.decode(response.body));

      // ❌ Business validation in BLoC
      if (user.age < 18) {
        emit(UserError('User must be 18 or older'));
      } else {
        emit(UserLoaded(user));
      }
    });
  }
}

// ✅ Correct approach
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetUser getUser; // Use case handles business logic

  UserBloc(this.getUser) : super(UserInitial()) {
    on<GetUserEvent>((event, emit) async {
      emit(UserLoading());
      final result = await getUser(event.id);
      result.fold(
        (failure) => emit(UserError(failure.message)),
        (user) => emit(UserLoaded(user)),
      );
    });
  }
}
```

**2. Boilerplate Code:**
```dart
// Challenge: More files and code to write

// For a simple feature, you need:
// 1. Entity
// domain/entities/product.dart
class Product {
  final String id;
  final String name;
  // ...
}

// 2. Model
// data/models/product_model.dart
class ProductModel extends Product {
  factory ProductModel.fromJson(Map<String, dynamic> json) {
    // ...
  }
  Map<String, dynamic> toJson() {
    // ...
  }
}

// 3. Repository interface
// domain/repositories/product_repository.dart
abstract class ProductRepository {
  Future<Either<Failure, Product>> getProduct(String id);
}

// 4. Repository implementation
// data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  // ...
}

// 5. Data source interface
// data/datasources/product_remote_data_source.dart
abstract class ProductRemoteDataSource {
  Future<ProductModel> getProduct(String id);
}

// 6. Data source implementation
// data/datasources/product_remote_data_source_impl.dart
class ProductRemoteDataSourceImpl implements ProductRemoteDataSource {
  // ...
}

// 7. Use case
// domain/usecases/get_product.dart
class GetProduct {
  // ...
}

// 8. State management (BLoC/Events/States)
// presentation/bloc/product_bloc.dart
// presentation/bloc/product_event.dart
// presentation/bloc/product_state.dart

// Solution: Use code generators
// - freezed for models and states
// - injectable for dependency injection
```

**3. Over-engineering for Simple Features:**
```dart
// Challenge: Simple operations become complex

// Simple preference storage becomes:

// ❌ Over-engineered for simple task
// domain/entities/user_preference.dart
class UserPreference {
  final String key;
  final String value;
}

// domain/usecases/save_preference.dart
class SavePreference {
  final PreferenceRepository repository;

  Future<Either<Failure, void>> call(UserPreference preference) {
    return repository.savePreference(preference);
  }
}

// ✅ Better approach for simple tasks
// Just use SharedPreferences directly in data layer
class SettingsLocalDataSource {
  final SharedPreferences prefs;

  Future<void> saveTheme(String theme) async {
    await prefs.setString('theme', theme);
  }
}

// Solution: Use Clean Architecture selectively
// - Complex business logic → Full Clean Architecture
// - Simple operations → Direct implementation
```

**4. Dependency Management:**
```dart
// Challenge: Managing dependencies becomes complex

// Wrong: Manual dependency management
void main() {
  final dio = Dio();
  final remoteDataSource = UserRemoteDataSourceImpl(dio);
  final localDataSource = UserLocalDataSourceImpl(
    await SharedPreferences.getInstance(),
  );
  final repository = UserRepositoryImpl(
    remoteDataSource: remoteDataSource,
    localDataSource: localDataSource,
  );
  final getUser = GetUser(repository);
  final userBloc = UserBloc(getUser);

  runApp(MyApp());
}

// ✅ Solution: Use dependency injection
// injection_container.dart
final sl = GetIt.instance;

Future<void> init() async {
  // BLoC
  sl.registerFactory(() => UserBloc(getUser: sl()));

  // Use cases
  sl.registerLazySingleton(() => GetUser(sl()));

  // Repository
  sl.registerLazySingleton<UserRepository>(
    () => UserRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
    ),
  );

  // Data sources
  sl.registerLazySingleton<UserRemoteDataSource>(
    () => UserRemoteDataSourceImpl(dio: sl()),
  );

  // External
  sl.registerLazySingleton(() => Dio());
}
```

**5. Testing Complexity:**
```dart
// Challenge: Need to mock multiple layers

void main() {
  late UserBloc bloc;
  late MockGetUser mockGetUser;
  late MockUserRepository mockRepository;
  late MockUserRemoteDataSource mockRemoteDataSource;

  setUp(() {
    mockGetUser = MockGetUser();
    bloc = UserBloc(getUser: mockGetUser);
  });

  // Need to understand mocking for each layer
  test('should emit [Loading, Loaded] when data is gotten successfully', () {
    // Arrange
    when(() => mockGetUser(any()))
        .thenAnswer((_) async => Right(testUser));

    // Assert later
    final expected = [
      UserLoading(),
      UserLoaded(testUser),
    ];
    expectLater(bloc.stream, emitsInOrder(expected));

    // Act
    bloc.add(GetUserEvent('1'));
  });
}

// Solution: Use testing utilities and learn testing patterns
```

**6. Performance Concerns:**
```dart
// Challenge: Extra layers might impact performance

// Problem: Multiple object conversions
// JSON → Model → Entity → State
final response = await dio.get('/user/1'); // JSON
final model = UserModel.fromJson(response.data); // Model
final entity = model as User; // Entity
emit(UserLoaded(entity)); // State

// Solution: Profile before optimizing
// Usually, the overhead is negligible
// Only optimize if performance issues are measured
```

**7. Team Alignment:**
```dart
// Challenge: Ensuring all team members follow the same structure

// Solution: Create team guidelines document
// example: architecture_guidelines.md
/*
## Guidelines

### Naming Conventions
- Use cases: Verb + Noun (GetUser, UpdateProfile)
- Repositories: Noun + Repository (UserRepository)
- Models: Noun + Model (UserModel)
- Entities: Just Noun (User, Product)

### File Organization
- Follow feature-first approach
- Group by feature, not by layer type

### Dependency Injection
- Use GetIt for all dependencies
- Register in injection_container.dart

### Testing
- Minimum 80% code coverage
- Test all use cases
- Mock repositories in tests
*/
```

**8. Folder Structure Decisions:**
```dart
// Challenge: Choosing between feature-first vs layer-first

// Layer-first approach:
// lib/
//   data/
//     models/
//     repositories/
//     datasources/
//   domain/
//     entities/
//     usecases/
//   presentation/
//     pages/
//     bloc/

// Feature-first approach:
// lib/
//   features/
//     authentication/
//       data/
//       domain/
//       presentation/
//     products/
//       data/
//       domain/
//       presentation/

// Solution: Choose based on project size
// Small projects: Layer-first
// Large projects: Feature-first
```

**Solutions to Challenges:**

1. **Learning Curve**: Provide training, documentation, and code reviews
2. **Boilerplate**: Use code generators (freezed, injectable, json_serializable)
3. **Over-engineering**: Apply architecture selectively based on complexity
4. **Dependencies**: Use GetIt or Injectable for automatic DI
5. **Testing**: Create testing utilities and templates
6. **Performance**: Profile first, optimize only when needed
7. **Team Alignment**: Create and maintain architecture guidelines
8. **Structure**: Choose one approach and stick to it

---

## Layers & Structure

### 9. **What is the Presentation Layer and what components does it contain?**

The Presentation Layer is the outermost layer responsible for everything the user sees and interacts with. It handles UI rendering, user input, and presentation logic.

**Components:**

**1. Pages/Screens:**
```dart
// presentation/pages/home_page.dart
class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: BlocProvider(
        create: (context) => sl<ProductBloc>()..add(LoadProductsEvent()),
        child: const ProductListView(),
      ),
    );
  }
}
```

**2. Widgets:**
```dart
// presentation/widgets/product_card.dart
class ProductCard extends StatelessWidget {
  final Product product;

  const ProductCard({
    Key? key,
    required this.product,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(product.name),
        subtitle: Text('\$${product.price}'),
        trailing: IconButton(
          icon: const Icon(Icons.add_shopping_cart),
          onPressed: () {
            context.read<CartBloc>().add(AddToCartEvent(product));
          },
        ),
      ),
    );
  }
}
```

**3. State Management (BLoC example):**
```dart
// presentation/bloc/product_bloc.dart
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  final GetProducts getProducts;
  final SearchProducts searchProducts;

  ProductBloc({
    required this.getProducts,
    required this.searchProducts,
  }) : super(ProductInitial()) {
    on<LoadProductsEvent>(_onLoadProducts);
    on<SearchProductsEvent>(_onSearchProducts);
  }

  Future<void> _onLoadProducts(
    LoadProductsEvent event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await getProducts();
    result.fold(
      (failure) => emit(ProductError(_mapFailureToMessage(failure))),
      (products) => emit(ProductLoaded(products)),
    );
  }

  Future<void> _onSearchProducts(
    SearchProductsEvent event,
    Emitter<ProductState> emit,
  ) async {
    emit(ProductLoading());
    final result = await searchProducts(event.query);
    result.fold(
      (failure) => emit(ProductError(_mapFailureToMessage(failure))),
      (products) => emit(ProductLoaded(products)),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    switch (failure.runtimeType) {
      case ServerFailure:
        return 'Server error. Please try again later.';
      case NetworkFailure:
        return 'No internet connection.';
      case CacheFailure:
        return 'Failed to load cached data.';
      default:
        return 'Unexpected error occurred.';
    }
  }
}

// presentation/bloc/product_event.dart
abstract class ProductEvent extends Equatable {
  const ProductEvent();

  @override
  List<Object> get props => [];
}

class LoadProductsEvent extends ProductEvent {}

class SearchProductsEvent extends ProductEvent {
  final String query;

  const SearchProductsEvent(this.query);

  @override
  List<Object> get props => [query];
}

// presentation/bloc/product_state.dart
abstract class ProductState extends Equatable {
  const ProductState();

  @override
  List<Object> get props => [];
}

class ProductInitial extends ProductState {}

class ProductLoading extends ProductState {}

class ProductLoaded extends ProductState {
  final List<Product> products;

  const ProductLoaded(this.products);

  @override
  List<Object> get props => [products];
}

class ProductError extends ProductState {
  final String message;

  const ProductError(this.message);

  @override
  List<Object> get props => [message];
}
```

**4. View Models (with GetX):**
```dart
// presentation/controllers/product_controller.dart
class ProductController extends GetxController {
  final GetProducts getProducts;
  final AddToCart addToCart;

  ProductController({
    required this.getProducts,
    required this.addToCart,
  });

  final products = <Product>[].obs;
  final isLoading = false.obs;
  final errorMessage = ''.obs;

  @override
  void onInit() {
    super.onInit();
    loadProducts();
  }

  Future<void> loadProducts() async {
    isLoading.value = true;
    final result = await getProducts();
    result.fold(
      (failure) {
        isLoading.value = false;
        errorMessage.value = _mapFailureToMessage(failure);
      },
      (productList) {
        isLoading.value = false;
        products.value = productList;
      },
    );
  }

  Future<void> addProductToCart(Product product) async {
    final result = await addToCart(product);
    result.fold(
      (failure) => Get.snackbar('Error', _mapFailureToMessage(failure)),
      (_) => Get.snackbar('Success', 'Product added to cart'),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    if (failure is ServerFailure) return 'Server error';
    if (failure is NetworkFailure) return 'No internet';
    return 'Unknown error';
  }
}
```

**5. Providers (with Riverpod):**
```dart
// presentation/providers/product_provider.dart
final productProvider = StateNotifierProvider<ProductNotifier, ProductState>(
  (ref) => ProductNotifier(
    getProducts: ref.watch(getProductsUseCaseProvider),
  ),
);

class ProductNotifier extends StateNotifier<ProductState> {
  final GetProducts getProducts;

  ProductNotifier({required this.getProducts}) : super(ProductInitial());

  Future<void> loadProducts() async {
    state = ProductLoading();
    final result = await getProducts();
    state = result.fold(
      (failure) => ProductError(_mapFailureToMessage(failure)),
      (products) => ProductLoaded(products),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    return 'Error loading products';
  }
}
```

**6. Navigation:**
```dart
// presentation/navigation/app_router.dart
class AppRouter {
  static const String home = '/';
  static const String productDetails = '/product-details';
  static const String cart = '/cart';

  static Route<dynamic> onGenerateRoute(RouteSettings settings) {
    switch (settings.name) {
      case home:
        return MaterialPageRoute(builder: (_) => const HomePage());

      case productDetails:
        final product = settings.arguments as Product;
        return MaterialPageRoute(
          builder: (_) => ProductDetailsPage(product: product),
        );

      case cart:
        return MaterialPageRoute(builder: (_) => const CartPage());

      default:
        return MaterialPageRoute(
          builder: (_) => const Scaffold(
            body: Center(child: Text('Page not found')),
          ),
        );
    }
  }
}
```

**7. Input Validators:**
```dart
// presentation/utils/input_validators.dart
class InputValidators {
  static String? validateEmail(String? value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(value)) {
      return 'Enter a valid email';
    }
    return null;
  }

  static String? validatePassword(String? value) {
    if (value == null || value.isEmpty) {
      return 'Password is required';
    }
    if (value.length < 6) {
      return 'Password must be at least 6 characters';
    }
    return null;
  }
}
```

**8. UI Utilities:**
```dart
// presentation/utils/ui_helpers.dart
class UIHelpers {
  static void showSuccessSnackbar(BuildContext context, String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.green,
      ),
    );
  }

  static void showErrorDialog(BuildContext context, String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}
```

**Responsibilities of Presentation Layer:**
- Display data to users
- Handle user interactions
- Manage UI state
- Navigate between screens
- Show loading indicators
- Display error messages
- Validate user input (format only, not business rules)
- Call use cases through state management

**What NOT to include:**
- Business logic (belongs in Domain)
- Data fetching (belongs in Data)
- API calls (belongs in Data)
- Database operations (belongs in Data)
- Business validations (belongs in Domain)

---

### 10. **What is the Domain Layer and why is it considered the core of Clean Architecture?**

The Domain Layer is the innermost layer containing the business logic and rules. It's framework-independent and doesn't depend on any external layer.

**Why it's the Core:**

1. **Contains Business Rules**
2. **Framework Independent**
3. **No External Dependencies**
4. **Most Stable Layer**
5. **Defines System Behavior**

**Components:**

**1. Entities (Business Objects):**
```dart
// domain/entities/order.dart
class Order {
  final String id;
  final List<OrderItem> items;
  final DateTime createdAt;
  final OrderStatus status;
  final double subtotal;
  final double tax;
  final double shipping;

  const Order({
    required this.id,
    required this.items,
    required this.createdAt,
    required this.status,
    required this.subtotal,
    required this.tax,
    required this.shipping,
  });

  // Business logic methods
  double get total => subtotal + tax + shipping;

  bool get canBeCancelled {
    return status == OrderStatus.pending ||
           status == OrderStatus.processing;
  }

  bool get isDelivered => status == OrderStatus.delivered;

  int get itemCount {
    return items.fold(0, (sum, item) => sum + item.quantity);
  }

  Order copyWith({
    OrderStatus? status,
    List<OrderItem>? items,
  }) {
    return Order(
      id: id,
      items: items ?? this.items,
      createdAt: createdAt,
      status: status ?? this.status,
      subtotal: subtotal,
      tax: tax,
      shipping: shipping,
    );
  }
}

class OrderItem {
  final String productId;
  final String productName;
  final int quantity;
  final double price;

  const OrderItem({
    required this.productId,
    required this.productName,
    required this.quantity,
    required this.price,
  });

  double get total => quantity * price;
}

enum OrderStatus {
  pending,
  processing,
  shipped,
  delivered,
  cancelled,
}
```

**2. Repository Interfaces:**
```dart
// domain/repositories/order_repository.dart
abstract class OrderRepository {
  Future<Either<Failure, Order>> getOrder(String id);
  Future<Either<Failure, List<Order>>> getUserOrders(String userId);
  Future<Either<Failure, Order>> createOrder(CreateOrderParams params);
  Future<Either<Failure, Order>> updateOrderStatus(
    String orderId,
    OrderStatus status,
  );
  Future<Either<Failure, void>> cancelOrder(String orderId);
}

// domain/repositories/payment_repository.dart
abstract class PaymentRepository {
  Future<Either<Failure, PaymentResult>> processPayment(
    PaymentParams params,
  );
  Future<Either<Failure, RefundResult>> refundPayment(String paymentId);
  Future<Either<Failure, List<PaymentMethod>>> getPaymentMethods(
    String userId,
  );
}
```

**3. Use Cases (Business Operations):**
```dart
// domain/usecases/create_order.dart
class CreateOrder {
  final OrderRepository orderRepository;
  final PaymentRepository paymentRepository;
  final InventoryRepository inventoryRepository;

  CreateOrder({
    required this.orderRepository,
    required this.paymentRepository,
    required this.inventoryRepository,
  });

  Future<Either<Failure, Order>> call(CreateOrderParams params) async {
    // Business rule: Check if all items are in stock
    for (final item in params.items) {
      final stockResult = await inventoryRepository.checkStock(
        item.productId,
        item.quantity,
      );

      final hasStock = stockResult.fold(
        (failure) => false,
        (inStock) => inStock,
      );

      if (!hasStock) {
        return Left(ValidationFailure(
          'Product ${item.productName} is out of stock',
        ));
      }
    }

    // Business rule: Calculate totals
    final subtotal = params.items.fold(
      0.0,
      (sum, item) => sum + (item.price * item.quantity),
    );

    // Business rule: Minimum order amount
    if (subtotal < 10.0) {
      return Left(ValidationFailure('Minimum order amount is \$10'));
    }

    // Business rule: Calculate tax (example: 10%)
    final tax = subtotal * 0.10;

    // Business rule: Free shipping over $50
    final shipping = subtotal >= 50.0 ? 0.0 : 5.99;

    // Create order
    final orderResult = await orderRepository.createOrder(
      params.copyWith(
        subtotal: subtotal,
        tax: tax,
        shipping: shipping,
      ),
    );

    return orderResult.fold(
      (failure) => Left(failure),
      (order) async {
        // Process payment
        final paymentResult = await paymentRepository.processPayment(
          PaymentParams(
            orderId: order.id,
            amount: order.total,
            paymentMethodId: params.paymentMethodId,
          ),
        );

        return paymentResult.fold(
          (failure) {
            // Payment failed, cancel order
            orderRepository.cancelOrder(order.id);
            return Left(PaymentFailure('Payment failed'));
          },
          (payment) {
            // Update inventory
            for (final item in params.items) {
              inventoryRepository.reduceStock(
                item.productId,
                item.quantity,
              );
            }
            return Right(order);
          },
        );
      },
    );
  }
}

class CreateOrderParams {
  final String userId;
  final List<OrderItem> items;
  final String shippingAddress;
  final String paymentMethodId;
  final double subtotal;
  final double tax;
  final double shipping;

  CreateOrderParams({
    required this.userId,
    required this.items,
    required this.shippingAddress,
    required this.paymentMethodId,
    this.subtotal = 0,
    this.tax = 0,
    this.shipping = 0,
  });

  CreateOrderParams copyWith({
    double? subtotal,
    double? tax,
    double? shipping,
  }) {
    return CreateOrderParams(
      userId: userId,
      items: items,
      shippingAddress: shippingAddress,
      paymentMethodId: paymentMethodId,
      subtotal: subtotal ?? this.subtotal,
      tax: tax ?? this.tax,
      shipping: shipping ?? this.shipping,
    );
  }
}
```

**4. Value Objects:**
```dart
// domain/entities/email.dart
class Email {
  final String value;

  Email._(this.value);

  static Either<Failure, Email> create(String input) {
    if (input.isEmpty) {
      return Left(ValidationFailure('Email cannot be empty'));
    }

    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(input)) {
      return Left(ValidationFailure('Invalid email format'));
    }

    return Right(Email._(input));
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is Email && value == other.value;

  @override
  int get hashCode => value.hashCode;

  @override
  String toString() => value;
}

// domain/entities/money.dart
class Money {
  final double amount;
  final String currency;

  const Money({
    required this.amount,
    required this.currency,
  });

  Money operator +(Money other) {
    if (currency != other.currency) {
      throw ArgumentError('Cannot add different currencies');
    }
    return Money(amount: amount + other.amount, currency: currency);
  }

  Money operator -(Money other) {
    if (currency != other.currency) {
      throw ArgumentError('Cannot subtract different currencies');
    }
    return Money(amount: amount - other.amount, currency: currency);
  }

  Money operator *(double multiplier) {
    return Money(amount: amount * multiplier, currency: currency);
  }

  bool operator >(Money other) {
    if (currency != other.currency) {
      throw ArgumentError('Cannot compare different currencies');
    }
    return amount > other.amount;
  }

  String get formatted {
    switch (currency) {
      case 'USD':
        return '\$${amount.toStringAsFixed(2)}';
      case 'EUR':
        return '€${amount.toStringAsFixed(2)}';
      default:
        return '$amount $currency';
    }
  }
}
```

**5. Business Validators:**
```dart
// domain/validators/order_validator.dart
class OrderValidator {
  static Either<Failure, void> validateOrderCreation(
    List<OrderItem> items,
    String shippingAddress,
  ) {
    // Business rule: Order must have at least one item
    if (items.isEmpty) {
      return Left(ValidationFailure('Order must contain at least one item'));
    }

    // Business rule: Each item quantity must be positive
    for (final item in items) {
      if (item.quantity <= 0) {
        return Left(ValidationFailure('Item quantity must be positive'));
      }

      // Business rule: Maximum quantity per item
      if (item.quantity > 99) {
        return Left(ValidationFailure(
          'Maximum quantity per item is 99',
        ));
      }
    }

    // Business rule: Shipping address is required
    if (shippingAddress.trim().isEmpty) {
      return Left(ValidationFailure('Shipping address is required'));
    }

    return const Right(null);
  }

  static Either<Failure, void> validateOrderCancellation(Order order) {
    // Business rule: Only pending or processing orders can be cancelled
    if (!order.canBeCancelled) {
      return Left(ValidationFailure(
        'Order cannot be cancelled at this stage',
      ));
    }

    // Business rule: Cannot cancel order after 24 hours
    final hoursSinceOrder = DateTime.now().difference(order.createdAt).inHours;
    if (hoursSinceOrder > 24) {
      return Left(ValidationFailure(
        'Order can only be cancelled within 24 hours',
      ));
    }

    return const Right(null);
  }
}
```

**6. Failures (Business Errors):**
```dart
// domain/failures/failure.dart
abstract class Failure extends Equatable {
  final String message;

  const Failure(this.message);

  @override
  List<Object> get props => [message];
}

class ServerFailure extends Failure {
  const ServerFailure([super.message = 'Server error occurred']);
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No internet connection']);
}

class CacheFailure extends Failure {
  const CacheFailure([super.message = 'Cache error occurred']);
}

class ValidationFailure extends Failure {
  const ValidationFailure(super.message);
}

class PaymentFailure extends Failure {
  const PaymentFailure(super.message);
}

class AuthenticationFailure extends Failure {
  const AuthenticationFailure([super.message = 'Authentication failed']);
}

class PermissionFailure extends Failure {
  const PermissionFailure([super.message = 'Permission denied']);
}
```

**Why Domain Layer is the Core:**

**1. Independence:**
```dart
// Domain layer has NO imports from other layers
// ❌ NO Flutter imports
// ❌ NO http, dio imports
// ❌ NO database imports
// ✅ ONLY Dart core and domain-specific packages (like dartz)

// This makes it:
// - Testable without Flutter
// - Reusable across platforms
// - Stable and resistant to change
```

**2. Business Logic Centralization:**
```dart
// All business rules are in one place
// Easy to find, understand, and modify
// Example: Discount calculation logic
class ApplyDiscount {
  final ProductRepository repository;

  ApplyDiscount(this.repository);

  Future<Either<Failure, double>> call(
    Product product,
    User user,
    String? couponCode,
  ) async {
    double price = product.price;

    // Business rule: VIP users get 15% off
    if (user.isVIP) {
      price *= 0.85;
    }

    // Business rule: First-time buyers get 10% off
    if (await _isFirstTimeBuyer(user.id)) {
      price *= 0.90;
    }

    // Business rule: Apply coupon if valid
    if (couponCode != null) {
      final couponResult = await repository.validateCoupon(couponCode);
      price = couponResult.fold(
        (failure) => price,
        (discount) => price * (1 - discount),
      );
    }

    return Right(price);
  }

  Future<bool> _isFirstTimeBuyer(String userId) async {
    final orders = await repository.getUserOrderCount(userId);
    return orders.fold((failure) => false, (count) => count == 0);
  }
}
```

**3. Single Source of Truth:**
```dart
// Business entities defined once, used everywhere
// All layers reference the same User entity
// Changes in one place affect entire app consistently
```

**Benefits:**
- Easy to test (no external dependencies)
- Highly maintainable
- Framework independent
- Can be shared across platforms
- Changes are isolated and controlled
- Business logic is explicit and documented

---

### 11. **What is the Data Layer and what are its main responsibilities?**

The Data Layer is the outermost layer responsible for data retrieval, persistence, and communication with external data sources.

**Main Responsibilities:**

**1. Data Fetching from APIs:**
```dart
// data/datasources/product_remote_data_source.dart
abstract class ProductRemoteDataSource {
  Future<List<ProductModel>> getProducts();
  Future<ProductModel> getProductById(String id);
  Future<List<ProductModel>> searchProducts(String query);
}

class ProductRemoteDataSourceImpl implements ProductRemoteDataSource {
  final Dio dio;

  ProductRemoteDataSourceImpl({required this.dio});

  @override
  Future<List<ProductModel>> getProducts() async {
    try {
      final response = await dio.get(
        '/products',
        options: Options(
          headers: {'Accept': 'application/json'},
        ),
      );

      if (response.statusCode == 200) {
        return (response.data['data'] as List)
            .map((json) => ProductModel.fromJson(json))
            .toList();
      } else {
        throw ServerException();
      }
    } on DioException catch (e) {
      if (e.type == DioExceptionType.connectionTimeout ||
          e.type == DioExceptionType.receiveTimeout) {
        throw NetworkException();
      }
      throw ServerException();
    }
  }

  @override
  Future<ProductModel> getProductById(String id) async {
    final response = await dio.get('/products/$id');

    if (response.statusCode == 200) {
      return ProductModel.fromJson(response.data['data']);
    } else if (response.statusCode == 404) {
      throw NotFoundException('Product not found');
    } else {
      throw ServerException();
    }
  }

  @override
  Future<List<ProductModel>> searchProducts(String query) async {
    final response = await dio.get(
      '/products/search',
      queryParameters: {'q': query},
    );

    if (response.statusCode == 200) {
      return (response.data['data'] as List)
          .map((json) => ProductModel.fromJson(json))
          .toList();
    } else {
      throw ServerException();
    }
  }
}
```

**2. Local Data Storage:**
```dart
// data/datasources/product_local_data_source.dart
abstract class ProductLocalDataSource {
  Future<List<ProductModel>> getCachedProducts();
  Future<ProductModel> getCachedProduct(String id);
  Future<void> cacheProducts(List<ProductModel> products);
  Future<void> cacheProduct(ProductModel product);
  Future<void> clearCache();
}

// Using Hive
class ProductLocalDataSourceHiveImpl implements ProductLocalDataSource {
  final Box<ProductModel> productBox;

  ProductLocalDataSourceHiveImpl({required this.productBox});

  @override
  Future<List<ProductModel>> getCachedProducts() async {
    if (productBox.isEmpty) {
      throw CacheException();
    }
    return productBox.values.toList();
  }

  @override
  Future<ProductModel> getCachedProduct(String id) async {
    final product = productBox.get(id);
    if (product == null) {
      throw CacheException();
    }
    return product;
  }

  @override
  Future<void> cacheProducts(List<ProductModel> products) async {
    await productBox.clear();
    for (final product in products) {
      await productBox.put(product.id, product);
    }
  }

  @override
  Future<void> cacheProduct(ProductModel product) async {
    await productBox.put(product.id, product);
  }

  @override
  Future<void> clearCache() async {
    await productBox.clear();
  }
}

// Using SharedPreferences
class ProductLocalDataSourcePrefsImpl implements ProductLocalDataSource {
  final SharedPreferences sharedPreferences;
  static const String cachedProductsKey = 'CACHED_PRODUCTS';

  ProductLocalDataSourcePrefsImpl({required this.sharedPreferences});

  @override
  Future<List<ProductModel>> getCachedProducts() {
    final jsonString = sharedPreferences.getString(cachedProductsKey);
    if (jsonString == null) {
      throw CacheException();
    }

    final jsonList = json.decode(jsonString) as List;
    return Future.value(
      jsonList.map((json) => ProductModel.fromJson(json)).toList(),
    );
  }

  @override
  Future<void> cacheProducts(List<ProductModel> products) {
    final jsonList = products.map((product) => product.toJson()).toList();
    return sharedPreferences.setString(
      cachedProductsKey,
      json.encode(jsonList),
    );
  }

  @override
  Future<void> clearCache() {
    return sharedPreferences.remove(cachedProductsKey);
  }

  @override
  Future<ProductModel> getCachedProduct(String id) async {
    final products = await getCachedProducts();
    try {
      return products.firstWhere((p) => p.id == id);
    } catch (e) {
      throw CacheException();
    }
  }

  @override
  Future<void> cacheProduct(ProductModel product) async {
    final products = await getCachedProducts();
    final index = products.indexWhere((p) => p.id == product.id);

    if (index != -1) {
      products[index] = product;
    } else {
      products.add(product);
    }

    await cacheProducts(products);
  }
}
```

**3. Data Models and Serialization:**
```dart
// data/models/product_model.dart
class ProductModel extends Product {
  const ProductModel({
    required super.id,
    required super.name,
    required super.description,
    required super.price,
    required super.imageUrl,
    required super.category,
    required super.rating,
    required super.inStock,
  });

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      price: (json['price'] as num).toDouble(),
      imageUrl: json['image_url'] as String,
      category: json['category'] as String,
      rating: (json['rating'] as num?)?.toDouble() ?? 0.0,
      inStock: json['in_stock'] as bool? ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'image_url': imageUrl,
      'category': category,
      'rating': rating,
      'in_stock': inStock,
    };
  }

  // Hive adapter (if using Hive)
  factory ProductModel.fromHive(Map<dynamic, dynamic> map) {
    return ProductModel(
      id: map['id'] as String,
      name: map['name'] as String,
      description: map['description'] as String,
      price: map['price'] as double,
      imageUrl: map['image_url'] as String,
      category: map['category'] as String,
      rating: map['rating'] as double,
      inStock: map['in_stock'] as bool,
    );
  }

  Map<String, dynamic> toHive() {
    return {
      'id': id,
      'name': name,
      'description': description,
      'price': price,
      'image_url': imageUrl,
      'category': category,
      'rating': rating,
      'in_stock': inStock,
    };
  }
}
```

**4. Repository Implementation:**
```dart
// data/repositories/product_repository_impl.dart
class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;
  final ProductLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  ProductRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, List<Product>>> getProducts() async {
    if (await networkInfo.isConnected) {
      try {
        final products = await remoteDataSource.getProducts();
        await localDataSource.cacheProducts(products);
        return Right(products);
      } on ServerException {
        return const Left(ServerFailure('Failed to fetch products'));
      } on NetworkException {
        return const Left(NetworkFailure());
      }
    } else {
      try {
        final cachedProducts = await localDataSource.getCachedProducts();
        return Right(cachedProducts);
      } on CacheException {
        return const Left(CacheFailure('No cached data available'));
      }
    }
  }

  @override
  Future<Either<Failure, Product>> getProductById(String id) async {
    // Try cache first for better performance
    try {
      final cachedProduct = await localDataSource.getCachedProduct(id);
      return Right(cachedProduct);
    } on CacheException {
      // Cache miss, fetch from remote
    }

    if (await networkInfo.isConnected) {
      try {
        final product = await remoteDataSource.getProductById(id);
        await localDataSource.cacheProduct(product);
        return Right(product);
      } on NotFoundException {
        return const Left(ValidationFailure('Product not found'));
      } on ServerException {
        return const Left(ServerFailure());
      }
    } else {
      return const Left(NetworkFailure());
    }
  }

  @override
  Future<Either<Failure, List<Product>>> searchProducts(String query) async {
    if (query.isEmpty) {
      return const Left(ValidationFailure('Search query cannot be empty'));
    }

    if (await networkInfo.isConnected) {
      try {
        final products = await remoteDataSource.searchProducts(query);
        return Right(products);
      } on ServerException {
        return const Left(ServerFailure());
      }
    } else {
      // Offline search in cached data
      try {
        final cachedProducts = await localDataSource.getCachedProducts();
        final filteredProducts = cachedProducts
            .where((p) => p.name.toLowerCase().contains(query.toLowerCase()))
            .toList();
        return Right(filteredProducts);
      } on CacheException {
        return const Left(CacheFailure());
      }
    }
  }
}
```

**5. Network Helper:**
```dart
// data/network/network_info.dart
abstract class NetworkInfo {
  Future<bool> get isConnected;
}

class NetworkInfoImpl implements NetworkInfo {
  final InternetConnectionChecker connectionChecker;

  NetworkInfoImpl(this.connectionChecker);

  @override
  Future<bool> get isConnected => connectionChecker.hasConnection;
}
```

**6. Exception Handling:**
```dart
// data/exceptions/exceptions.dart
class ServerException implements Exception {
  final String? message;

  ServerException([this.message]);
}

class NetworkException implements Exception {
  final String? message;

  NetworkException([this.message]);
}

class CacheException implements Exception {
  final String? message;

  CacheException([this.message]);
}

class NotFoundException implements Exception {
  final String message;

  NotFoundException(this.message);
}

class UnauthorizedException implements Exception {
  final String? message;

  UnauthorizedException([this.message]);
}
```

**7. API Client Configuration:**
```dart
// data/network/dio_client.dart
class DioClient {
  static Dio createDio() {
    final dio = Dio(
      BaseOptions(
        baseUrl: 'https://api.example.com/v1',
        connectTimeout: const Duration(seconds: 30),
        receiveTimeout: const Duration(seconds: 30),
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
      ),
    );

    // Add interceptors
    dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
      logPrint: (obj) => print(obj),
    ));

    dio.interceptors.add(AuthInterceptor());

    return dio;
  }
}

// data/network/auth_interceptor.dart
class AuthInterceptor extends Interceptor {
  final AuthLocalDataSource authLocalDataSource;

  AuthInterceptor({required this.authLocalDataSource});

  @override
  Future<void> onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) async {
    final token = await authLocalDataSource.getToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      // Token expired, refresh or logout
      authLocalDataSource.clearToken();
    }
    handler.next(err);
  }
}
```

**Responsibilities Summary:**
- Fetch data from APIs
- Store data locally (cache, database)
- Transform API responses to Models
- Transform Entities to Models for storage
- Handle network errors
- Manage caching strategies
- Implement repository interfaces from Domain
- Provide offline support

**What NOT to include:**
- Business logic (belongs in Domain)
- UI logic (belongs in Presentation)
- Business validation (belongs in Domain)
- State management (belongs in Presentation)

---

### 12. **How do the three layers communicate with each other in Clean Architecture?**

Communication follows the Dependency Rule: dependencies flow inward, with outer layers depending on inner layers.

**Communication Flow:**

```dart
// ┌──────────────────────────────────────────────┐
// │          PRESENTATION LAYER                   │
// │  (Depends on Domain, doesn't know about Data) │
// └──────────────────────────────────────────────┘
//                      ↓ uses
// ┌──────────────────────────────────────────────┐
// │            DOMAIN LAYER                       │
// │  (Independent, defines interfaces)            │
// └──────────────────────────────────────────────┘
//                      ↑ implements
// ┌──────────────────────────────────────────────┐
// │            DATA LAYER                         │
// │  (Depends on Domain, implements interfaces)   │
// └──────────────────────────────────────────────┘
```

**Example: User Login Flow**

**1. Presentation → Domain:**
```dart
// presentation/bloc/auth_bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUser loginUser; // Use case from Domain

  AuthBloc({required this.loginUser}) : super(AuthInitial()) {
    on<LoginEvent>(_onLogin);
  }

  Future<void> _onLogin(
    LoginEvent event,
    Emitter<AuthState> emit,
  ) async {
    emit(AuthLoading());

    // Presentation calls Domain use case
    final result = await loginUser(LoginParams(
      email: event.email,
      password: event.password,
    ));

    result.fold(
      (failure) => emit(AuthError(_mapFailureToMessage(failure))),
      (user) => emit(AuthSuccess(user)),
    );
  }

  String _mapFailureToMessage(Failure failure) {
    if (failure is ServerFailure) return 'Server error';
    if (failure is NetworkFailure) return 'No internet connection';
    if (failure is AuthenticationFailure) return 'Invalid credentials';
    return 'Unknown error';
  }
}
```

**2. Domain Use Case:**
```dart
// domain/usecases/login_user.dart
class LoginUser {
  final AuthRepository repository; // Repository interface from Domain

  LoginUser(this.repository);

  Future<Either<Failure, User>> call(LoginParams params) async {
    // Business validation
    if (params.email.isEmpty) {
      return const Left(ValidationFailure('Email is required'));
    }

    if (params.password.isEmpty) {
      return const Left(ValidationFailure('Password is required'));
    }

    if (params.password.length < 6) {
      return const Left(ValidationFailure('Password must be at least 6 characters'));
    }

    // Call repository (Domain doesn't know it's implemented in Data layer)
    return await repository.login(params.email, params.password);
  }
}

class LoginParams {
  final String email;
  final String password;

  LoginParams({
    required this.email,
    required this.password,
  });
}
```

**3. Domain Repository Interface:**
```dart
// domain/repositories/auth_repository.dart
abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, User>> register(String email, String password, String name);
  Future<Either<Failure, void>> logout();
  Future<Either<Failure, User>> getCurrentUser();
}
```

**4. Data → Domain (Implementation):**
```dart
// data/repositories/auth_repository_impl.dart
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    if (!await networkInfo.isConnected) {
      return const Left(NetworkFailure());
    }

    try {
      // Data source returns Model (Data layer)
      final userModel = await remoteDataSource.login(email, password);

      // Cache user data
      await localDataSource.cacheUser(userModel);
      await localDataSource.cacheToken(userModel.token);

      // Return Entity (Domain layer)
      // Model extends Entity, so it can be returned as Entity
      return Right(userModel);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message ?? 'Server error'));
    } on UnauthorizedException {
      return const Left(AuthenticationFailure('Invalid credentials'));
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> getCurrentUser() async {
    try {
      // Try to get from cache first
      final cachedUser = await localDataSource.getCachedUser();
      return Right(cachedUser);
    } on CacheException {
      if (!await networkInfo.isConnected) {
        return const Left(NetworkFailure());
      }

      try {
        final userModel = await remoteDataSource.getCurrentUser();
        await localDataSource.cacheUser(userModel);
        return Right(userModel);
      } on UnauthorizedException {
        return const Left(AuthenticationFailure('Not authenticated'));
      } on ServerException {
        return const Left(ServerFailure());
      }
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      await remoteDataSource.logout();
      await localDataSource.clearCache();
      return const Right(null);
    } catch (e) {
      return Left(ServerFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, User>> register(
    String email,
    String password,
    String name,
  ) async {
    if (!await networkInfo.isConnected) {
      return const Left(NetworkFailure());
    }

    try {
      final userModel = await remoteDataSource.register(email, password, name);
      await localDataSource.cacheUser(userModel);
      await localDataSource.cacheToken(userModel.token);
      return Right(userModel);
    } on ServerException catch (e) {
      return Left(ServerFailure(e.message ?? 'Server error'));
    }
  }
}
```

**5. Data Sources:**
```dart
// data/datasources/auth_remote_data_source.dart
abstract class AuthRemoteDataSource {
  Future<UserModel> login(String email, String password);
  Future<UserModel> register(String email, String password, String name);
  Future<void> logout();
  Future<UserModel> getCurrentUser();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSourceImpl({required this.dio});

  @override
  Future<UserModel> login(String email, String password) async {
    try {
      final response = await dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      if (response.statusCode == 200) {
        return UserModel.fromJson(response.data['data']);
      } else if (response.statusCode == 401) {
        throw UnauthorizedException('Invalid credentials');
      } else {
        throw ServerException('Login failed');
      }
    } on DioException catch (e) {
      if (e.response?.statusCode == 401) {
        throw UnauthorizedException('Invalid credentials');
      }
      throw ServerException(e.message);
    }
  }

  @override
  Future<UserModel> getCurrentUser() async {
    final response = await dio.get('/auth/me');

    if (response.statusCode == 200) {
      return UserModel.fromJson(response.data['data']);
    } else if (response.statusCode == 401) {
      throw UnauthorizedException();
    } else {
      throw ServerException();
    }
  }

  @override
  Future<void> logout() async {
    await dio.post('/auth/logout');
  }

  @override
  Future<UserModel> register(String email, String password, String name) async {
    final response = await dio.post(
      '/auth/register',
      data: {
        'email': email,
        'password': password,
        'name': name,
      },
    );

    if (response.statusCode == 201) {
      return UserModel.fromJson(response.data['data']);
    } else {
      throw ServerException('Registration failed');
    }
  }
}

// data/datasources/auth_local_data_source.dart
abstract class AuthLocalDataSource {
  Future<UserModel> getCachedUser();
  Future<void> cacheUser(UserModel user);
  Future<String?> getToken();
  Future<void> cacheToken(String token);
  Future<void> clearCache();
}

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final SharedPreferences sharedPreferences;

  static const String cachedUserKey = 'CACHED_USER';
  static const String tokenKey = 'AUTH_TOKEN';

  AuthLocalDataSourceImpl({required this.sharedPreferences});

  @override
  Future<UserModel> getCachedUser() {
    final jsonString = sharedPreferences.getString(cachedUserKey);
    if (jsonString == null) {
      throw CacheException('No cached user');
    }
    return Future.value(UserModel.fromJson(json.decode(jsonString)));
  }

  @override
  Future<void> cacheUser(UserModel user) {
    return sharedPreferences.setString(
      cachedUserKey,
      json.encode(user.toJson()),
    );
  }

  @override
  Future<String?> getToken() {
    return Future.value(sharedPreferences.getString(tokenKey));
  }

  @override
  Future<void> cacheToken(String token) {
    return sharedPreferences.setString(tokenKey, token);
  }

  @override
  Future<void> clearCache() async {
    await sharedPreferences.remove(cachedUserKey);
    await sharedPreferences.remove(tokenKey);
  }
}
```

**6. Dependency Injection (Wiring Everything Together):**
```dart
// injection_container.dart
final sl = GetIt.instance;

Future<void> init() async {
  // ===== Features - Auth =====

  // Bloc
  sl.registerFactory(
    () => AuthBloc(loginUser: sl()),
  );

  // Use cases
  sl.registerLazySingleton(() => LoginUser(sl()));

  // Repository
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data sources
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(dio: sl()),
  );

  sl.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSourceImpl(sharedPreferences: sl()),
  );

  // ===== Core =====

  sl.registerLazySingleton<NetworkInfo>(
    () => NetworkInfoImpl(sl()),
  );

  // ===== External =====

  sl.registerLazySingleton(() => Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com/v1',
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
    ),
  ));

  final sharedPreferences = await SharedPreferences.getInstance();
  sl.registerLazySingleton(() => sharedPreferences);

  sl.registerLazySingleton(() => InternetConnectionChecker());
}
```

**7. Usage in UI:**
```dart
// presentation/pages/login_page.dart
class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: BlocProvider(
        // Dependency injection provides the BLoC with all its dependencies
        create: (context) => sl<AuthBloc>(),
        child: const LoginForm(),
      ),
    );
  }
}

class LoginForm extends StatefulWidget {
  const LoginForm({Key? key}) : super(key: key);

  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthBloc, AuthState>(
      listener: (context, state) {
        if (state is AuthSuccess) {
          Navigator.pushReplacementNamed(context, '/home');
        } else if (state is AuthError) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.message)),
          );
        }
      },
      child: BlocBuilder<AuthBloc, AuthState>(
        builder: (context, state) {
          if (state is AuthLoading) {
            return const Center(child: CircularProgressIndicator());
          }

          return Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                TextField(
                  controller: _emailController,
                  decoration: const InputDecoration(labelText: 'Email'),
                ),
                TextField(
                  controller: _passwordController,
                  decoration: const InputDecoration(labelText: 'Password'),
                  obscureText: true,
                ),
                const SizedBox(height: 20),
                ElevatedButton(
                  onPressed: () {
                    // UI triggers event → BLoC → Use Case → Repository → Data Source
                    context.read<AuthBloc>().add(
                      LoginEvent(
                        email: _emailController.text,
                        password: _passwordController.text,
                      ),
                    );
                  },
                  child: const Text('Login'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }
}
```

**Communication Flow Summary:**

1. **User Action** → UI Widget
2. **UI Widget** → BLoC/Controller (Presentation)
3. **BLoC/Controller** → Use Case (Domain)
4. **Use Case** → Repository Interface (Domain)
5. **Repository Implementation** (Data) implements Interface
6. **Repository** → Data Source (Data)
7. **Data Source** → External API/Database
8. **Response flows back** through the same chain
9. **BLoC/Controller** updates State
10. **UI Widget** rebuilds based on new State

**Key Points:**
- Presentation depends on Domain
- Data depends on Domain
- Domain depends on nothing
- Communication is through interfaces (abstractions)
- Dependency Injection wires everything together
- Each layer only knows about the layer directly inside it

---

### 13. **What is the difference between Models and Entities in Clean Architecture?**

**Entities** (Domain Layer) represent pure business objects, while **Models** (Data Layer) are data transfer objects that handle serialization.

**Comparison:**

| Aspect | Entity (Domain) | Model (Data) |
|--------|----------------|--------------|
| **Location** | domain/entities/ | data/models/ |
| **Purpose** | Business logic | Data transfer & serialization |
| **Dependencies** | None (pure Dart) | May use json_annotation, Hive, etc. |
| **Serialization** | No | Yes (toJson/fromJson) |
| **Mutability** | Usually immutable | Usually immutable |
| **Business Logic** | Yes | No |

**Example:**

**Entity (Domain Layer):**
```dart
// domain/entities/user.dart
class User {
  final String id;
  final String name;
  final String email;
  final DateTime dateOfBirth;
  final UserRole role;
  final bool isActive;

  const User({
    required this.id,
    required this.name,
    required this.email,
    required this.dateOfBirth,
    required this.role,
    required this.isActive,
  });

  // Business logic methods
  int get age {
    final now = DateTime.now();
    int age = now.year - dateOfBirth.year;
    if (now.month < dateOfBirth.month ||
        (now.month == dateOfBirth.month && now.day < dateOfBirth.day)) {
      age--;
    }
    return age;
  }

  bool get isAdult => age >= 18;

  bool get canAccessAdminPanel => role == UserRole.admin && isActive;

  bool get canMakePurchase => isActive && isAdult;

  User copyWith({
    String? name,
    String? email,
    bool? isActive,
    UserRole? role,
  }) {
    return User(
      id: id,
      name: name ?? this.name,
      email: email ?? this.email,
      dateOfBirth: dateOfBirth,
      role: role ?? this.role,
      isActive: isActive ?? this.isActive,
    );
  }

  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      other is User &&
          runtimeType == other.runtimeType &&
          id == other.id;

  @override
  int get hashCode => id.hashCode;
}

enum UserRole {
  user,
  admin,
  moderator,
}
```

**Model (Data Layer):**
```dart
// data/models/user_model.dart
import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/user.dart';

part 'user_model.g.dart';

@JsonSerializable()
class UserModel extends User {
  // Additional fields for API response that we don't need in domain
  @JsonKey(name: 'created_at')
  final String? createdAt;

  @JsonKey(name: 'updated_at')
  final String? updatedAt;

  const UserModel({
    required super.id,
    required super.name,
    required super.email,
    required super.dateOfBirth,
    required super.role,
    required super.isActive,
    this.createdAt,
    this.updatedAt,
  });

  // Factory constructor for JSON deserialization
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      dateOfBirth: DateTime.parse(json['date_of_birth'] as String),
      role: _roleFromString(json['role'] as String),
      isActive: json['is_active'] as bool? ?? true,
      createdAt: json['created_at'] as String?,
      updatedAt: json['updated_at'] as String?,
    );
  }

  // JSON serialization
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'date_of_birth': dateOfBirth.toIso8601String(),
      'role': _roleToString(role),
      'is_active': isActive,
      if (createdAt != null) 'created_at': createdAt,
      if (updatedAt != null) 'updated_at': updatedAt,
    };
  }

  // Convert from Entity to Model (for sending to API)
  factory UserModel.fromEntity(User user) {
    return UserModel(
      id: user.id,
      name: user.name,
      email: user.email,
      dateOfBirth: user.dateOfBirth,
      role: user.role,
      isActive: user.isActive,
    );
  }

  // Convert to Entity (already done by inheritance)
  User toEntity() => this;

  // Helper methods for enum conversion
  static UserRole _roleFromString(String role) {
    switch (role.toLowerCase()) {
      case 'admin':
        return UserRole.admin;
      case 'moderator':
        return UserRole.moderator;
      default:
        return UserRole.user;
    }
  }

  static String _roleToString(UserRole role) {
    switch (role) {
      case UserRole.admin:
        return 'admin';
      case UserRole.moderator:
        return 'moderator';
      case UserRole.user:
        return 'user';
    }
  }

  // Hive adapter for local storage
  factory UserModel.fromHive(Map<dynamic, dynamic> map) {
    return UserModel(
      id: map['id'] as String,
      name: map['name'] as String,
      email: map['email'] as String,
      dateOfBirth: DateTime.parse(map['date_of_birth'] as String),
      role: _roleFromString(map['role'] as String),
      isActive: map['is_active'] as bool,
    );
  }

  Map<String, dynamic> toHive() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'date_of_birth': dateOfBirth.toIso8601String(),
      'role': _roleToString(role),
      'is_active': isActive,
    };
  }
}
```

**Why the Separation?**

**1. API Response Format differs from Business Needs:**
```dart
// API returns:
{
  "id": "123",
  "full_name": "John Doe",  // API uses "full_name"
  "email_address": "john@example.com",  // API uses "email_address"
  "birth_date": "1990-01-15",  // String format
  "account_type": "premium",  // API-specific field
  "created_timestamp": "2024-01-01T00:00:00Z",  // We don't need in domain
  "last_login": "2024-12-04T10:30:00Z",  // We don't need in domain
}

// Model handles API structure
class UserModel extends User {
  @JsonKey(name: 'full_name')
  final String name;

  @JsonKey(name: 'email_address')
  final String email;

  @JsonKey(name: 'birth_date')
  final DateTime dateOfBirth;

  @JsonKey(name: 'account_type')
  final String? accountType;  // API-specific, not in Entity

  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
}

// Entity is clean and focused on business
class User {
  final String name;  // Simple name
  final String email;  // Simple email
  final DateTime dateOfBirth;  // Already parsed
  // No API-specific fields
}
```

**2. Multiple Data Sources, One Entity:**
```dart
// Remote API Model
class UserModelFromAPI extends User {
  factory UserModelFromAPI.fromJson(Map<String, dynamic> json) {
    return UserModelFromAPI(
      id: json['id'],
      name: json['name'],
      email: json['email'],
      // ... API-specific parsing
    );
  }
}

// Local Database Model
class UserModelFromDB extends User {
  factory UserModelFromDB.fromHive(Map<dynamic, dynamic> map) {
    return UserModelFromDB(
      id: map['id'],
      name: map['name'],
      email: map['email'],
      // ... DB-specific parsing
    );
  }
}

// Both convert to the same Entity
// Business logic doesn't care where data came from
```

**3. Business Logic Independence:**
```dart
// Domain layer doesn't care about JSON, Hive, etc.
class ValidateUserAge {
  Either<Failure, void> call(User user) {
    // Pure business logic
    if (!user.isAdult) {
      return Left(ValidationFailure('User must be 18 or older'));
    }
    return const Right(null);
  }
}

// Can test without any serialization concerns
test('should return failure when user is under 18', () {
  final user = User(
    id: '1',
    name: 'Test User',
    email: 'test@test.com',
    dateOfBirth: DateTime(2010, 1, 1),  // 14 years old
    role: UserRole.user,
    isActive: true,
  );

  final validator = ValidateUserAge();
  final result = validator(user);

  expect(result, isA<Left>());
});
```

**4. Change Isolation:**
```dart
// API changes from snake_case to camelCase
// BEFORE API:
{
  "user_id": "123",
  "user_name": "John"
}

// AFTER API:
{
  "userId": "123",
  "userName": "John"
}

// Only Model changes, Entity and all business logic stays the same
class UserModel extends User {
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['userId'],  // Changed
      name: json['userName'],  // Changed
      // Rest of domain logic unchanged
    );
  }
}
```

**Best Practices:**

**1. Model extends Entity:**
```dart
// ✅ Good: Model extends Entity
class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    // Parsing logic
  }
}

// Can be used as Entity directly
User user = UserModel.fromJson(json);
```

**2. Keep Entity Pure:**
```dart
// ✅ Good: Entity has no dependencies
class User {
  final String id;
  final String name;

  int calculatePoints() {
    // Pure business logic
  }
}

// ❌ Bad: Entity with serialization
class User {
  final String id;
  final String name;

  factory User.fromJson(Map<String, dynamic> json) {
    // NO! This couples entity to JSON
  }
}
```

**3. Conversion Methods:**
```dart
// Model provides conversion
class UserModel extends User {
  // From JSON to Model
  factory UserModel.fromJson(Map<String, dynamic> json) {...}

  // From Entity to Model
  factory UserModel.fromEntity(User entity) {...}

  // To JSON
  Map<String, dynamic> toJson() {...}

  // To Entity (already an Entity through inheritance)
  User toEntity() => this;
}
```

**Summary:**
- **Entity**: Business concepts, pure logic, no serialization
- **Model**: Data transfer, serialization, API-specific fields
- **Model extends Entity**: Can be used as Entity
- **Separation**: Protects business logic from external changes

---

### 14. **How do you structure a Flutter project using Clean Architecture with feature-first approach?**

The feature-first approach organizes code by features/modules rather than by layer types. Each feature contains its own layers.

**Folder Structure:**
```
lib/
├── core/
│   ├── error/
│   │   ├── exceptions.dart
│   │   └── failures.dart
│   ├── network/
│   │   ├── network_info.dart
│   │   └── dio_client.dart
│   ├── usecases/
│   │   └── usecase.dart
│   └── utils/
│       ├── constants.dart
│       └── input_converter.dart
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   │   ├── auth_local_data_source.dart
│   │   │   │   └── auth_remote_data_source.dart
│   │   │   ├── models/
│   │   │   │   └── user_model.dart
│   │   │   └── repositories/
│   │   │       └── auth_repository_impl.dart
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   │   └── user.dart
│   │   │   ├── repositories/
│   │   │   │   └── auth_repository.dart
│   │   │   └── usecases/
│   │   │       ├── login_user.dart
│   │   │       ├── logout_user.dart
│   │   │       └── register_user.dart
│   │   └── presentation/
│   │       ├── bloc/
│   │       │   ├── auth_bloc.dart
│   │       │   ├── auth_event.dart
│   │       │   └── auth_state.dart
│   │       ├── pages/
│   │       │   ├── login_page.dart
│   │       │   └── register_page.dart
│   │       └── widgets/
│   │           ├── login_form.dart
│   │           └── social_login_buttons.dart
│   ├── products/
│   │   ├── data/
│   │   │   ├── datasources/
│   │   │   ├── models/
│   │   │   └── repositories/
│   │   ├── domain/
│   │   │   ├── entities/
│   │   │   ├── repositories/
│   │   │   └── usecases/
│   │   └── presentation/
│   │       ├── bloc/
│   │       ├── pages/
│   │       └── widgets/
│   ├── cart/
│   │   └── ...
│   └── orders/
│       └── ...
├── injection_container.dart
└── main.dart
```

**Example Implementation:**

**Core Layer:**
```dart
// core/usecases/usecase.dart
import 'package:dartz/dartz.dart';
import '../error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {}

// core/error/failures.dart
abstract class Failure {
  final String message;
  const Failure(this.message);
}

class ServerFailure extends Failure {
  const ServerFailure([super.message = 'Server error']);
}

class NetworkFailure extends Failure {
  const NetworkFailure([super.message = 'No internet connection']);
}

// core/error/exceptions.dart
class ServerException implements Exception {}
class CacheException implements Exception {}
class NetworkException implements Exception {}

// core/network/network_info.dart
abstract class NetworkInfo {
  Future<bool> get isConnected;
}

class NetworkInfoImpl implements NetworkInfo {
  final InternetConnectionChecker connectionChecker;

  NetworkInfoImpl(this.connectionChecker);

  @override
  Future<bool> get isConnected => connectionChecker.hasConnection;
}
```

**Feature: Authentication**
```dart
// features/authentication/domain/entities/user.dart
class User {
  final String id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });
}

// features/authentication/domain/repositories/auth_repository.dart
abstract class AuthRepository {
  Future<Either<Failure, User>> login(String email, String password);
  Future<Either<Failure, User>> register(String email, String password, String name);
  Future<Either<Failure, void>> logout();
}

// features/authentication/domain/usecases/login_user.dart
class LoginUser implements UseCase<User, LoginParams> {
  final AuthRepository repository;

  LoginUser(this.repository);

  @override
  Future<Either<Failure, User>> call(LoginParams params) async {
    return await repository.login(params.email, params.password);
  }
}

class LoginParams {
  final String email;
  final String password;

  LoginParams({required this.email, required this.password});
}

// features/authentication/data/models/user_model.dart
class UserModel extends User {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}

// features/authentication/data/datasources/auth_remote_data_source.dart
abstract class AuthRemoteDataSource {
  Future<UserModel> login(String email, String password);
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSourceImpl({required this.dio});

  @override
  Future<UserModel> login(String email, String password) async {
    final response = await dio.post(
      '/auth/login',
      data: {'email': email, 'password': password},
    );

    if (response.statusCode == 200) {
      return UserModel.fromJson(response.data);
    } else {
      throw ServerException();
    }
  }
}

// features/authentication/data/repositories/auth_repository_impl.dart
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;
  final NetworkInfo networkInfo;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
    required this.networkInfo,
  });

  @override
  Future<Either<Failure, User>> login(String email, String password) async {
    if (!await networkInfo.isConnected) {
      return const Left(NetworkFailure());
    }

    try {
      final user = await remoteDataSource.login(email, password);
      await localDataSource.cacheUser(user);
      return Right(user);
    } on ServerException {
      return const Left(ServerFailure());
    }
  }

  @override
  Future<Either<Failure, User>> register(String email, String password, String name) async {
    // Implementation
    throw UnimplementedError();
  }

  @override
  Future<Either<Failure, void>> logout() async {
    // Implementation
    throw UnimplementedError();
  }
}

// features/authentication/presentation/bloc/auth_bloc.dart
class AuthBloc extends Bloc<AuthEvent, AuthState> {
  final LoginUser loginUser;
  final LogoutUser logoutUser;

  AuthBloc({
    required this.loginUser,
    required this.logoutUser,
  }) : super(AuthInitial()) {
    on<LoginEvent>(_onLogin);
    on<LogoutEvent>(_onLogout);
  }

  Future<void> _onLogin(LoginEvent event, Emitter<AuthState> emit) async {
    emit(AuthLoading());

    final result = await loginUser(
      LoginParams(email: event.email, password: event.password),
    );

    result.fold(
      (failure) => emit(AuthError(failure.message)),
      (user) => emit(AuthSuccess(user)),
    );
  }

  Future<void> _onLogout(LogoutEvent event, Emitter<AuthState> emit) async {
    // Implementation
  }
}

// features/authentication/presentation/pages/login_page.dart
class LoginPage extends StatelessWidget {
  const LoginPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: BlocProvider(
        create: (context) => sl<AuthBloc>(),
        child: const LoginForm(),
      ),
    );
  }
}
```

**Dependency Injection:**
```dart
// injection_container.dart
final sl = GetIt.instance;

Future<void> init() async {
  // ===== Features - Authentication =====

  // Bloc
  sl.registerFactory(() => AuthBloc(
    loginUser: sl(),
    logoutUser: sl(),
  ));

  // Use cases
  sl.registerLazySingleton(() => LoginUser(sl()));
  sl.registerLazySingleton(() => LogoutUser(sl()));

  // Repository
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(
      remoteDataSource: sl(),
      localDataSource: sl(),
      networkInfo: sl(),
    ),
  );

  // Data sources
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(dio: sl()),
  );

  sl.registerLazySingleton<AuthLocalDataSource>(
    () => AuthLocalDataSourceImpl(sharedPreferences: sl()),
  );

  // ===== Features - Products =====
  // Similar structure...

  // ===== Core =====
  sl.registerLazySingleton<NetworkInfo>(() => NetworkInfoImpl(sl()));

  // ===== External =====
  final sharedPreferences = await SharedPreferences.getInstance();
  sl.registerLazySingleton(() => sharedPreferences);

  sl.registerLazySingleton(() => Dio());
  sl.registerLazySingleton(() => InternetConnectionChecker());
}
```

**Benefits of Feature-First:**
- Easy to find all code related to a feature
- Better for large projects with many features
- Clear feature boundaries
- Easy to delete entire features
- Good for team collaboration (different teams work on different features)

---

### 15. **How do you structure a Flutter project using Clean Architecture with layer-first approach?**

The layer-first approach organizes code by layers (Data, Domain, Presentation) first, then by features within each layer.

**Folder Structure:**
```
lib/
├── data/
│   ├── datasources/
│   │   ├── auth/
│   │   │   ├── auth_local_data_source.dart
│   │   │   └── auth_remote_data_source.dart
│   │   ├── product/
│   │   │   ├── product_local_data_source.dart
│   │   │   └── product_remote_data_source.dart
│   │   └── cart/
│   │       └── cart_local_data_source.dart
│   ├── models/
│   │   ├── auth/
│   │   │   └── user_model.dart
│   │   ├── product/
│   │   │   └── product_model.dart
│   │   └── cart/
│   │       └── cart_item_model.dart
│   └── repositories/
│       ├── auth_repository_impl.dart
│       ├── product_repository_impl.dart
│       └── cart_repository_impl.dart
├── domain/
│   ├── entities/
│   │   ├── user.dart
│   │   ├── product.dart
│   │   └── cart_item.dart
│   ├── repositories/
│   │   ├── auth_repository.dart
│   │   ├── product_repository.dart
│   │   └── cart_repository.dart
│   └── usecases/
│       ├── auth/
│       │   ├── login_user.dart
│       │   ├── register_user.dart
│       │   └── logout_user.dart
│       ├── product/
│       │   ├── get_products.dart
│       │   ├── get_product_details.dart
│       │   └── search_products.dart
│       └── cart/
│           ├── add_to_cart.dart
│           ├── remove_from_cart.dart
│           └── get_cart_items.dart
├── presentation/
│   ├── bloc/
│   │   ├── auth/
│   │   │   ├── auth_bloc.dart
│   │   │   ├── auth_event.dart
│   │   │   └── auth_state.dart
│   │   ├── product/
│   │   │   ├── product_bloc.dart
│   │   │   ├── product_event.dart
│   │   │   └── product_state.dart
│   │   └── cart/
│   │       ├── cart_bloc.dart
│   │       ├── cart_event.dart
│   │       └── cart_state.dart
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── login_page.dart
│   │   │   └── register_page.dart
│   │   ├── product/
│   │   │   ├── product_list_page.dart
│   │   │   └── product_details_page.dart
│   │   └── cart/
│   │       └── cart_page.dart
│   └── widgets/
│       ├── auth/
│       │   └── login_form.dart
│       ├── product/
│       │   └── product_card.dart
│       └── common/
│           ├── loading_indicator.dart
│           └── error_widget.dart
├── core/
│   ├── error/
│   │   ├── failures.dart
│   │   └── exceptions.dart
│   ├── network/
│   │   └── network_info.dart
│   └── utils/
│       └── constants.dart
├── injection_container.dart
└── main.dart
```

**When to use Layer-First:**
- Smaller projects (< 10 features)
- When layers are more important than features
- When features share a lot of common entities
- Academic projects or learning Clean Architecture

**When to use Feature-First:**
- Larger projects (10+ features)
- When features are independent
- Better for modular architecture
- Production applications

**Hybrid Approach:**
```
lib/
├── features/
│   ├── authentication/
│   │   ├── data/
│   │   ├── domain/
│   │   └── presentation/
│   └── products/
│       ├── data/
│       ├── domain/
│       └── presentation/
├── shared/
│   ├── data/
│   │   └── datasources/
│   │       └── http_client.dart
│   ├── domain/
│   │   └── entities/
│   │       └── paginated_response.dart
│   └── presentation/
│       └── widgets/
│           └── custom_button.dart
└── core/
    ├── error/
    ├── network/
    └── utils/
```

---

### 16. **What should and shouldn't be included in each layer?**

**PRESENTATION LAYER**

**Should Include:**
```dart
// ✅ UI Components (Pages, Widgets)
class ProductListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Products')),
      body: ProductListView(),
    );
  }
}

// ✅ State Management (BLoC, GetX, Riverpod)
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  final GetProducts getProducts;

  ProductBloc({required this.getProducts}) : super(ProductInitial());
}

// ✅ Navigation Logic
void navigateToProductDetails(BuildContext context, Product product) {
  Navigator.push(
    context,
    MaterialPageRoute(
      builder: (_) => ProductDetailsPage(product: product),
    ),
  );
}

// ✅ Input Formatting
String formatPrice(double price) {
  return '\$${price.toStringAsFixed(2)}';
}

// ✅ UI Validators (format only)
String? validateEmailFormat(String? email) {
  if (email == null || email.isEmpty) {
    return 'Email is required';
  }
  if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email)) {
    return 'Enter a valid email format';
  }
  return null;
}

// ✅ Presentation Models (optional, for UI-specific data transformation)
class ProductPresentation {
  final Product product;

  ProductPresentation(this.product);

  String get formattedPrice => '\$${product.price.toStringAsFixed(2)}';
  String get stockStatus => product.inStock ? 'In Stock' : 'Out of Stock';
  Color get stockColor => product.inStock ? Colors.green : Colors.red;
}
```

**Should NOT Include:**
```dart
// ❌ Business Logic
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  // ❌ NO! Business validation belongs in Domain
  bool isProductExpensive(Product product) {
    return product.price > 100;
  }

  // ❌ NO! Business rules belong in Domain
  double calculateDiscount(Product product, User user) {
    if (user.isPremium) {
      return product.price * 0.8;
    }
    return product.price;
  }
}

// ❌ Direct API Calls
class ProductController extends GetxController {
  Future<void> loadProducts() async {
    // ❌ NO! API calls belong in Data layer
    final response = await http.get('https://api.example.com/products');
    // ...
  }
}

// ❌ Direct Database Access
class ProductBloc extends Bloc<ProductEvent, ProductState> {
  Future<void> loadProducts() async {
    // ❌ NO! Database access belongs in Data layer
    final box = await Hive.openBox<Product>('products');
    // ...
  }
}

// ❌ Business Validation
String? validateUserAge(int age) {
  // ❌ NO! Business validation belongs in Domain
  if (age < 18) {
    return 'Must be 18 or older to purchase';
  }
  return null;
}
```

---

**DOMAIN LAYER**

**Should Include:**
```dart
// ✅ Entities (Business Objects)
class Order {
  final String id;
  final List<OrderItem> items;
  final double subtotal;
  final double tax;
  final double shipping;

  const Order({
    required this.id,
    required this.items,
    required this.subtotal,
    required this.tax,
    required this.shipping,
  });

  // ✅ Business logic methods
  double get total => subtotal + tax + shipping;

  bool get canBeCancelled => status == OrderStatus.pending;
}

// ✅ Repository Interfaces
abstract class ProductRepository {
  Future<Either<Failure, List<Product>>> getProducts();
  Future<Either<Failure, Product>> getProductById(String id);
}

// ✅ Use Cases (Business Operations)
class CalculateOrderTotal {
  final OrderRepository repository;

  CalculateOrderTotal(this.repository);

  Future<Either<Failure, double>> call(CalculateOrderParams params) async {
    // ✅ Business logic
    double total = params.items.fold(
      0.0,
      (sum, item) => sum + (item.price * item.quantity),
    );

    // ✅ Business rules
    final tax = total * 0.1; // 10% tax
    final shipping = total >= 50 ? 0 : 5.99; // Free shipping over $50

    return Right(total + tax + shipping);
  }
}

// ✅ Business Validators
class OrderValidator {
  static Either<Failure, void> validate(List<OrderItem> items) {
    // ✅ Business validation
    if (items.isEmpty) {
      return Left(ValidationFailure('Order must have at least one item'));
    }

    for (final item in items) {
      if (item.quantity <= 0) {
        return Left(ValidationFailure('Quantity must be positive'));
      }
      if (item.quantity > 99) {
        return Left(ValidationFailure('Max quantity per item is 99'));
      }
    }

    return const Right(null);
  }
}

// ✅ Failures (Business Errors)
abstract class Failure {
  final String message;
  const Failure(this.message);
}

class PaymentFailure extends Failure {
  const PaymentFailure(super.message);
}

// ✅ Value Objects
class Email {
  final String value;

  Email._(this.value);

  static Either<Failure, Email> create(String input) {
    if (!RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(input)) {
      return Left(ValidationFailure('Invalid email'));
    }
    return Right(Email._(input));
  }
}
```

**Should NOT Include:**
```dart
// ❌ Flutter Dependencies
import 'package:flutter/material.dart';  // ❌ NO!

class User {
  final String id;
  final String name;

  // ❌ NO! Flutter-specific
  Color get statusColor => isActive ? Colors.green : Colors.red;
}

// ❌ Serialization Logic
class Product {
  final String id;
  final String name;

  // ❌ NO! JSON parsing belongs in Data layer
  factory Product.fromJson(Map<String, dynamic> json) {
    return Product(
      id: json['id'],
      name: json['name'],
    );
  }
}

// ❌ HTTP Client, Dio, etc.
class GetProducts {
  final Dio dio;  // ❌ NO! External dependency

  GetProducts(this.dio);
}

// ❌ Database Packages (Hive, Sqflite, etc.)
import 'package:hive/hive.dart';  // ❌ NO!

// ❌ Data Source Implementations
class GetProducts {
  Future<List<Product>> call() async {
    // ❌ NO! Fetching data belongs in Data layer
    final response = await http.get('api/products');
    // ...
  }
}

// ❌ UI Logic
class CalculatePrice {
  String call(double price) {
    // ❌ NO! Formatting for UI belongs in Presentation
    return '\$${price.toStringAsFixed(2)}';
  }
}
```

---

**DATA LAYER**

**Should Include:**
```dart
// ✅ Repository Implementations
class ProductRepositoryImpl implements ProductRepository {
  final ProductRemoteDataSource remoteDataSource;
  final ProductLocalDataSource localDataSource;

  ProductRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<Either<Failure, List<Product>>> getProducts() async {
    try {
      final products = await remoteDataSource.getProducts();
      await localDataSource.cacheProducts(products);
      return Right(products);
    } on ServerException {
      return const Left(ServerFailure());
    }
  }
}

// ✅ Data Sources
abstract class ProductRemoteDataSource {
  Future<List<ProductModel>> getProducts();
}

class ProductRemoteDataSourceImpl implements ProductRemoteDataSource {
  final Dio dio;

  ProductRemoteDataSourceImpl(this.dio);

  @override
  Future<List<ProductModel>> getProducts() async {
    final response = await dio.get('/products');
    return (response.data as List)
        .map((json) => ProductModel.fromJson(json))
        .toList();
  }
}

// ✅ Models with Serialization
class ProductModel extends Product {
  const ProductModel({
    required super.id,
    required super.name,
    required super.price,
  });

  factory ProductModel.fromJson(Map<String, dynamic> json) {
    return ProductModel(
      id: json['id'],
      name: json['name'],
      price: json['price'].toDouble(),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'price': price,
    };
  }
}

// ✅ Exceptions
class ServerException implements Exception {}
class CacheException implements Exception {}
class NetworkException implements Exception {}

// ✅ API Client Configuration
class DioClient {
  static Dio createDio() {
    return Dio(
      BaseOptions(
        baseUrl: 'https://api.example.com',
        connectTimeout: const Duration(seconds: 30),
      ),
    );
  }
}

// ✅ Caching Logic
class ProductLocalDataSourceImpl implements ProductLocalDataSource {
  final Box<ProductModel> productBox;

  ProductLocalDataSourceImpl(this.productBox);

  @override
  Future<void> cacheProducts(List<ProductModel> products) async {
    await productBox.clear();
    for (final product in products) {
      await productBox.put(product.id, product);
    }
  }
}
```

**Should NOT Include:**
```dart
// ❌ Business Logic
class ProductRepositoryImpl implements ProductRepository {
  @override
  Future<Either<Failure, List<Product>>> getProducts() async {
    final products = await remoteDataSource.getProducts();

    // ❌ NO! Business filtering belongs in Domain
    final filteredProducts = products.where((p) => p.price < 100).toList();

    return Right(filteredProducts);
  }
}

// ❌ UI Logic
class ProductModel extends Product {
  // ❌ NO! UI formatting belongs in Presentation
  String get formattedPrice => '\$${price.toStringAsFixed(2)}';
}

// ❌ BLoC, GetX, Riverpod
import 'package:flutter_bloc/flutter_bloc.dart';  // ❌ NO!

// ❌ Business Validation
class UserRepositoryImpl implements UserRepository {
  @override
  Future<Either<Failure, User>> createUser(User user) async {
    // ❌ NO! Business validation belongs in Domain (Use Case)
    if (user.age < 18) {
      return Left(ValidationFailure('Must be 18 or older'));
    }

    // Data layer should only handle data operations
    final userModel = await remoteDataSource.createUser(user);
    return Right(userModel);
  }
}

// ❌ Navigation
class ProductRepositoryImpl implements ProductRepository {
  @override
  Future<Either<Failure, Product>> getProduct(String id) async {
    final product = await remoteDataSource.getProduct(id);

    // ❌ NO! Navigation belongs in Presentation
    Navigator.push(context, MaterialPageRoute(...));

    return Right(product);
  }
}
```

**Summary Table:**

| Layer | Should Include | Should NOT Include |
|-------|----------------|-------------------|
| **Presentation** | UI, Widgets, State Management, Navigation, UI Formatting | Business Logic, API Calls, Database Access, Business Validation |
| **Domain** | Entities, Use Cases, Repository Interfaces, Business Logic, Business Validation | Flutter/UI, Serialization, HTTP/Database packages, Data Fetching |
| **Data** | Repository Implementations, Data Sources, Models, Serialization, Caching | Business Logic, UI Logic, State Management, Business Validation |

---

## Use Cases / Interactors

### 17. **What is a Use Case (or Interactor) in Clean Architecture?**

A Use Case represents a single business operation or user action. It encapsulates the business logic for that specific operation and orchestrates the flow between different repositories and services.

**Key Characteristics:**
- Represents one specific user action
- Contains business logic and rules
- Orchestrates data flow
- Independent of UI and frameworks
- Highly testable

**Basic Structure:**
```dart
// domain/usecases/get_user_profile.dart
class GetUserProfile {
  final UserRepository userRepository;

  GetUserProfile(this.userRepository);

  Future<Either<Failure, User>> call(String userId) async {
    // Business validation
    if (userId.isEmpty) {
      return const Left(ValidationFailure('User ID cannot be empty'));
    }

    // Call repository
    return await userRepository.getUserById(userId);
  }
}
```

**Real-World Example: Create Order**
```dart
// domain/usecases/create_order.dart
class CreateOrder {
  final OrderRepository orderRepository;
  final PaymentRepository paymentRepository;
  final InventoryRepository inventoryRepository;
  final NotificationRepository notificationRepository;

  CreateOrder({
    required this.orderRepository,
    required this.paymentRepository,
    required this.inventoryRepository,
    required this.notificationRepository,
  });

  Future<Either<Failure, Order>> call(CreateOrderParams params) async {
    // Step 1: Validate business rules
    final validation = _validateOrder(params);
    if (validation != null) {
      return Left(validation);
    }

    // Step 2: Check inventory
    for (final item in params.items) {
      final stockCheck = await inventoryRepository.checkStock(
        item.productId,
        item.quantity,
      );

      final hasStock = stockCheck.fold(
        (failure) => false,
        (available) => available,
      );

      if (!hasStock) {
        return Left(
          ValidationFailure('Product ${item.productName} is out of stock'),
        );
      }
    }

    // Step 3: Calculate totals (business logic)
    final subtotal = params.items.fold(
      0.0,
      (sum, item) => sum + (item.price * item.quantity),
    );

    // Business rule: Minimum order amount
    if (subtotal < 10.0) {
      return Left(ValidationFailure('Minimum order amount is \$10'));
    }

    // Business rule: Calculate tax
    final tax = subtotal * 0.1;

    // Business rule: Free shipping over $50
    final shipping = subtotal >= 50.0 ? 0.0 : 5.99;

    // Step 4: Create order
    final orderResult = await orderRepository.createOrder(
      OrderCreateData(
        userId: params.userId,
        items: params.items,
        subtotal: subtotal,
        tax: tax,
        shipping: shipping,
        shippingAddress: params.shippingAddress,
      ),
    );

    return orderResult.fold(
      (failure) => Left(failure),
      (order) async {
        // Step 5: Process payment
        final paymentResult = await paymentRepository.processPayment(
          PaymentParams(
            orderId: order.id,
            amount: order.total,
            paymentMethodId: params.paymentMethodId,
          ),
        );

        return paymentResult.fold(
          (failure) async {
            // Payment failed, cancel order
            await orderRepository.cancelOrder(order.id);
            return Left(PaymentFailure('Payment failed'));
          },
          (payment) async {
            // Step 6: Update inventory
            for (final item in params.items) {
              await inventoryRepository.reduceStock(
                item.productId,
                item.quantity,
              );
            }

            // Step 7: Send notification
            await notificationRepository.sendOrderConfirmation(
              userId: params.userId,
              orderId: order.id,
            );

            return Right(order);
          },
        );
      },
    );
  }

  Failure? _validateOrder(CreateOrderParams params) {
    // Business validation
    if (params.items.isEmpty) {
      return ValidationFailure('Order must contain at least one item');
    }

    if (params.shippingAddress.trim().isEmpty) {
      return ValidationFailure('Shipping address is required');
    }

    for (final item in params.items) {
      if (item.quantity <= 0) {
        return ValidationFailure('Item quantity must be positive');
      }

      if (item.quantity > 99) {
        return ValidationFailure('Maximum quantity per item is 99');
      }
    }

    return null;
  }
}

class CreateOrderParams {
  final String userId;
  final List<OrderItem> items;
  final String shippingAddress;
  final String paymentMethodId;

  CreateOrderParams({
    required this.userId,
    required this.items,
    required this.shippingAddress,
    required this.paymentMethodId,
  });
}
```

**Why Use Cases?**

**1. Single Responsibility:**
```dart
// Each use case does ONE thing

// ✅ Good: Separate use cases
class LoginUser {
  Future<Either<Failure, User>> call(LoginParams params) {
    // Only handles login
  }
}

class RegisterUser {
  Future<Either<Failure, User>> call(RegisterParams params) {
    // Only handles registration
  }
}

class ResetPassword {
  Future<Either<Failure, void>> call(String email) {
    // Only handles password reset
  }
}

// ❌ Bad: One use case doing multiple things
class AuthUseCase {
  Future<Either<Failure, User>> login(...) {}
  Future<Either<Failure, User>> register(...) {}
  Future<Either<Failure, void>> resetPassword(...) {}
  Future<Either<Failure, void>> logout(...) {}
  // Too many responsibilities!
}
```

**2. Business Logic Centralization:**
```dart
// All business rules for "adding to cart" in one place
class AddToCart {
  final CartRepository cartRepository;
  final ProductRepository productRepository;

  AddToCart({
    required this.cartRepository,
    required this.productRepository,
  });

  Future<Either<Failure, Cart>> call(AddToCartParams params) async {
    // Business rule: Check if product exists and is available
    final productResult = await productRepository.getProductById(
      params.productId,
    );

    return productResult.fold(
      (failure) => Left(failure),
      (product) async {
        // Business rule: Check stock
        if (!product.inStock) {
          return Left(ValidationFailure('Product is out of stock'));
        }

        // Business rule: Maximum quantity
        if (params.quantity > 10) {
          return Left(ValidationFailure('Maximum 10 items per product'));
        }

        // Business rule: Check if item already in cart
        final cartResult = await cartRepository.getCart(params.userId);

        return cartResult.fold(
          (failure) => Left(failure),
          (cart) async {
            final existingItem = cart.items.firstWhere(
              (item) => item.productId == params.productId,
              orElse: () => null as CartItem,
            );

            if (existingItem != null) {
              // Business rule: Update quantity instead of adding duplicate
              final newQuantity = existingItem.quantity + params.quantity;

              if (newQuantity > 10) {
                return Left(
                  ValidationFailure('Total quantity exceeds maximum (10)'),
                );
              }

              return await cartRepository.updateItemQuantity(
                params.userId,
                params.productId,
                newQuantity,
              );
            } else {
              // Add new item
              return await cartRepository.addItem(
                params.userId,
                CartItem(
                  productId: params.productId,
                  productName: product.name,
                  quantity: params.quantity,
                  price: product.price,
                ),
              );
            }
          },
        );
      },
    );
  }
}

class AddToCartParams {
  final String userId;
  final String productId;
  final int quantity;

  AddToCartParams({
    required this.userId,
    required this.productId,
    required this.quantity,
  });
}
```

**3. Testability:**
```dart
// Easy to test use cases in isolation
void main() {
  late AddToCart addToCart;
  late MockCartRepository mockCartRepository;
  late MockProductRepository mockProductRepository;

  setUp(() {
    mockCartRepository = MockCartRepository();
    mockProductRepository = MockProductRepository();
    addToCart = AddToCart(
      cartRepository: mockCartRepository,
      productRepository: mockProductRepository,
    );
  });

  group('AddToCart', () {
    test('should add item to cart when product is available', () async {
      // Arrange
      final testProduct = Product(
        id: '1',
        name: 'Test Product',
        price: 29.99,
        inStock: true,
      );

      final testCart = Cart(userId: 'user1', items: []);

      when(() => mockProductRepository.getProductById('1'))
          .thenAnswer((_) async => Right(testProduct));

      when(() => mockCartRepository.getCart('user1'))
          .thenAnswer((_) async => Right(testCart));

      when(() => mockCartRepository.addItem('user1', any()))
          .thenAnswer((_) async => Right(testCart));

      // Act
      final result = await addToCart(
        AddToCartParams(
          userId: 'user1',
          productId: '1',
          quantity: 2,
        ),
      );

      // Assert
      expect(result, isA<Right>());
      verify(() => mockProductRepository.getProductById('1')).called(1);
      verify(() => mockCartRepository.addItem('user1', any())).called(1);
    });

    test('should return failure when product is out of stock', () async {
      // Arrange
      final testProduct = Product(
        id: '1',
        name: 'Test Product',
        price: 29.99,
        inStock: false,  // Out of stock
      );

      when(() => mockProductRepository.getProductById('1'))
          .thenAnswer((_) async => Right(testProduct));

      // Act
      final result = await addToCart(
        AddToCartParams(
          userId: 'user1',
          productId: '1',
          quantity: 2,
        ),
      );

      // Assert
      expect(result, isA<Left>());
      final failure = (result as Left).value;
      expect(failure, isA<ValidationFailure>());
      expect(failure.message, 'Product is out of stock');

      // Verify repository was never called to add item
      verifyNever(() => mockCartRepository.addItem(any(), any()));
    });

    test('should return failure when quantity exceeds maximum', () async {
      // Act
      final result = await addToCart(
        AddToCartParams(
          userId: 'user1',
          productId: '1',
          quantity: 15,  // Exceeds max of 10
        ),
      );

      // Assert
      expect(result, isA<Left>());
      final failure = (result as Left).value;
      expect(failure.message, contains('Maximum 10 items'));

      // Verify product repository was never called
      verifyNever(() => mockProductRepository.getProductById(any()));
    });
  });
}
```

**4. Reusability:**
```dart
// Same use case used in different parts of the app

// In Product Details Page
class ProductDetailsBloc extends Bloc<ProductDetailsEvent, ProductDetailsState> {
  final AddToCart addToCart;  // Use case

  ProductDetailsBloc({required this.addToCart}) : super(ProductDetailsInitial());
}

// In Quick Add Widget
class QuickAddController extends GetxController {
  final AddToCart addToCart;  // Same use case

  QuickAddController({required this.addToCart});
}

// In Cart Page (when updating quantity)
class CartBloc extends Bloc<CartEvent, CartState> {
  final AddToCart addToCart;  // Same use case
  final RemoveFromCart removeFromCart;

  CartBloc({
    required this.addToCart,
    required this.removeFromCart,
  }) : super(CartInitial());
}
```

**Use Case Best Practices:**

1. **One public method**: Usually `call()` or `execute()`
2. **Clear naming**: Use verb + noun (GetUser, CreateOrder, ValidateEmail)
3. **Parameters object**: For complex inputs
4. **Either return type**: For error handling
5. **No UI dependencies**: Pure business logic
6. **Dependency injection**: Inject repositories via constructor

---

### 18. **How do you implement a Use Case in Flutter?**

**Basic Use Case Pattern:**

**1. Simple Use Case (No Parameters):**
```dart
// domain/usecases/get_current_user.dart
class GetCurrentUser {
  final UserRepository repository;

  GetCurrentUser(this.repository);

  Future<Either<Failure, User>> call() {
    return repository.getCurrentUser();
  }
}

// Usage in BLoC
class UserBloc extends Bloc<UserEvent, UserState> {
  final GetCurrentUser getCurrentUser;

  UserBloc({required this.getCurrentUser}) : super(UserInitial()) {
    on<LoadCurrentUserEvent>(_onLoadCurrentUser);
  }

  Future<void> _onLoadCurrentUser(
    LoadCurrentUserEvent event,
    Emitter<UserState> emit,
  ) async {
    emit(UserLoading());
    final result = await getCurrentUser();
    result.fold(
      (failure) => emit(UserError(failure.message)),
      (user) => emit(UserLoaded(user)),
    );
  }
}
```

**2. Use Case with Simple Parameter:**
```dart
// domain/usecases/get_product_by_id.dart
class GetProductById {
  final ProductRepository repository;

  GetProductById(this.repository);

  Future<Either<Failure, Product>> call(String productId) async {
    // Business validation
    if (productId.isEmpty) {
      return const Left(ValidationFailure('Product ID is required'));
    }

    return await repository.getProductById(productId);
  }
}

// Usage
final result = await getProductById('product-123');
```

**3. Use Case with Parameters Class:**
```dart
// domain/usecases/search_products.dart
class SearchProducts {
  final ProductRepository repository;

  SearchProducts(this.repository);

  Future<Either<Failure, List<Product>>> call(SearchProductsParams params) async {
    // Business validation
    if (params.query.trim().isEmpty) {
      return const Left(ValidationFailure('Search query cannot be empty'));
    }

    if (params.query.length < 3) {
      return const Left(
        ValidationFailure('Search query must be at least 3 characters'),
      );
    }

    // Business logic: Filter by category if provided
    if (params.category != null) {
      return await repository.searchProductsByCategory(
        params.query,
        params.category!,
      );
    }

    return await repository.searchProducts(params.query);
  }
}

class SearchProductsParams {
  final String query;
  final String? category;
  final double? minPrice;
  final double? maxPrice;
  final ProductSortOption sortBy;

  SearchProductsParams({
    required this.query,
    this.category,
    this.minPrice,
    this.maxPrice,
    this.sortBy = ProductSortOption.relevance,
  });
}

enum ProductSortOption {
  relevance,
  priceLowToHigh,
  priceHighToLow,
  nameAZ,
  nameZA,
}
```

**4. Use Case with Base Class:**
```dart
// core/usecases/usecase.dart
import 'package:dartz/dartz.dart';
import '../error/failures.dart';

abstract class UseCase<Type, Params> {
  Future<Either<Failure, Type>> call(Params params);
}

class NoParams {}

// Implementing specific use case
// domain/usecases/get_user.dart
class GetUser implements UseCase<User, GetUserParams> {
  final UserRepository repository;

  GetUser(this.repository);

  @override
  Future<Either<Failure, User>> call(GetUserParams params) async {
    if (params.userId.isEmpty) {
      return const Left(ValidationFailure('User ID is required'));
    }

    return await repository.getUserById(params.userId);
  }
}

class GetUserParams {
  final String userId;

  GetUserParams({required this.userId});
}

// Use case with no parameters
class GetAllProducts implements UseCase<List<Product>, NoParams> {
  final ProductRepository repository;

  GetAllProducts(this.repository);

  @override
  Future<Either<Failure, List<Product>>> call(NoParams params) {
    return repository.getAllProducts();
  }
}

// Usage
final user = await getUser(GetUserParams(userId: '123'));
final products = await getAllProducts(NoParams());
```

**5. Complex Use Case with Multiple Dependencies:**
```dart
// domain/usecases/checkout_cart.dart
class CheckoutCart {
  final CartRepository cartRepository;
  final OrderRepository orderRepository;
  final PaymentRepository paymentRepository;
  final InventoryRepository inventoryRepository;
  final UserRepository userRepository;
  final EmailRepository emailRepository;

  CheckoutCart({
    required this.cartRepository,
    required this.orderRepository,
    required this.paymentRepository,
    required this.inventoryRepository,
    required this.userRepository,
    required this.emailRepository,
  });

  Future<Either<Failure, CheckoutResult>> call(
    CheckoutCartParams params,
  ) async {
    // Step 1: Get user
    final userResult = await userRepository.getUserById(params.userId);
    if (userResult.isLeft()) {
      return Left((userResult as Left).value);
    }
    final user = (userResult as Right).value;

    // Step 2: Get cart
    final cartResult = await cartRepository.getCart(params.userId);
    if (cartResult.isLeft()) {
      return Left((cartResult as Left).value);
    }
    final cart = (cartResult as Right).value;

    // Business rule: Cart must not be empty
    if (cart.items.isEmpty) {
      return const Left(ValidationFailure('Cart is empty'));
    }

    // Step 3: Verify inventory for all items
    for (final item in cart.items) {
      final stockResult = await inventoryRepository.checkStock(
        item.productId,
        item.quantity,
      );

      final hasStock = stockResult.fold(
        (failure) => false,
        (available) => available,
      );

      if (!hasStock) {
        return Left(
          ValidationFailure('${item.productName} is no longer available'),
        );
      }
    }

    // Step 4: Calculate totals
    final subtotal = cart.totalPrice;
    final tax = subtotal * 0.1;
    final shipping = _calculateShipping(subtotal, user);
    final total = subtotal + tax + shipping;

    // Business rule: Check if user can make purchase
    if (user.accountStatus != AccountStatus.active) {
      return const Left(
        ValidationFailure('Account is not active. Please contact support.'),
      );
    }

    // Step 5: Create order
    final orderResult = await orderRepository.createOrder(
      CreateOrderData(
        userId: params.userId,
        items: cart.items,
        subtotal: subtotal,
        tax: tax,
        shipping: shipping,
        shippingAddress: params.shippingAddress,
        billingAddress: params.billingAddress,
      ),
    );

    return orderResult.fold(
      (failure) => Left(failure),
      (order) async {
        // Step 6: Process payment
        final paymentResult = await paymentRepository.processPayment(
          PaymentParams(
            orderId: order.id,
            amount: total,
            paymentMethodId: params.paymentMethodId,
            customerId: user.id,
          ),
        );

        return paymentResult.fold(
          (failure) async {
            // Payment failed, cancel order
            await orderRepository.cancelOrder(order.id);
            return Left(PaymentFailure('Payment processing failed'));
          },
          (payment) async {
            // Step 7: Update inventory
            for (final item in cart.items) {
              await inventoryRepository.reduceStock(
                item.productId,
                item.quantity,
              );
            }

            // Step 8: Clear cart
            await cartRepository.clearCart(params.userId);

            // Step 9: Send confirmation email
            await emailRepository.sendOrderConfirmation(
              email: user.email,
              orderId: order.id,
              orderDetails: order,
            );

            // Return result
            return Right(
              CheckoutResult(
                order: order,
                payment: payment,
                message: 'Order placed successfully!',
              ),
            );
          },
        );
      },
    );
  }

  double _calculateShipping(double subtotal, User user) {
    // Business rule: Free shipping for premium users
    if (user.isPremium) {
      return 0.0;
    }

    // Business rule: Free shipping over $50
    if (subtotal >= 50.0) {
      return 0.0;
    }

    // Business rule: Express shipping
    return 5.99;
  }
}

class CheckoutCartParams {
  final String userId;
  final String shippingAddress;
  final String billingAddress;
  final String paymentMethodId;

  CheckoutCartParams({
    required this.userId,
    required this.shippingAddress,
    required this.billingAddress,
    required this.paymentMethodId,
  });
}

class CheckoutResult {
  final Order order;
  final Payment payment;
  final String message;

  CheckoutResult({
    required this.order,
    required this.payment,
    required this.message,
  });
}
```

**6. Use Case with Stream Output:**
```dart
// domain/usecases/watch_cart_updates.dart
class WatchCartUpdates {
  final CartRepository repository;

  WatchCartUpdates(this.repository);

  Stream<Either<Failure, Cart>> call(String userId) {
    if (userId.isEmpty) {
      return Stream.value(
        const Left(ValidationFailure('User ID is required')),
      );
    }

    return repository.watchCart(userId);
  }
}

// Usage in BLoC
class CartBloc extends Bloc<CartEvent, CartState> {
  final WatchCartUpdates watchCartUpdates;
  StreamSubscription<Either<Failure, Cart>>? _cartSubscription;

  CartBloc({required this.watchCartUpdates}) : super(CartInitial()) {
    on<StartWatchingCart>(_onStartWatchingCart);
    on<CartUpdated>(_onCartUpdated);
  }

  Future<void> _onStartWatchingCart(
    StartWatchingCart event,
    Emitter<CartState> emit,
  ) async {
    await _cartSubscription?.cancel();

    _cartSubscription = watchCartUpdates(event.userId).listen(
      (result) {
        result.fold(
          (failure) => add(CartUpdateFailed(failure)),
          (cart) => add(CartUpdated(cart)),
        );
      },
    );
  }

  Future<void> _onCartUpdated(
    CartUpdated event,
    Emitter<CartState> emit,
  ) async {
    emit(CartLoaded(event.cart));
  }

  @override
  Future<void> close() {
    _cartSubscription?.cancel();
    return super.close();
  }
}
```

**7. Use Case Testing:**
```dart
// test/domain/usecases/get_product_by_id_test.dart
void main() {
  late GetProductById getProductById;
  late MockProductRepository mockRepository;

  setUp(() {
    mockRepository = MockProductRepository();
    getProductById = GetProductById(mockRepository);
  });

  group('GetProductById', () {
    const testProductId = '123';
    final testProduct = Product(
      id: testProductId,
      name: 'Test Product',
      price: 29.99,
      inStock: true,
    );

    test('should return product when repository call is successful', () async {
      // Arrange
      when(() => mockRepository.getProductById(testProductId))
          .thenAnswer((_) async => Right(testProduct));

      // Act
      final result = await getProductById(testProductId);

      // Assert
      expect(result, Right(testProduct));
      verify(() => mockRepository.getProductById(testProductId)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return failure when repository call fails', () async {
      // Arrange
      when(() => mockRepository.getProductById(testProductId))
          .thenAnswer((_) async => const Left(ServerFailure()));

      // Act
      final result = await getProductById(testProductId);

      // Assert
      expect(result, const Left(ServerFailure()));
      verify(() => mockRepository.getProductById(testProductId)).called(1);
    });

    test('should return validation failure when product ID is empty', () async {
      // Act
      final result = await getProductById('');

      // Assert
      expect(result, isA<Left>());
      final failure = (result as Left).value;
      expect(failure, isA<ValidationFailure>());
      expect(failure.message, 'Product ID is required');

      // Verify repository was never called
      verifyZeroInteractions(mockRepository);
    });
  });
}
```

**Best Practices:**

1. **Name clearly**: `GetUser`, `CreateOrder`, `DeleteProduct`
2. **Single method**: Usually just `call()`
3. **Validate inputs**: Check business rules before calling repository
4. **Return Either**: For consistent error handling
5. **No UI logic**: Keep it pure business logic
6. **Inject dependencies**: Via constructor
7. **Test thoroughly**: Unit test each use case

---

### 19. **Should a Use Case contain only one public method? Why or why not?**

**Yes, a Use Case should typically have only ONE public method (usually `call()`).**

**Reasons:**

**1. Single Responsibility Principle:**
```dart
// ✅ Good: One responsibility
class CreateOrder {
  final OrderRepository repository;

  CreateOrder(this.repository);

  Future<Either<Failure, Order>> call(CreateOrderParams params) {
    // One clear responsibility: Create an order
  }
}

// ❌ Bad: Multiple responsibilities
class OrderUseCase {
  final OrderRepository repository;

  OrderUseCase(this.repository);

  Future<Either<Failure, Order>> createOrder(CreateOrderParams params) {}
  Future<Either<Failure, Order>> updateOrder(UpdateOrderParams params) {}
  Future<Either<Failure, void>> cancelOrder(String orderId) {}
  Future<Either<Failure, List<Order>>> getUserOrders(String userId) {}
  // Too many responsibilities!
}
```

**2. Better Testability:**
```dart
// ✅ Easy to test
void main() {
  late CreateOrder createOrder;
  late MockOrderRepository mockRepository;

  setUp(() {
    mockRepository = MockOrderRepository();
    createOrder = CreateOrder(mockRepository);
  });

  test('should create order successfully', () async {
    // Test one clear behavior
    final result = await createOrder(testParams);
    expect(result, isA<Right>());
  });
}

// ❌ Harder to test multiple methods
void main() {
  late OrderUseCase orderUseCase;

  setUp(() {
    orderUseCase = OrderUseCase(mockRepository);
  });

  group('createOrder', () {
    // Tests for createOrder
  });

  group('updateOrder', () {
    // Tests for updateOrder
  });

  group('cancelOrder', () {
    // Tests for cancelOrder
  });

  // Getting complicated...
}
```

**3. Clearer Dependencies:**
```dart
// ✅ Clear what each use case needs
class CreateOrder {
  final OrderRepository orderRepository;
  final PaymentRepository paymentRepository;
  final InventoryRepository inventoryRepository;

  CreateOrder({
    required this.orderRepository,
    required this.paymentRepository,
    required this.inventoryRepository,
  });
}

class GetOrderHistory {
  final OrderRepository orderRepository;  // Only needs this

  GetOrderHistory(this.orderRepository);
}

// ❌ Unclear dependencies
class OrderUseCase {
  final OrderRepository orderRepository;
  final PaymentRepository paymentRepository;
  final InventoryRepository inventoryRepository;
  final UserRepository userRepository;
  // Do all methods need all these? Unclear!

  // Some methods might not need all repositories
  Future<List<Order>> getUserOrders(String userId) {
    // Only uses orderRepository, why inject others?
  }
}
```

**4. Better Reusability:**
```dart
// ✅ Can compose use cases
class CheckoutController extends GetxController {
  final CreateOrder createOrder;
  final ProcessPayment processPayment;
  final ClearCart clearCart;

  // Clear separation, can reuse each independently

  Future<void> checkout() async {
    final orderResult = await createOrder(orderParams);
    // ...
    final paymentResult = await processPayment(paymentParams);
    // ...
    await clearCart(userId);
  }
}

// ❌ Tightly coupled
class CheckoutController extends GetxController {
  final OrderUseCase orderUseCase;  // Has too many methods

  Future<void> checkout() async {
    await orderUseCase.createOrder(...);
    await orderUseCase.processPayment(...);
    await orderUseCase.clearCart(...);
    // Can't reuse individual operations easily
  }
}
```

**When is it acceptable to have helper/private methods?**

**✅ YES - Private helper methods are fine:**
```dart
class CreateOrder {
  final OrderRepository orderRepository;
  final InventoryRepository inventoryRepository;

  CreateOrder({
    required this.orderRepository,
    required this.inventoryRepository,
  });

  // ✅ One public method
  Future<Either<Failure, Order>> call(CreateOrderParams params) async {
    // Validate
    final validationFailure = _validateParams(params);
    if (validationFailure != null) {
      return Left(validationFailure);
    }

    // Check inventory
    final hasStock = await _checkInventory(params.items);
    if (!hasStock) {
      return const Left(ValidationFailure('Some items are out of stock'));
    }

    // Calculate totals
    final totals = _calculateTotals(params.items);

    // Create order
    return await orderRepository.createOrder(
      OrderData(
        userId: params.userId,
        items: params.items,
        subtotal: totals.subtotal,
        tax: totals.tax,
        shipping: totals.shipping,
      ),
    );
  }

  // ✅ Private helper methods - OK!
  Failure? _validateParams(CreateOrderParams params) {
    if (params.items.isEmpty) {
      return ValidationFailure('Order must have items');
    }

    if (params.userId.isEmpty) {
      return ValidationFailure('User ID is required');
    }

    return null;
  }

  Future<bool> _checkInventory(List<OrderItem> items) async {
    for (final item in items) {
      final result = await inventoryRepository.checkStock(
        item.productId,
        item.quantity,
      );

      final hasStock = result.fold(
        (failure) => false,
        (available) => available,
      );

      if (!hasStock) return false;
    }

    return true;
  }

  OrderTotals _calculateTotals(List<OrderItem> items) {
    final subtotal = items.fold(
      0.0,
      (sum, item) => sum + (item.price * item.quantity),
    );

    final tax = subtotal * 0.1;
    final shipping = subtotal >= 50.0 ? 0.0 : 5.99;

    return OrderTotals(
      subtotal: subtotal,
      tax: tax,
      shipping: shipping,
    );
  }
}

class OrderTotals {
  final double subtotal;
  final double tax;
  final double shipping;

  OrderTotals({
    required this.subtotal,
    required this.tax,
    required this.shipping,
  });

  double get total => subtotal + tax + shipping;
}
```

**❌ NO - Multiple public methods:**
```dart
class OrderUseCase {
  final OrderRepository repository;

  OrderUseCase(this.repository);

  // ❌ Multiple public methods - split into separate use cases
  Future<Either<Failure, Order>> createOrder(CreateOrderParams params) {}
  Future<Either<Failure, Order>> updateOrder(UpdateOrderParams params) {}
  Future<Either<Failure, void>> cancelOrder(String orderId) {}
  Future<Either<Failure, Order>> getOrder(String orderId) {}
}
```

**Proper Solution - Split into separate use cases:**
```dart
// ✅ Separate use cases
class CreateOrder {
  Future<Either<Failure, Order>> call(CreateOrderParams params) {}
}

class UpdateOrder {
  Future<Either<Failure, Order>> call(UpdateOrderParams params) {}
}

class CancelOrder {
  Future<Either<Failure, void>> call(String orderId) {}
}

class GetOrder {
  Future<Either<Failure, Order>> call(String orderId) {}
}
```

**Summary:**
- **One public method**: Usually `call()` or `execute()`
- **Private helpers**: Allowed and encouraged for code organization
- **Multiple public methods**: Split into separate use cases
- **Benefit**: Clear responsibility, better testing, better reusability

---

### 20. **How do you handle parameters in Use Cases?**

**Different approaches based on complexity:**

**1. No Parameters:**
```dart
// Use NoParams class or omit parameter
class GetCurrentUser {
  final UserRepository repository;

  GetCurrentUser(this.repository);

  Future<Either<Failure, User>> call() {
    return repository.getCurrentUser();
  }
}

// Usage
final result = await getCurrentUser();

// Alternative with NoParams
class GetAllProducts implements UseCase<List<Product>, NoParams> {
  final ProductRepository repository;

  GetAllProducts(this.repository);

  @override
  Future<Either<Failure, List<Product>>> call(NoParams params) {
    return repository.getAllProducts();
  }
}

// Usage
final result = await getAllProducts(NoParams());
```

**2. Single Simple Parameter:**
```dart
// Just pass the parameter directly
class GetUserById {
  final UserRepository repository;

  GetUserById(this.repository);

  Future<Either<Failure, User>> call(String userId) async {
    if (userId.isEmpty) {
      return const Left(ValidationFailure('User ID is required'));
    }

    return await repository.getUserById(userId);
  }
}

// Usage
final result = await getUserById('user-123');

// Another example
class DeleteProduct {
  final ProductRepository repository;

  DeleteProduct(this.repository);

  Future<Either<Failure, void>> call(String productId) async {
    if (productId.isEmpty) {
      return const Left(ValidationFailure('Product ID is required'));
    }

    return await repository.deleteProduct(productId);
  }
}

// Usage
final result = await deleteProduct('product-456');
```

**3. Multiple Parameters - Create Params Class:**
```dart
// Good for 2+ parameters
class LoginUser {
  final AuthRepository repository;

  LoginUser(this.repository);

  Future<Either<Failure, User>> call(LoginParams params) async {
    // Validate params
    if (params.email.isEmpty) {
      return const Left(ValidationFailure('Email is required'));
    }

    if (params.password.isEmpty) {
      return const Left(ValidationFailure('Password is required'));
    }

    if (params.password.length < 6) {
      return const Left(ValidationFailure('Password must be at least 6 characters'));
    }

    return await repository.login(params.email, params.password);
  }
}

// Params class
class LoginParams {
  final String email;
  final String password;

  LoginParams({
    required this.email,
    required this.password,
  });

  // Optional: Add validation methods
  bool get isValid {
    return email.isNotEmpty &&
           password.isNotEmpty &&
           password.length >= 6;
  }

  // Optional: Add copyWith for immutability
  LoginParams copyWith({
    String? email,
    String? password,
  }) {
    return LoginParams(
      email: email ?? this.email,
      password: password ?? this.password,
    );
  }
}

// Usage
final result = await loginUser(
  LoginParams(
    email: 'user@example.com',
    password: 'password123',
  ),
);
```

**4. Complex Parameters with Optional Fields:**
```dart
class SearchProducts {
  final ProductRepository repository;

  SearchProducts(this.repository);

  Future<Either<Failure, List<Product>>> call(SearchProductsParams params) async {
    // Validate
    if (params.query.trim().isEmpty) {
      return const Left(ValidationFailure('Search query is required'));
    }

    if (params.query.length < 3) {
      return const Left(
        ValidationFailure('Search query must be at least 3 characters'),
      );
    }

    // Business logic based on params
    return await repository.searchProducts(
      query: params.query,
      category: params.category,
      minPrice: params.minPrice,
      maxPrice: params.maxPrice,
      sortBy: params.sortBy,
      page: params.page,
      pageSize: params.pageSize,
    );
  }
}

class SearchProductsParams {
  final String query;
  final String? category;
  final double? minPrice;
  final double? maxPrice;
  final ProductSortOption sortBy;
  final int page;
  final int pageSize;

  SearchProductsParams({
    required this.query,
    this.category,
    this.minPrice,
    this.maxPrice,
    this.sortBy = ProductSortOption.relevance,
    this.page = 1,
    this.pageSize = 20,
  });

  // Validation
  bool get hasValidPriceRange {
    if (minPrice != null && maxPrice != null) {
      return minPrice! <= maxPrice!;
    }
    return true;
  }

  // Helper methods
  bool get hasFilters {
    return category != null ||
           minPrice != null ||
           maxPrice != null;
  }

  // CopyWith for easy modification
  SearchProductsParams copyWith({
    String? query,
    String? category,
    double? minPrice,
    double? maxPrice,
    ProductSortOption? sortBy,
    int? page,
    int? pageSize,
  }) {
    return SearchProductsParams(
      query: query ?? this.query,
      category: category ?? this.category,
      minPrice: minPrice ?? this.minPrice,
      maxPrice: maxPrice ?? this.maxPrice,
      sortBy: sortBy ?? this.sortBy,
      page: page ?? this.page,
      pageSize: pageSize ?? this.pageSize,
    );
  }
}

enum ProductSortOption {
  relevance,
  priceLowToHigh,
  priceHighToLow,
  nameAZ,
  nameZA,
  newest,
}

// Usage
final result = await searchProducts(
  SearchProductsParams(
    query: 'laptop',
    category: 'electronics',
    minPrice: 500,
    maxPrice: 2000,
    sortBy: ProductSortOption.priceLowToHigh,
  ),
);
```

**5. Using Equatable for Params (Recommended):**
```dart
import 'package:equatable/equatable.dart';

class CreateOrderParams extends Equatable {
  final String userId;
  final List<OrderItem> items;
  final String shippingAddress;
  final String billingAddress;
  final String paymentMethodId;
  final String? couponCode;

  const CreateOrderParams({
    required this.userId,
    required this.items,
    required this.shippingAddress,
    required this.billingAddress,
    required this.paymentMethodId,
    this.couponCode,
  });

  @override
  List<Object?> get props => [
    userId,
    items,
    shippingAddress,
    billingAddress,
    paymentMethodId,
    couponCode,
  ];

  CreateOrderParams copyWith({
    String? userId,
    List<OrderItem>? items,
    String? shippingAddress,
    String? billingAddress,
    String? paymentMethodId,
    String? couponCode,
  }) {
    return CreateOrderParams(
      userId: userId ?? this.userId,
      items: items ?? this.items,
      shippingAddress: shippingAddress ?? this.shippingAddress,
      billingAddress: billingAddress ?? this.billingAddress,
      paymentMethodId: paymentMethodId ?? this.paymentMethodId,
      couponCode: couponCode ?? this.couponCode,
    );
  }
}

// Usage
final params = CreateOrderParams(
  userId: '123',
  items: cartItems,
  shippingAddress: '123 Main St',
  billingAddress: '123 Main St',
  paymentMethodId: 'pm_123',
  couponCode: 'SAVE10',
);

final result = await createOrder(params);
```

**6. Using Freezed for Params (Advanced):**
```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'update_profile_params.freezed.dart';

@freezed
class UpdateProfileParams with _$UpdateProfileParams {
  const factory UpdateProfileParams({
    required String userId,
    String? name,
    String? email,
    String? phoneNumber,
    String? avatarUrl,
    String? bio,
  }) = _UpdateProfileParams;
}

// Usage
final params = UpdateProfileParams(
  userId: 'user-123',
  name: 'John Doe',
  email: 'john@example.com',
);

// Easy to modify with copyWith (provided by freezed)
final updatedParams = params.copyWith(
  phoneNumber: '+1234567890',
);

final result = await updateProfile(updatedParams);
```

**7. Named Parameters vs Params Class:**
```dart
// ❌ Avoid: Too many named parameters
class CreateUser {
  Future<Either<Failure, User>> call({
    required String name,
    required String email,
    required String password,
    String? phoneNumber,
    String? address,
    String? city,
    String? country,
    String? postalCode,
  }) {
    // Hard to manage, hard to test
  }
}

// ✅ Better: Use params class
class CreateUser {
  Future<Either<Failure, User>> call(CreateUserParams params) {
    // Much cleaner
  }
}

class CreateUserParams {
  final String name;
  final String email;
  final String password;
  final String? phoneNumber;
  final Address? address;

  CreateUserParams({
    required this.name,
    required this.email,
    required this.password,
    this.phoneNumber,
    this.address,
  });
}
```

**8. Testing with Params:**
```dart
void main() {
  late LoginUser loginUser;
  late MockAuthRepository mockRepository;

  setUp(() {
    mockRepository = MockAuthRepository();
    loginUser = LoginUser(mockRepository);
  });

  group('LoginUser', () {
    final testParams = LoginParams(
      email: 'test@example.com',
      password: 'password123',
    );

    test('should return user when login is successful', () async {
      // Arrange
      when(() => mockRepository.login(any(), any()))
          .thenAnswer((_) async => Right(testUser));

      // Act
      final result = await loginUser(testParams);

      // Assert
      expect(result, Right(testUser));
      verify(() => mockRepository.login(
        testParams.email,
        testParams.password,
      )).called(1);
    });

    test('should return failure when email is empty', () async {
      // Arrange
      final invalidParams = testParams.copyWith(email: '');

      // Act
      final result = await loginUser(invalidParams);

      // Assert
      expect(result, isA<Left>());
      verifyZeroInteractions(mockRepository);
    });
  });
}
```

**Best Practices:**

1. **No params**: Omit parameter or use `NoParams`
2. **1 param**: Pass directly
3. **2+ params**: Create params class
4. **Use Equatable**: For value equality and testing
5. **Use Freezed**: For immutability and code generation
6. **Add validation**: In params class or use case
7. **Add copyWith**: For easy modification
8. **Name clearly**: `LoginParams`, `CreateOrderParams`

---

This continues the comprehensive answers. Would you like me to continue with questions 21-60?