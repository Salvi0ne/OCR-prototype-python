# Frontend - OCR React Native

## Issues and Problems

- **Android Emulator Camera Issue**: The Android emulator captures a black screen when using the camera.
- **Limited Functionality on Android Devices**: Both the emulator and physical Android devices can't fully function. The web version works fine, including the camera, but this is not ideal since the web camera often captures text upside down.
- **No iOS Testing**: The iPhone version has not been tested on Xcode yet.
- **File Upload Issues**: Unable to send files through the API from both the Android phone and emulator. File uploads only work on the web.
- **Lack of Tests**: There are few to no tests implemented for the app.
- **Core Functionality Incomplete**: Due to file upload issues, essential features such as extracting data from receipts, capturing receipts with the camera, and the extract button are not functioning as intended.

## Author's Note

This is an unfinished prototype. I need more time to learn and refine the app. React Native has a steep learning curve for me, and my lack of experience has resulted in an incomplete product. However, I plan to update and fix issues over time.

## Prerequisites

- Install [Node.js](https://nodejs.org/), ensuring npm (Node Package Manager) is available.
- Install project dependencies:
    ```bash
    npm install
    ```

## Getting Started

To start the development server:
```bash
npm run start


### Expo
- [development build](https://docs.expo.dev/develop/development-builds/introduction/)
- [Android emulator](https://docs.expo.dev/workflow/android-studio-emulator/)
- [iOS simulator](https://docs.expo.dev/workflow/ios-simulator/)



