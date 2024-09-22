import { useState, Fragment } from "react";
import {
  Button,
  Image,
  View,
  StyleSheet,
  Modal,
  Pressable,
  TouchableOpacity,
  Text,
} from "react-native";
import * as ImagePicker from "expo-image-picker";
import { useExtractReceipts } from "@/hooks/api/useExtractReceipts";
import MaterialIcons from "@expo/vector-icons/build/MaterialIcons";
import { useNavigation } from "expo-router";

export default function MyGallery() {
  const [images, setImage] = useState<ImagePicker.ImagePickerAsset[] | null>(
    null
  );
  const [selectedImage, setSelectedImage] =
    useState<ImagePicker.ImagePickerAsset | null>(null);
  const [isVisible, setIsVisible] = useState(false);
  const { responseMessage, extractReceipts } = useExtractReceipts();
  const SPACING = 10;
  const THUMB_SIZE = 80;

  const pickImage = async () => {
    let result: ImagePicker.ImagePickerResult =
      await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.All,
        allowsEditing: true,
        aspect: [4, 3],
        allowsMultipleSelection: true,
        quality: 1,
      });

    if (!result.canceled) {
      setImage(result.assets);
    }
  };


  const handleImagePress = (image: ImagePicker.ImagePickerAsset) => {
    setSelectedImage(image);
    setIsVisible(true);
  };

  const { navigate } = useNavigation();
  return (
    <Fragment>
      <View style={styles.container}>
        <Button title="Pick Images from camera roll" onPress={pickImage} />
        {images &&
          images.map((image,index) => {
            return (
              <TouchableOpacity
                onPress={() => handleImagePress(image)}
                key={index}
              >
                <Image
                  source={{ uri: image.uri }}
                  style={styles.image}
                  key={index}
                />
              </TouchableOpacity>
            );
          })}
        <View style={styles.margin10}>
          <Button
            title="Submit Receipt"
            onPress={() => extractReceipts(images)}
          />
        </View>
      </View>
      <Modal animationType="slide" transparent={true} visible={isVisible}>
        <View style={styles.modalContent}>
          <Image
            source={{ uri: selectedImage?.uri }}
            style={styles.largeImage}
          />
          <Pressable
            onPress={() => setIsVisible(false)}
            style={styles.closeButton}
          >
            <MaterialIcons name="close" color="#fff" size={22} />
          </Pressable>
        </View>
      </Modal>
    </Fragment>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  margin10: {
    margin: 10,
  },
  image: {
    width: 200,
    height: 200,
    margin: 4,
    borderRadius: 2,
    borderWidth: 1,
    borderColor: "#2096F3",
  },
  largeImage: {
    width: "100%",
    height: 300,
    resizeMode: "contain",
  },
  closeButton: {
    position: "absolute",
    top: 10,
    right: 10,
  },
  modalContent: {
    flex: 1,
    backgroundColor: "rgba(0, 0, 0, 0.5)",
    justifyContent: "center",
    alignItems: "center",
  },
});
