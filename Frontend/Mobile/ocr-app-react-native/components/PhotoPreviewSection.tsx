import { useExtractReceipts } from "@/hooks/api/useExtractReceipts";
import { Fontisto } from "@expo/vector-icons";
import { CameraCapturedPicture } from "expo-camera";
import React from "react";
import {
  TouchableOpacity,
  SafeAreaView,
  Image,
  StyleSheet,
  View,
  Text,
  Dimensions
} from "react-native";

interface PhotoPreviewSectionProps {
  photo: CameraCapturedPicture;
  handleRetakePhoto: () => void;
  onPhotoLoaded: (photo: CameraCapturedPicture) => void;
}

const PhotoPreviewSection: React.FC<PhotoPreviewSectionProps> = ({
  photo,
  handleRetakePhoto,
  onPhotoLoaded,
}) => {

    const { extraReceiptFromCamera } = useExtractReceipts();

    function handleSubmit() {
        extraReceiptFromCamera(photo)
    }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.box}>
        {/* <Image style={styles.previewContainer} source={{ uri: photo.uri }} /> */}
        {/* <Image style={styles.previewContainer} source={{ uri: 'data:image/jpg;base64,'+ photo.base64 + ".jpg" }} /> */}
      <Text>12345678</Text>

        <Image style={styles.previewContainer} source={{ uri: 'data:image/jpg;base64,'+ photo.base64 }} />
      </View>
      <View style={styles.buttonContainer}>
        <TouchableOpacity style={styles.button} onPress={handleRetakePhoto}>
          <Fontisto name="trash" size={36} color="black" />
        </TouchableOpacity>
        <TouchableOpacity style={styles.button} onPress={handleSubmit}>
          <Fontisto name="check" size={36} color="black" />
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
};

const screenWidth = Dimensions.get('window').width;
const screenHeight = Dimensions.get('window').height;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "black",
    alignItems: "center",
    justifyContent: "center",
  },
  box: {
    borderRadius: 15,
    padding: 1,
    // width: "95%",
    // width: 300,
    width: screenWidth * 0.75, // 95% of screen width
    height: screenHeight * 0.75, // 85% of screen height
    // height: 400, 
    backgroundColor: "darkgray",
    justifyContent: "center",
    alignItems: "center",
  },
  previewContainer: {
    width: "95%",
    height: "85%",
    borderRadius: 15,
  },
  buttonContainer: {
    marginTop: "4%",
    flexDirection: "row",
    justifyContent: "center",
    width: "100%",
    gap: 20,
  },
  button: {
    backgroundColor: "gray",
    borderRadius: 25,
    padding: 10,
    alignItems: "center",
    justifyContent: "center",
  },
});

export default PhotoPreviewSection;