# Flutter CI/CD: Answers

## Beginner Level

**1. What is CI/CD and why is it important in Flutter development?**

**CI (Continuous Integration)**: Automatically building and testing code when changes are pushed.
**CD (Continuous Deployment/Delivery)**: Automatically deploying tested code to production or app stores.

**Why it's important for Flutter:**
1. **Automated testing**: Run unit, widget, integration tests on every push
2. **Build verification**: Ensure code compiles for all platforms
3. **Quality assurance**: Catch bugs before they reach production
4. **Faster releases**: Reduce manual deployment steps
5. **Consistency**: Same build process every time
6. **Platform coverage**: Test iOS, Android, Web simultaneously

```yaml
# Simple CI example
name: Flutter CI
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: flutter test
      - run: flutter build apk
```

---

**2. What are the key differences between Continuous Integration (CI) and Continuous Deployment (CD)?**

| Aspect | Continuous Integration | Continuous Deployment |
|--------|----------------------|----------------------|
| Focus | Building & Testing | Releasing & Deploying |
| Trigger | Every commit/PR | After CI passes |
| Output | Build artifacts, test results | App in store/production |
| Frequency | Multiple times daily | Per release/feature |
| Automation | Tests, linting, builds | Store uploads, releases |

**CI Pipeline:**
```
Code Push → Build → Test → Report
```

**CD Pipeline:**
```
CI Pass → Sign → Upload to Store → Release
```

---

**3. What are the main benefits of implementing CI/CD in Flutter projects?**

1. **Early Bug Detection**: Tests run automatically on every change
2. **Faster Development**: No manual build/test cycles
3. **Consistent Builds**: Same environment every time
4. **Team Collaboration**: Everyone sees build status
5. **Reduced Risk**: Small, frequent releases
6. **Documentation**: Build history shows what changed
7. **Time Savings**: Automate repetitive tasks
8. **Quality Gates**: Enforce code standards

**Real-world impact:**
```
Before CI/CD:
- 2 hours to test manually
- 1 hour to build all platforms
- Frequent "works on my machine" issues

After CI/CD:
- Tests run in 10 minutes
- All platforms build in parallel
- Consistent reproducible builds
```

---

**4. Name five popular CI/CD platforms that support Flutter development.**

1. **GitHub Actions**
   - Free for public repos
   - Native GitHub integration
   - Extensive marketplace

2. **Codemagic**
   - Flutter-specific
   - macOS machines included
   - Built-in code signing

3. **Bitrise**
   - Mobile-focused
   - Pre-built Flutter steps
   - Good for teams

4. **CircleCI**
   - Flexible configuration
   - Docker support
   - Good performance

5. **GitLab CI/CD**
   - Built into GitLab
   - Self-hosted option
   - Full DevOps platform

**Others:** Azure DevOps, Travis CI, Jenkins, Fastlane (automation tool)

---

**5. What is a CI/CD pipeline and what are its main components?**

A **pipeline** is a series of automated steps that code goes through from commit to deployment.

**Main Components:**

```yaml
# 1. Trigger - What starts the pipeline
on:
  push:
    branches: [main]
  pull_request:

# 2. Jobs - Groups of steps
jobs:
  test:
    runs-on: ubuntu-latest
    steps: [...]

  build-android:
    runs-on: ubuntu-latest
    needs: test  # Dependency
    steps: [...]

  build-ios:
    runs-on: macos-latest
    needs: test
    steps: [...]

  deploy:
    needs: [build-android, build-ios]
    steps: [...]
```

**Stages:**
1. **Source**: Get code from repository
2. **Build**: Compile the application
3. **Test**: Run automated tests
4. **Package**: Create artifacts (APK, IPA)
5. **Deploy**: Upload to stores/servers

---

**6. How does automated testing fit into a CI/CD pipeline?**

Testing is the **quality gate** that determines if code can proceed.

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Unit tests
      - name: Run unit tests
        run: flutter test --coverage

      # Widget tests
      - name: Run widget tests
        run: flutter test test/widgets/

      # Integration tests
      - name: Run integration tests
        run: flutter test integration_test/

      # Upload coverage
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage/lcov.info

  build:
    needs: test  # Only runs if tests pass
    runs-on: ubuntu-latest
    steps: [...]
```

**Test Types in Pipeline:**
- **Unit tests**: Fast, run on every commit
- **Widget tests**: Test UI components
- **Integration tests**: Full app flows
- **Golden tests**: Screenshot comparisons

---

**7. What is GitHub Actions and how does it work with Flutter projects?**

**GitHub Actions** is GitHub's built-in CI/CD platform using YAML workflow files.

**How it works:**
1. Create `.github/workflows/` directory
2. Add YAML workflow files
3. Define triggers, jobs, and steps
4. GitHub runs workflows automatically

**Basic Flutter workflow:**
```yaml
name: Flutter CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: 'stable'

      - name: Get dependencies
        run: flutter pub get

      - name: Analyze code
        run: flutter analyze

      - name: Run tests
        run: flutter test

      - name: Build APK
        run: flutter build apk --release
```

---

**8. What is the purpose of a workflow file in GitHub Actions?**

A **workflow file** defines the automation process:
- When to run (triggers)
- Where to run (runners)
- What to do (jobs and steps)

**File location:** `.github/workflows/name.yml`

```yaml
# Workflow file structure
name: Workflow Name           # Display name

on:                           # Triggers
  push:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'       # Daily at midnight

env:                          # Global environment variables
  FLUTTER_VERSION: '3.16.0'

jobs:                         # Work to perform
  job-name:
    runs-on: ubuntu-latest    # Runner
    env:                      # Job-level variables
      API_KEY: ${{ secrets.API_KEY }}

    steps:                    # Individual tasks
      - name: Step Name
        uses: action/name@v1  # Pre-built action
        with:                 # Action inputs
          param: value

      - name: Run Command
        run: |                # Shell commands
          echo "Hello"
          flutter build
```

---

**9. What are artifacts in CI/CD and why are they important?**

**Artifacts** are files produced by a build (APKs, IPAs, test results, logs).

**Why important:**
1. Download and test builds without local compilation
2. Store build history
3. Share between jobs
4. Deploy to stores

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - name: Build APK
        run: flutter build apk --release

      # Upload artifact
      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: release-apk
          path: build/app/outputs/flutter-apk/app-release.apk
          retention-days: 30

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      # Download artifact from build job
      - name: Download APK
        uses: actions/download-artifact@v4
        with:
          name: release-apk

      - name: Deploy to store
        run: fastlane deploy
```

---

**10. What is the difference between hosted runners and self-hosted runners?**

| Aspect | Hosted Runners | Self-Hosted Runners |
|--------|---------------|-------------------|
| Management | GitHub manages | You manage |
| Cost | Free tier + paid | Your infrastructure |
| Hardware | Standard specs | Custom hardware |
| Software | Pre-installed | Full control |
| Security | Shared | Your network |
| iOS builds | macOS available | Need Mac hardware |

**Hosted runner:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest  # GitHub-hosted
```

**Self-hosted runner:**
```yaml
jobs:
  build:
    runs-on: self-hosted  # Your machine
    # or with labels
    runs-on: [self-hosted, macOS, ARM64]
```

**When to use self-hosted:**
- Need specific hardware
- Want faster builds (more powerful machines)
- Security requirements
- Cost optimization at scale

---

**11. What is Codemagic and what makes it suitable for Flutter projects?**

**Codemagic** is a CI/CD platform specifically designed for Flutter/mobile development.

**Why it's suitable:**
1. **Flutter-native**: Pre-configured for Flutter
2. **macOS included**: Build iOS without extra setup
3. **Code signing**: Built-in certificate management
4. **App store deployment**: Direct publishing
5. **YAML or UI**: Configure via file or web interface

**codemagic.yaml example:**
```yaml
workflows:
  flutter-workflow:
    name: Flutter Build
    max_build_duration: 60
    environment:
      flutter: stable
      xcode: latest
      cocoapods: default

    scripts:
      - name: Get dependencies
        script: flutter pub get

      - name: Run tests
        script: flutter test

      - name: Build Android
        script: flutter build apk --release

      - name: Build iOS
        script: |
          flutter build ipa --release \
            --export-options-plist=/path/to/options.plist

    artifacts:
      - build/**/outputs/**/*.apk
      - build/ios/ipa/*.ipa

    publishing:
      google_play:
        credentials: $GCLOUD_SERVICE_ACCOUNT
        track: internal
      app_store_connect:
        api_key: $APP_STORE_CONNECT_API_KEY
```

---

**12. What are environment variables and why are they important in CI/CD?**

**Environment variables** store configuration values separate from code.

**Why important:**
1. **Security**: Keep secrets out of code
2. **Flexibility**: Different values per environment
3. **Configuration**: Easy to change without code changes

```yaml
# GitHub Actions
env:
  FLUTTER_VERSION: '3.16.0'  # Plain value

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      API_KEY: ${{ secrets.API_KEY }}  # Secret

    steps:
      - name: Use variables
        run: |
          echo "Flutter version: $FLUTTER_VERSION"
          # API_KEY available but not printed
        env:
          BUILD_NUMBER: ${{ github.run_number }}
```

**Setting secrets in GitHub:**
1. Repository → Settings → Secrets and variables → Actions
2. New repository secret
3. Add name and value

**Common secrets:**
- `FIREBASE_TOKEN`
- `GOOGLE_PLAY_KEY`
- `APP_STORE_CONNECT_API_KEY`
- `KEYSTORE_PASSWORD`
- `SIGNING_KEY`

---

**13. What is code signing and why is it necessary for mobile app deployment?**

**Code signing** cryptographically signs your app to verify:
1. The app comes from you (identity)
2. The app hasn't been modified (integrity)

**Android signing:**
```bash
# Create keystore
keytool -genkey -v -keystore my-key.keystore \
  -alias my-alias -keyalg RSA -keysize 2048 -validity 10000

# In build.gradle
android {
    signingConfigs {
        release {
            keyAlias 'my-alias'
            keyPassword System.getenv("KEY_PASSWORD")
            storeFile file('../my-key.keystore')
            storePassword System.getenv("KEYSTORE_PASSWORD")
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

**iOS signing:**
- **Certificates**: Identity (who you are)
- **Provisioning Profiles**: What you can do
- Required for: TestFlight, App Store

**CI/CD signing approaches:**
1. Store keystore/certificates as secrets
2. Use Codemagic/Fastlane match
3. Environment-specific signing configs

---

**14. What is the purpose of build flavors in Flutter?**

**Build flavors** create different versions of your app (dev, staging, prod) with different configurations.

**Use cases:**
- Different API endpoints
- Different app names/icons
- Feature flags
- Analytics configuration

**Android (android/app/build.gradle):**
```groovy
flavorDimensions "environment"
productFlavors {
    dev {
        dimension "environment"
        applicationIdSuffix ".dev"
        versionNameSuffix "-dev"
    }
    staging {
        dimension "environment"
        applicationIdSuffix ".staging"
        versionNameSuffix "-staging"
    }
    prod {
        dimension "environment"
    }
}
```

**Flutter commands:**
```bash
# Build specific flavor
flutter build apk --flavor dev
flutter build apk --flavor prod

# Run with flavor
flutter run --flavor dev
```

**In code:**
```dart
// Using --dart-define
// flutter run --dart-define=ENV=dev
const String env = String.fromEnvironment('ENV', defaultValue: 'prod');
```

---

**15. What is Firebase App Distribution and how is it used in CI/CD?**

**Firebase App Distribution** distributes pre-release builds to testers.

**Benefits:**
- Easy tester management
- No TestFlight/Play Console needed for testing
- Works for both iOS and Android
- In-app update prompts

**CI/CD integration:**
```yaml
- name: Build APK
  run: flutter build apk --release

- name: Upload to Firebase App Distribution
  uses: wzieba/Firebase-Distribution-Github-Action@v1
  with:
    appId: ${{ secrets.FIREBASE_APP_ID }}
    serviceCredentialsFileContent: ${{ secrets.FIREBASE_CREDENTIALS }}
    groups: testers
    file: build/app/outputs/flutter-apk/app-release.apk
    releaseNotes: "Build ${{ github.run_number }}"
```

**Using Firebase CLI:**
```bash
firebase appdistribution:distribute \
  build/app/outputs/flutter-apk/app-release.apk \
  --app YOUR_APP_ID \
  --groups "testers" \
  --release-notes "New build"
```

---

## Intermediate Level

**16. How do you set up a basic GitHub Actions workflow for Flutter testing?**

```yaml
# .github/workflows/test.yml
name: Flutter Test

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          channel: stable
          cache: true  # Cache Flutter SDK

      - name: Install dependencies
        run: flutter pub get

      - name: Verify formatting
        run: dart format --set-exit-if-changed .

      - name: Analyze code
        run: flutter analyze --fatal-infos

      - name: Run tests
        run: flutter test --coverage

      - name: Check coverage
        uses: VeryGoodOpenSource/very_good_coverage@v2
        with:
          min_coverage: 80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: coverage/lcov.info
```

---

**17. What is Fastlane and how is it used in Flutter CI/CD pipelines?**

**Fastlane** is an automation tool for mobile app deployment.

**Features:**
- Automated screenshots
- Code signing management
- Store uploads
- Beta distribution

**Setup for Flutter:**
```bash
# Install
gem install fastlane

# Initialize (in ios/ or android/ folder)
cd ios
fastlane init

cd android
fastlane init
```

**ios/fastlane/Fastfile:**
```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    # Build Flutter app
    sh "cd .. && flutter build ipa --release"

    # Upload to TestFlight
    upload_to_testflight(
      ipa: "../build/ios/ipa/MyApp.ipa",
      skip_waiting_for_build_processing: true
    )
  end
end
```

**android/fastlane/Fastfile:**
```ruby
default_platform(:android)

platform :android do
  desc "Deploy to Play Store internal track"
  lane :internal do
    upload_to_play_store(
      track: 'internal',
      aab: '../build/app/outputs/bundle/release/app-release.aab',
      json_key: 'play-store-key.json'
    )
  end
end
```

**In CI/CD:**
```yaml
- name: Deploy Android
  run: |
    cd android
    bundle exec fastlane internal
```

---

**18. How do you configure automated testing in a CI/CD pipeline for Flutter?**

```yaml
name: Full Test Suite

on: [push, pull_request]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter test test/unit/ --coverage

  widget-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter test test/widget/

  integration-tests:
    runs-on: macos-latest  # For iOS simulator
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Start iOS simulator
      - name: Start Simulator
        run: |
          xcrun simctl boot "iPhone 15"
          xcrun simctl bootstatus "iPhone 15" -b

      - run: flutter pub get
      - run: flutter test integration_test/

  golden-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter pub get
      - run: flutter test --update-goldens  # Update if needed
      - run: flutter test test/golden/

      # Upload golden diffs on failure
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: golden-failures
          path: test/**/failures/
```

---

**19. What are GitHub Secrets and how do you use them securely in workflows?**

**GitHub Secrets** store sensitive data encrypted at rest.

**Creating secrets:**
1. Repository → Settings → Secrets → Actions
2. New repository secret
3. Enter name (e.g., `KEYSTORE_BASE64`) and value

**Using in workflow:**
```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
      KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
      KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}

    steps:
      - uses: actions/checkout@v4

      # Decode base64 encoded keystore
      - name: Decode Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/keystore.jks

      - name: Build APK
        run: flutter build apk --release
```

**Best practices:**
1. Never print secrets in logs
2. Use minimal permissions
3. Rotate secrets regularly
4. Use repository secrets for repo-specific
5. Use organization secrets for shared values

**Encoding files as secrets:**
```bash
# Encode file to base64
base64 -i keystore.jks | pbcopy  # Copy to clipboard

# In workflow, decode
echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > keystore.jks
```

---

**20. How do you implement code signing for iOS apps in a CI/CD pipeline?**

**Method 1: Manual certificate management**
```yaml
jobs:
  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Install Apple certificate
      - name: Install Certificate
        env:
          CERTIFICATE_BASE64: ${{ secrets.IOS_CERTIFICATE_BASE64 }}
          CERTIFICATE_PASSWORD: ${{ secrets.IOS_CERTIFICATE_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
        run: |
          # Create keychain
          security create-keychain -p "$KEYCHAIN_PASSWORD" build.keychain
          security default-keychain -s build.keychain
          security unlock-keychain -p "$KEYCHAIN_PASSWORD" build.keychain

          # Import certificate
          echo "$CERTIFICATE_BASE64" | base64 --decode > certificate.p12
          security import certificate.p12 -k build.keychain \
            -P "$CERTIFICATE_PASSWORD" -T /usr/bin/codesign
          security set-key-partition-list -S apple-tool:,apple: \
            -s -k "$KEYCHAIN_PASSWORD" build.keychain

      # Install provisioning profile
      - name: Install Profile
        env:
          PROFILE_BASE64: ${{ secrets.IOS_PROFILE_BASE64 }}
        run: |
          mkdir -p ~/Library/MobileDevice/Provisioning\ Profiles
          echo "$PROFILE_BASE64" | base64 --decode > profile.mobileprovision
          cp profile.mobileprovision ~/Library/MobileDevice/Provisioning\ Profiles/

      - run: flutter build ipa --release

      # Cleanup
      - name: Cleanup
        if: always()
        run: security delete-keychain build.keychain
```

**Method 2: Fastlane Match (recommended)**
```yaml
- name: Setup Match
  run: |
    cd ios
    bundle exec fastlane match appstore --readonly
  env:
    MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
    MATCH_GIT_PRIVATE_KEY: ${{ secrets.MATCH_GIT_PRIVATE_KEY }}
```

---

**21. How do you implement code signing for Android apps in a CI/CD pipeline?**

```yaml
jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Decode and setup keystore
      - name: Setup Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/upload-keystore.jks

      # Create key.properties
      - name: Create key.properties
        run: |
          cat > android/key.properties <<EOF
          storePassword=${{ secrets.KEYSTORE_PASSWORD }}
          keyPassword=${{ secrets.KEY_PASSWORD }}
          keyAlias=${{ secrets.KEY_ALIAS }}
          storeFile=upload-keystore.jks
          EOF

      - name: Build AAB
        run: flutter build appbundle --release

      # Cleanup sensitive files
      - name: Cleanup
        if: always()
        run: |
          rm -f android/app/upload-keystore.jks
          rm -f android/key.properties
```

**android/app/build.gradle:**
```groovy
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ?
                file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

---

**22. What is a build matrix in GitHub Actions and when would you use it?**

A **build matrix** runs jobs with multiple configurations in parallel.

**Use cases:**
- Test on multiple Flutter versions
- Build for multiple platforms
- Test on different OS versions

```yaml
jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        flutter-version: ['3.16.0', '3.19.0']
        channel: [stable, beta]
        exclude:
          - os: windows-latest
            channel: beta  # Skip beta on Windows

    steps:
      - uses: actions/checkout@v4

      - uses: subosito/flutter-action@v2
        with:
          flutter-version: ${{ matrix.flutter-version }}
          channel: ${{ matrix.channel }}

      - run: flutter pub get
      - run: flutter test

  build:
    needs: test
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false  # Continue other builds if one fails
      matrix:
        include:
          - os: ubuntu-latest
            build-cmd: flutter build apk
            artifact: build/app/outputs/flutter-apk/app-release.apk
          - os: macos-latest
            build-cmd: flutter build ipa --no-codesign
            artifact: build/ios/archive/
          - os: ubuntu-latest
            build-cmd: flutter build web
            artifact: build/web/

    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - run: ${{ matrix.build-cmd }}

      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ matrix.os }}
          path: ${{ matrix.artifact }}
```

---

**23. How do you configure multiple build flavors (dev, staging, production) in CI/CD?**

```yaml
name: Build All Flavors

on:
  push:
    branches: [main]

jobs:
  build-flavors:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        flavor: [dev, staging, prod]
        include:
          - flavor: dev
            build-type: apk
          - flavor: staging
            build-type: apk
          - flavor: prod
            build-type: appbundle

    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter pub get

      - name: Build ${{ matrix.flavor }}
        run: |
          flutter build ${{ matrix.build-type }} \
            --flavor ${{ matrix.flavor }} \
            --dart-define=ENV=${{ matrix.flavor }}
        env:
          # Flavor-specific secrets
          API_KEY: ${{ secrets[format('{0}_API_KEY', matrix.flavor)] }}

      - name: Upload ${{ matrix.flavor }} artifact
        uses: actions/upload-artifact@v4
        with:
          name: app-${{ matrix.flavor }}
          path: |
            build/app/outputs/**/*.apk
            build/app/outputs/**/*.aab

  deploy-staging:
    needs: build-flavors
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: app-staging

      - name: Deploy to Firebase App Distribution
        run: |
          # Deploy staging to testers
```

---

**24. What is TestFlight and how do you automate deployment to it?**

**TestFlight** is Apple's beta testing platform for iOS apps.

**Automated deployment:**
```yaml
jobs:
  deploy-testflight:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Setup signing (see question 20)
      - name: Setup Signing
        run: # ... certificate and profile setup

      - name: Build IPA
        run: flutter build ipa --release

      - name: Upload to TestFlight
        uses: apple-actions/upload-testflight-build@v1
        with:
          app-path: build/ios/ipa/MyApp.ipa
          issuer-id: ${{ secrets.APP_STORE_CONNECT_ISSUER_ID }}
          api-key-id: ${{ secrets.APP_STORE_CONNECT_KEY_ID }}
          api-private-key: ${{ secrets.APP_STORE_CONNECT_PRIVATE_KEY }}
```

**Using Fastlane:**
```ruby
# ios/fastlane/Fastfile
lane :beta do
  # Build with Flutter
  sh "cd .. && flutter build ipa --release"

  # Upload to TestFlight
  upload_to_testflight(
    ipa: "../build/ios/ipa/MyApp.ipa",
    changelog: "New build from CI",
    distribute_external: true,
    groups: ["External Testers"]
  )
end
```

---

**25. How do you automate deployment to Google Play internal testing?**

```yaml
jobs:
  deploy-play-store:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Setup signing
      - name: Setup Keystore
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 --decode > android/app/keystore.jks
          echo "${{ secrets.PLAY_STORE_KEY }}" > android/play-store-key.json

      - name: Build AAB
        run: flutter build appbundle --release

      # Upload to Play Store
      - name: Upload to Play Store
        uses: r0adkll/upload-google-play@v1
        with:
          serviceAccountJson: android/play-store-key.json
          packageName: com.example.myapp
          releaseFiles: build/app/outputs/bundle/release/app-release.aab
          track: internal
          status: completed
          changesNotSentForReview: true
```

**Using Fastlane:**
```ruby
# android/fastlane/Fastfile
lane :internal do
  upload_to_play_store(
    track: 'internal',
    aab: '../build/app/outputs/bundle/release/app-release.aab',
    json_key: 'play-store-key.json',
    skip_upload_changelogs: true
  )
end
```

---

**26. What caching strategies can be used to speed up Flutter builds in CI/CD?**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Cache Flutter SDK
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.16.0'
          cache: true  # Built-in caching

      # Cache pub packages
      - name: Cache pub packages
        uses: actions/cache@v4
        with:
          path: |
            ~/.pub-cache
            .dart_tool
          key: ${{ runner.os }}-pub-${{ hashFiles('**/pubspec.lock') }}
          restore-keys: |
            ${{ runner.os }}-pub-

      # Cache Gradle (Android)
      - name: Cache Gradle
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*', '**/gradle-wrapper.properties') }}
          restore-keys: |
            ${{ runner.os }}-gradle-

      # Cache CocoaPods (iOS)
      - name: Cache CocoaPods
        uses: actions/cache@v4
        with:
          path: ios/Pods
          key: ${{ runner.os }}-pods-${{ hashFiles('**/Podfile.lock') }}
          restore-keys: |
            ${{ runner.os }}-pods-

      - run: flutter pub get
      - run: flutter build apk
```

**Additional tips:**
- Use `--no-pub` if already cached
- Split into multiple jobs (parallel)
- Use self-hosted runners with persistent cache

---

**27. How do you handle different environment variables for different build flavors?**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        flavor: [dev, staging, prod]

    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - name: Set environment variables
        run: |
          case ${{ matrix.flavor }} in
            dev)
              echo "API_URL=https://dev-api.example.com" >> $GITHUB_ENV
              echo "API_KEY=${{ secrets.DEV_API_KEY }}" >> $GITHUB_ENV
              ;;
            staging)
              echo "API_URL=https://staging-api.example.com" >> $GITHUB_ENV
              echo "API_KEY=${{ secrets.STAGING_API_KEY }}" >> $GITHUB_ENV
              ;;
            prod)
              echo "API_URL=https://api.example.com" >> $GITHUB_ENV
              echo "API_KEY=${{ secrets.PROD_API_KEY }}" >> $GITHUB_ENV
              ;;
          esac

      - name: Build
        run: |
          flutter build apk \
            --flavor ${{ matrix.flavor }} \
            --dart-define=API_URL=$API_URL \
            --dart-define=API_KEY=$API_KEY
```

**Using .env files:**
```yaml
- name: Create .env file
  run: |
    cat > .env.${{ matrix.flavor }} <<EOF
    API_URL=${{ secrets[format('{0}_API_URL', matrix.flavor)] }}
    API_KEY=${{ secrets[format('{0}_API_KEY', matrix.flavor)] }}
    EOF

- name: Build
  run: flutter build apk --flavor ${{ matrix.flavor }}
```

---

**28. What is Bitrise and how does it compare to other CI/CD platforms for Flutter?**

**Bitrise** is a mobile-focused CI/CD platform.

**Comparison:**

| Feature | Bitrise | GitHub Actions | Codemagic |
|---------|---------|----------------|-----------|
| Flutter focus | Good | Generic | Excellent |
| macOS runners | Yes | Yes | Yes |
| Visual workflow editor | Yes | No | Yes |
| Pre-built steps | Many mobile | General | Flutter-specific |
| Pricing | Per build min | Per min | Per build min |
| Self-hosted | No | Yes | No |

**Bitrise workflow (bitrise.yml):**
```yaml
format_version: "11"
default_step_lib_source: https://github.com/bitrise-io/bitrise-steplib.git

workflows:
  primary:
    steps:
      - git-clone@6: {}

      - flutter-installer@0:
          inputs:
            - version: stable

      - flutter-analyze@0:
          inputs:
            - project_location: $BITRISE_SOURCE_DIR

      - flutter-test@1:
          inputs:
            - project_location: $BITRISE_SOURCE_DIR

      - flutter-build@0:
          inputs:
            - project_location: $BITRISE_SOURCE_DIR
            - platform: android
            - android_output_type: apk

      - deploy-to-bitrise-io@2: {}
```

---

**29. How do you integrate code quality checks (linting, formatting) into CI/CD?**

```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - name: Install dependencies
        run: flutter pub get

      # Check formatting
      - name: Check formatting
        run: dart format --set-exit-if-changed .

      # Analyze code
      - name: Analyze code
        run: flutter analyze --fatal-infos

      # Custom lint rules (if using custom_lint)
      - name: Run custom lints
        run: dart run custom_lint

      # Check for outdated packages
      - name: Check outdated packages
        run: flutter pub outdated --no-dev-dependencies

      # Check for security vulnerabilities
      - name: Security scan
        run: |
          dart pub global activate dependency_validator
          dart pub global run dependency_validator

  # Separate job for Dart metrics
  metrics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install DCM
        run: |
          dart pub global activate dart_code_metrics
          dart pub global run dart_code_metrics:metrics \
            analyze lib \
            --reporter=github

      - name: Check cyclomatic complexity
        run: |
          dart pub global run dart_code_metrics:metrics \
            check-unnecessary-nullable lib \
            --fatal-found
```

**analysis_options.yaml:**
```yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  errors:
    missing_return: error
    missing_required_param: error
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"

linter:
  rules:
    - prefer_const_constructors
    - prefer_final_locals
    - avoid_print
```

---

**30. What is the purpose of the pubspec.lock file in CI/CD pipelines?**

**pubspec.lock** locks exact package versions for reproducible builds.

**Why important in CI/CD:**
1. **Reproducibility**: Same versions every build
2. **Consistency**: Team uses identical dependencies
3. **Security**: Known working versions
4. **Debugging**: Can reproduce any build

```yaml
# Should commit pubspec.lock for apps
# Should NOT commit for packages

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # This uses exact versions from pubspec.lock
      - run: flutter pub get

      # To update dependencies (in separate workflow)
      - run: flutter pub upgrade
```

**Best practices:**
- **Apps**: Commit `pubspec.lock` ✅
- **Packages**: Don't commit, use ranges
- **CI**: Never use `--upgrade` in build pipeline
- **Updates**: Separate PR for dependency updates

---

## Advanced Level

**31. How do you implement automated versioning and build number incrementation in CI/CD?**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for versioning

      - uses: subosito/flutter-action@v2

      # Method 1: Use GitHub run number
      - name: Set version
        run: |
          VERSION="1.0.${{ github.run_number }}"
          BUILD_NUMBER="${{ github.run_number }}"
          flutter build apk \
            --build-name=$VERSION \
            --build-number=$BUILD_NUMBER

      # Method 2: Git-based versioning
      - name: Auto version from git
        run: |
          # Count commits
          BUILD_NUMBER=$(git rev-list --count HEAD)
          # Get latest tag or default
          VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "1.0.0")
          flutter build apk \
            --build-name=$VERSION \
            --build-number=$BUILD_NUMBER

      # Method 3: Using cider package
      - name: Version with cider
        run: |
          dart pub global activate cider
          cider bump build
          cider version
          flutter build apk
```

**Semantic versioning with tags:**
```yaml
- name: Calculate version
  id: version
  run: |
    if [[ $GITHUB_REF == refs/tags/v* ]]; then
      VERSION=${GITHUB_REF#refs/tags/v}
    else
      VERSION="1.0.0-dev.${{ github.run_number }}"
    fi
    echo "version=$VERSION" >> $GITHUB_OUTPUT

- name: Build with version
  run: |
    flutter build apk --build-name=${{ steps.version.outputs.version }}
```

---

**32. What are the best practices for managing secrets and sensitive data in CI/CD pipelines?**

**1. Use platform secret management:**
```yaml
# GitHub Secrets - encrypted at rest
env:
  API_KEY: ${{ secrets.API_KEY }}
```

**2. Minimize secret exposure:**
```yaml
- name: Use secret
  run: |
    # Good - use in environment
    echo "Using API"
  env:
    API_KEY: ${{ secrets.API_KEY }}

    # Bad - don't echo secrets!
    # echo ${{ secrets.API_KEY }}
```

**3. Encode binary files:**
```bash
# Encode
base64 -i keystore.jks -o keystore.base64

# In CI, decode
echo "${{ secrets.KEYSTORE }}" | base64 --decode > keystore.jks
```

**4. Cleanup sensitive files:**
```yaml
- name: Cleanup
  if: always()  # Run even on failure
  run: |
    rm -f keystore.jks
    rm -f key.properties
    rm -f google-services.json
```

**5. Use OIDC for cloud providers:**
```yaml
permissions:
  id-token: write
  contents: read

- uses: google-github-actions/auth@v1
  with:
    workload_identity_provider: 'projects/123/locations/global/...'
    service_account: 'sa@project.iam.gserviceaccount.com'
```

**6. Rotate secrets regularly**
**7. Use different secrets per environment**
**8. Audit secret usage**

---

**33. How do you set up a multi-stage deployment pipeline (dev → staging → production)?**

```yaml
name: Multi-Stage Deployment

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy to'
        required: true
        default: 'staging'
        type: choice
        options: [staging, production]

jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter build apk --release
      - uses: actions/upload-artifact@v4
        with:
          name: app
          path: build/app/outputs/flutter-apk/app-release.apk

  deploy-dev:
    needs: build
    runs-on: ubuntu-latest
    environment: dev
    steps:
      - uses: actions/download-artifact@v4
      - name: Deploy to Dev
        run: |
          # Deploy to Firebase App Distribution
          echo "Deploying to dev..."

  deploy-staging:
    needs: deploy-dev
    runs-on: ubuntu-latest
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - uses: actions/download-artifact@v4
      - name: Deploy to Staging
        run: |
          # Deploy to internal track
          echo "Deploying to staging..."

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    # Require manual approval
    steps:
      - uses: actions/download-artifact@v4
      - name: Deploy to Production
        run: |
          # Deploy to production track
          echo "Deploying to production..."
```

---

**34. What strategies can you use to optimize build times in CI/CD pipelines?**

**1. Caching:**
```yaml
- uses: subosito/flutter-action@v2
  with:
    cache: true

- uses: actions/cache@v4
  with:
    path: |
      ~/.pub-cache
      .dart_tool
      ~/.gradle
      ios/Pods
    key: ${{ runner.os }}-flutter-${{ hashFiles('**/pubspec.lock') }}
```

**2. Parallel jobs:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
  build-android:
    runs-on: ubuntu-latest
  build-ios:
    runs-on: macos-latest
  # All run in parallel
```

**3. Skip unnecessary steps:**
```yaml
- name: Build
  if: github.event_name == 'push'
  run: flutter build apk
```

**4. Use faster runners:**
```yaml
runs-on: ubuntu-latest  # or larger runners
# GitHub: ubuntu-latest-4-cores
```

**5. Incremental builds:**
```bash
# Only rebuild changed code
flutter build apk --no-tree-shake-icons
```

**6. Split tests:**
```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: |
      flutter test --shard-index=${{ matrix.shard }} --total-shards=4
```

**7. Skip iOS simulator boot:**
```yaml
# Use pre-booted simulator
- run: xcrun simctl boot "iPhone 15" || true
```

---

**35. How do you implement automated screenshot testing in CI/CD?**

```yaml
name: Golden Tests

on: [push, pull_request]

jobs:
  golden-tests:
    runs-on: macos-latest  # Consistent rendering
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter pub get

      # Run golden tests
      - name: Run golden tests
        run: flutter test --tags=golden

      # Update goldens (on main branch only)
      - name: Update goldens
        if: github.ref == 'refs/heads/main' && failure()
        run: flutter test --update-goldens --tags=golden

      # Upload failures as artifact
      - name: Upload failures
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: golden-failures
          path: |
            **/failures/*.png
            **/goldens/*.png

      # Commit updated goldens
      - name: Commit updated goldens
        if: github.ref == 'refs/heads/main'
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add test/**/goldens/
          git diff --staged --quiet || git commit -m "Update golden files"
          git push
```

**Golden test example:**
```dart
testWidgets('HomeScreen golden test', (tester) async {
  await tester.pumpWidget(MyApp());
  await expectLater(
    find.byType(HomeScreen),
    matchesGoldenFile('goldens/home_screen.png'),
  );
}, tags: 'golden');
```

---

**36. What is a deployment gate and how would you implement one in Flutter CI/CD?**

**Deployment gates** are checks that must pass before deployment proceeds.

```yaml
name: Deploy with Gates

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter build apk

  # Gate 1: Test coverage
  coverage-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter test --coverage
      - name: Check coverage threshold
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info | grep 'lines' | awk '{print $2}' | tr -d '%')
          if (( $(echo "$COVERAGE < 80" | bc -l) )); then
            echo "Coverage $COVERAGE% is below 80%"
            exit 1
          fi

  # Gate 2: Security scan
  security-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run security scan
        run: |
          # Check for known vulnerabilities
          flutter pub outdated --json | jq '.packages[] | select(.latest.isDiscontinued == true)'

  # Gate 3: Performance check
  performance-gate:
    runs-on: ubuntu-latest
    steps:
      - name: Check app size
        run: |
          SIZE=$(stat -f%z build/app/outputs/flutter-apk/app-release.apk)
          MAX_SIZE=50000000  # 50MB
          if [ $SIZE -gt $MAX_SIZE ]; then
            echo "APK size exceeds limit"
            exit 1
          fi

  # Gate 4: Manual approval (using environment)
  deploy:
    needs: [build, coverage-gate, security-gate, performance-gate]
    runs-on: ubuntu-latest
    environment:
      name: production  # Requires approval
    steps:
      - name: Deploy
        run: echo "Deploying..."
```

---

**37. How do you handle rollback strategies in automated Flutter deployments?**

```yaml
name: Deploy with Rollback

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Save current version for potential rollback
      - name: Record current version
        id: current
        run: |
          CURRENT=$(gcloud app versions list --sort-by=~version.createTime --limit=1 --format='value(version.id)')
          echo "version=$CURRENT" >> $GITHUB_OUTPUT

      - name: Deploy new version
        id: deploy
        run: |
          flutter build apk
          # Deploy to Play Store
          fastlane deploy
        continue-on-error: true

      # Health check
      - name: Health check
        id: health
        if: steps.deploy.outcome == 'success'
        run: |
          # Wait for rollout
          sleep 60
          # Check crash rate
          CRASH_RATE=$(firebase crashlytics:get-crash-rate)
          if (( $(echo "$CRASH_RATE > 1" | bc -l) )); then
            echo "High crash rate detected"
            exit 1
          fi
        continue-on-error: true

      # Rollback if health check fails
      - name: Rollback
        if: steps.health.outcome == 'failure'
        run: |
          echo "Rolling back to ${{ steps.current.outputs.version }}"
          # Rollback Play Store
          fastlane rollback version:${{ steps.current.outputs.version }}

      - name: Notify on rollback
        if: steps.health.outcome == 'failure'
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {"text": "⚠️ Deployment rolled back due to health check failure"}
```

---

**38. What are the best practices for implementing notifications and reporting in CI/CD?**

```yaml
name: CI with Notifications

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter test --machine > test-results.json
        continue-on-error: true

      # Publish test results
      - name: Publish Test Results
        uses: EnricoMi/publish-unit-test-result-action@v2
        with:
          files: test-results.json

      - run: flutter build apk

  notify:
    needs: build
    if: always()
    runs-on: ubuntu-latest
    steps:
      # Slack notification
      - name: Slack Notification
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "${{ needs.build.result == 'success' && '✅' || '❌' }} Build *${{ github.ref_name }}*\n${{ github.event.head_commit.message }}"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

      # Discord notification
      - name: Discord Notification
        uses: sarisia/actions-status-discord@v1
        with:
          webhook: ${{ secrets.DISCORD_WEBHOOK }}
          status: ${{ needs.build.result }}

      # Email on failure
      - name: Send failure email
        if: needs.build.result == 'failure'
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 465
          username: ${{ secrets.EMAIL_USERNAME }}
          password: ${{ secrets.EMAIL_PASSWORD }}
          subject: Build Failed - ${{ github.repository }}
          to: team@example.com
          body: |
            Build failed for ${{ github.ref_name }}
            Commit: ${{ github.sha }}
            See: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

---

**39. How do you configure parallel builds for iOS and Android in the same pipeline?**

```yaml
name: Parallel Platform Builds

on:
  push:
    branches: [main]

jobs:
  # Shared setup job
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          cache: true

      - run: flutter pub get

      # Cache dependencies for other jobs
      - uses: actions/cache/save@v4
        with:
          path: |
            ~/.pub-cache
            .dart_tool
          key: deps-${{ github.sha }}

  test:
    needs: setup
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - uses: actions/cache/restore@v4
        with:
          path: |
            ~/.pub-cache
            .dart_tool
          key: deps-${{ github.sha }}
      - run: flutter test

  # Parallel builds
  build-android:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - uses: actions/cache/restore@v4
        with:
          path: ~/.pub-cache
          key: deps-${{ github.sha }}

      - run: flutter build apk --release
      - uses: actions/upload-artifact@v4
        with:
          name: android-build
          path: build/app/outputs/flutter-apk/

  build-ios:
    needs: test
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter build ios --release --no-codesign
      - uses: actions/upload-artifact@v4
        with:
          name: ios-build
          path: build/ios/iphoneos/

  build-web:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - run: flutter build web --release
      - uses: actions/upload-artifact@v4
        with:
          name: web-build
          path: build/web/

  # Deploy after all builds complete
  deploy:
    needs: [build-android, build-ios, build-web]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - name: Deploy all platforms
        run: echo "Deploying..."
```

---

**40. What is CircleCI and how do you configure it for Flutter projects?**

**CircleCI** is a popular CI/CD platform with Docker support.

**.circleci/config.yml:**
```yaml
version: 2.1

orbs:
  flutter: circleci/flutter@2.0.0

executors:
  flutter-executor:
    docker:
      - image: circleci/android:api-30
    resource_class: large

jobs:
  test:
    executor: flutter-executor
    steps:
      - checkout
      - flutter/install_sdk_and_pub:
          version: 3.16.0
      - run:
          name: Run tests
          command: flutter test --coverage
      - store_test_results:
          path: test-results
      - store_artifacts:
          path: coverage

  build-android:
    executor: flutter-executor
    steps:
      - checkout
      - flutter/install_sdk_and_pub:
          version: 3.16.0
      - run:
          name: Build APK
          command: flutter build apk --release
      - store_artifacts:
          path: build/app/outputs/flutter-apk

  build-ios:
    macos:
      xcode: 15.0.0
    steps:
      - checkout
      - flutter/install_sdk_and_pub:
          version: 3.16.0
      - run:
          name: Build iOS
          command: flutter build ios --release --no-codesign
      - store_artifacts:
          path: build/ios/iphoneos

workflows:
  build-and-test:
    jobs:
      - test
      - build-android:
          requires:
            - test
      - build-ios:
          requires:
            - test
      - deploy:
          requires:
            - build-android
            - build-ios
          filters:
            branches:
              only: main
```

---

**41. How do you implement automated release notes generation in CI/CD?**

```yaml
name: Release with Notes

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      # Generate changelog from commits
      - name: Generate Changelog
        id: changelog
        run: |
          PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREVIOUS_TAG" ]; then
            CHANGELOG=$(git log --oneline --pretty=format:"- %s")
          else
            CHANGELOG=$(git log --oneline --pretty=format:"- %s" $PREVIOUS_TAG..HEAD)
          fi
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGELOG" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      # Using conventional commits
      - name: Generate Conventional Changelog
        uses: TriPSs/conventional-changelog-action@v4
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          output-file: CHANGELOG.md

      - uses: subosito/flutter-action@v2
      - run: flutter build apk --release

      # Create GitHub Release
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          body: |
            ## What's Changed
            ${{ steps.changelog.outputs.changelog }}

            ## Downloads
            - APK: See assets below
          files: |
            build/app/outputs/flutter-apk/app-release.apk
          draft: false
          prerelease: ${{ contains(github.ref, 'beta') }}

      # Update Play Store release notes
      - name: Update Play Store Notes
        run: |
          mkdir -p fastlane/metadata/android/en-US/changelogs/
          echo "${{ steps.changelog.outputs.changelog }}" > \
            fastlane/metadata/android/en-US/changelogs/${{ github.run_number }}.txt
```

---

**42. What are the security considerations when setting up CI/CD for Flutter apps?**

**1. Secret Management:**
```yaml
# Use encrypted secrets
env:
  API_KEY: ${{ secrets.API_KEY }}

# Don't expose in logs
- run: |
    # Bad
    echo ${{ secrets.API_KEY }}

    # Good - mask in logs
    echo "::add-mask::${{ secrets.API_KEY }}"
```

**2. Dependency Security:**
```yaml
- name: Security audit
  run: |
    # Check for vulnerabilities
    flutter pub outdated

    # Use dependabot
    # .github/dependabot.yml
```

**3. Code Signing Security:**
```yaml
# Store signing keys securely
- name: Secure keystore handling
  run: |
    echo "${{ secrets.KEYSTORE }}" | base64 -d > keystore.jks
    # Use and delete
    flutter build apk
    rm -f keystore.jks
```

**4. Branch Protection:**
```yaml
# Require reviews before merge
# Require CI to pass
# Protect secrets from forks
if: github.event.pull_request.head.repo.full_name == github.repository
```

**5. Least Privilege:**
```yaml
permissions:
  contents: read  # Minimum needed
  # Don't use: write-all
```

**6. Environment Isolation:**
```yaml
environment:
  name: production
  # Require approval for production
```

---

**43. How do you handle native dependencies and plugins in CI/CD pipelines?**

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      # Java for Android
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      # Android SDK
      - name: Setup Android SDK
        uses: android-actions/setup-android@v3

      # Accept licenses
      - name: Accept Android licenses
        run: yes | sdkmanager --licenses

      # NDK for native code
      - name: Install NDK
        run: sdkmanager "ndk;25.1.8937393"

      - uses: subosito/flutter-action@v2
      - run: flutter pub get

      # For plugins with native dependencies
      - name: Install native dependencies
        run: |
          # For audio plugins
          sudo apt-get install -y libasound2-dev

          # For image processing
          sudo apt-get install -y libpng-dev libjpeg-dev

      - run: flutter build apk

  build-ios:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # CocoaPods for iOS
      - name: Install CocoaPods
        run: |
          cd ios
          pod install --repo-update

      # Xcode selection
      - uses: maxim-lobanov/setup-xcode@v1
        with:
          xcode-version: '15.0'

      - run: flutter build ios --no-codesign
```

---

**44. What monitoring and analytics should be integrated into CI/CD pipelines?**

```yaml
name: CI with Monitoring

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      # Build timing
      - name: Build with timing
        run: |
          START=$(date +%s)
          flutter build apk
          END=$(date +%s)
          echo "Build time: $((END-START)) seconds"

      # Test metrics
      - name: Run tests with coverage
        run: flutter test --coverage --machine > test-results.json

      # Upload coverage
      - uses: codecov/codecov-action@v3
        with:
          files: coverage/lcov.info

      # App size analysis
      - name: Analyze APK size
        run: |
          APK_SIZE=$(stat -f%z build/app/outputs/flutter-apk/app-release.apk)
          echo "APK Size: $((APK_SIZE/1024/1024))MB"

          # Track over time
          curl -X POST "${{ secrets.METRICS_ENDPOINT }}" \
            -d "{\"metric\":\"apk_size\",\"value\":$APK_SIZE}"

      # Dart analyzer metrics
      - name: Code metrics
        run: |
          dart pub global activate dart_code_metrics
          dart pub global run dart_code_metrics:metrics analyze lib \
            --reporter=json > metrics.json

      # Upload to dashboard
      - name: Upload metrics
        run: |
          curl -X POST "${{ secrets.DASHBOARD_URL }}" \
            -H "Content-Type: application/json" \
            -d @metrics.json

  # Performance testing
  performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - name: Run performance tests
        run: |
          flutter drive --driver=test_driver/perf_driver.dart \
            --target=integration_test/perf_test.dart

      - name: Upload performance results
        uses: actions/upload-artifact@v4
        with:
          name: performance-results
          path: build/perf_*.json
```

---

**45. How do you implement A/B testing deployment strategies using CI/CD?**

```yaml
name: A/B Testing Deployment

on:
  push:
    branches: [main]

jobs:
  build-variants:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        variant: [control, treatment-a, treatment-b]
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2

      - name: Build variant
        run: |
          flutter build apk \
            --dart-define=AB_VARIANT=${{ matrix.variant }} \
            --dart-define=AB_TEST_ID=${{ github.run_id }}

      - uses: actions/upload-artifact@v4
        with:
          name: app-${{ matrix.variant }}
          path: build/app/outputs/flutter-apk/app-release.apk

  deploy-ab-test:
    needs: build-variants
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4

      # Deploy control to 80% of users
      - name: Deploy control
        run: |
          # Using Play Store staged rollout
          fastlane supply \
            --aab app-control/app-release.apk \
            --track production \
            --rollout 0.8

      # Deploy treatment to 10% each
      - name: Deploy treatments
        run: |
          # Using Firebase App Distribution for A/B
          firebase appdistribution:distribute app-treatment-a/app-release.apk \
            --groups "ab-test-a"
          firebase appdistribution:distribute app-treatment-b/app-release.apk \
            --groups "ab-test-b"

      # Configure Remote Config for A/B
      - name: Setup Remote Config
        run: |
          firebase remoteconfig:rollout \
            --parameter ab_test_variant \
            --percentage-value control:80,treatment-a:10,treatment-b:10

  analyze-results:
    needs: deploy-ab-test
    runs-on: ubuntu-latest
    # Run after test period
    if: github.event.schedule
    steps:
      - name: Fetch analytics
        run: |
          # Get metrics from Firebase Analytics
          bq query --format=json '
            SELECT
              ab_variant,
              COUNT(*) as users,
              AVG(conversion_rate) as conversion
            FROM analytics
            WHERE test_id = "${{ github.run_id }}"
            GROUP BY ab_variant
          ' > results.json

      - name: Determine winner
        run: |
          WINNER=$(jq -r 'max_by(.conversion) | .ab_variant' results.json)
          echo "Winner: $WINNER"
          # Rollout winner to 100%
```

**In Flutter code:**
```dart
// main.dart
void main() {
  const variant = String.fromEnvironment('AB_VARIANT', defaultValue: 'control');

  runApp(MyApp(abVariant: variant));
}

class MyApp extends StatelessWidget {
  final String abVariant;

  const MyApp({required this.abVariant});

  @override
  Widget build(BuildContext context) {
    // Use variant to show different features
    return MaterialApp(
      home: abVariant == 'treatment-a'
          ? NewHomeScreen()
          : OriginalHomeScreen(),
    );
  }
}
```
