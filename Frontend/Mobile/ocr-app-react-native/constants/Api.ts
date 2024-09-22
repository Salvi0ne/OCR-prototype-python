import { Platform } from "react-native";

export const basedUrlLocalhost = Platform.select({
    ios: "http://localhost:5001",
    android: "http://10.0.2.2:5001",
    web: "http://localhost:5001",
});

// export const basedUrlLocalhost = "https://4fae-175-143-188-207.ngrok-free.app";  // ngrok must change after run ngrok on the device
export const emulatorApiLocahost = `http://10.0.2.2:5001/api`;
export const basedUrlApiLocalhost = `${basedUrlLocalhost}/api`;
// http://10.0.2.2:5001/api/receipts/unverified
