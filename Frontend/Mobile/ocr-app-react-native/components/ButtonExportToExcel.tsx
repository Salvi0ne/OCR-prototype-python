import ReceiptItem from "@/constants/Interface/receiptItem";
import React, { Fragment } from "react";
import {
  Button,
  StyleProp,
  TextStyle,
  View,
  Alert,
  Platform,
} from "react-native";
// import XLSX from 'xlsx';
// import RNFS from 'react-native-fs';
import * as FileSystem from "expo-file-system";
import { basedUrlApiLocalhost } from "@/constants/Api";
import { shareAsync } from "expo-sharing";
import {
  saveToLibraryAsync,
  requestPermissionsAsync,
} from "expo-media-library";

const ButtonExportToExcel = ({
  receipts,
  style = {},
}: {
  receipts: ReceiptItem[];
  style?: StyleProp<TextStyle> | TextStyle;
}) => {
  const downloadExcel = async () => {
    const url = basedUrlApiLocalhost + "/get-data-excel"; // Flask API URL for Excel
    const fileUri = FileSystem.documentDirectory + "employees.xlsx"; // Path to save the file locally
    console.log("url:", url, fileUri);
    try {
      // Download the file
      const fileName = "employees.xlsx";
      const url = basedUrlApiLocalhost + "/get-data-excel";
      // const fileUri = FileSystem.documentDirectory + '/receipts.xlsx';

      const downloadResult = await FileSystem.downloadAsync(
        url,
        FileSystem.documentDirectory + fileName
      );

      //  console.log(downloadResult,'::downRes::');
      //  NOT SUPPORT BY WEB!
      await save(
        downloadResult.uri,
        fileName,
        downloadResult.headers["Content-Type"]
      );

    } catch (error) {
      Alert.alert("Error", "An error occurred while downloading the file 2");
      console.error(error);
    }
  };

  const save = async (uri: any, filename: any, mimetype: any) => {
    if (Platform.OS === "android") {
      const permissions =
        await FileSystem.StorageAccessFramework.requestDirectoryPermissionsAsync();
      if (permissions.granted) {
        const base64 = await FileSystem.readAsStringAsync(uri, {
          encoding: FileSystem.EncodingType.Base64,
        });
        await FileSystem.StorageAccessFramework.createFileAsync(
          permissions.directoryUri,
          filename,
          mimetype
        )
          .then(async (uri) => {
            await FileSystem.writeAsStringAsync(uri, base64, {
              encoding: FileSystem.EncodingType.Base64,
            });
            Alert.alert("Success", "File saved successfully!", [
              { text: "OK" },
            ]);
          })
          .catch((e) => console.log(e));
      } else {
        shareAsync(uri);
      }
    } else {
      shareAsync(uri);
    }
  };

  return (
    <View style={style}>
      <Button
        title="Export to Excel"
        onPress={downloadExcel}
        color={"green"}
      ></Button>
    </View>
  );
};

export default ButtonExportToExcel;
