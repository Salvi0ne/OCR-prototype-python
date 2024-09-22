import { Image, StyleSheet, Platform, Button, View, Text } from "react-native";
import ParallaxScrollView from "@/components/ParallaxScrollView";
import { ThemedText } from "@/components/ThemedText";
import { ThemedView } from "@/components/ThemedView";
import { useGetVerifiedReceipts } from "@/hooks/api/useGetVerifiedReceipts";
import ReceiptsComponent from "@/components/ReceiptsComponent";
import { Fragment } from "react";
import ButtonExportToExcel from "@/components/ButtonExportToExcel";

export default function HomeScreen() {
  const { receipts, setReceipts } = useGetVerifiedReceipts();

  return (
    <Fragment>
      <View style={styles.stepContainer}>
        <Text style={styles.textHeader}> Home  - OCR Prototype </Text>
        <ReceiptsComponent receipts={receipts} setReceipts={setReceipts} />
        {/* 
        //! INCOMPLETE EXPORT TO EXCEL Due to unable to test with emulator or with web or with phone thru expo
        //! REMOVE THIS COMMENT IF ABLE TO FIX & TEST THIS COMPONENT!
        <ButtonExportToExcel receipts={receipts} style={styles.buttonExcel} /> */}
      </View>
    </Fragment>
  );
}

const styles = StyleSheet.create({
  titleContainer: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  margin: {
    margin: 8,
  },
  textHeader: { fontSize: 20, fontWeight: "bold", paddingLeft: 16, paddingTop: 16 },
  text: { fontSize: 16, fontWeight: "bold", paddingLeft: 16, paddingTop: 16 },
  stepContainer: {
    gap: 8,
    marginBottom: 8,

  },
  buttonExcel: {
    padding: 10,
    width: 220,
    alignSelf: "center",
  },
  reactLogo: {
    height: 178,
    width: 290,
    bottom: 0,
    left: 0,
    position: "absolute",
  },
});
