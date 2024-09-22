import {
  CameraView,
  Camera,
  CameraType,
  useCameraPermissions,
  CameraCapturedPicture,
} from "expo-camera";
import { useEffect, useRef, useState } from "react";
import {
  Button,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Image,
} from "react-native";
import {
  saveToLibraryAsync,
  usePermissions as useMediaPermissions,
} from "expo-media-library";
import { basedUrlApiLocalhost, basedUrlLocalhost } from "@/constants/Api";
import axios from "axios";
import { useExtractReceipts } from "@/hooks/api/useExtractReceipts";

export default function CameraTab() {
  const [facing, setFacing] = useState<CameraType>("back");
  const [permission, requestPermission] = useCameraPermissions();
  const [permissionMedia, requestMediaPermission] = useMediaPermissions();
  const [photo, setPhoto]: [ CameraCapturedPicture | undefined, any] = useState();
  const [imageTestUri, setImageTestUri] = useState<any>(null);
  const { extractReceipts, extraReceiptFromCamera } = useExtractReceipts();

  let cameraRef = useRef<CameraView | null>(null);

  if (!permission) {
    // Camera permissions are still loading.
    return <View />;
  }

  if (!permission.granted) {
    // Camera permissions are not granted yet.
    return (
      <View style={styles.container}>
        <Text style={styles.message}>
          We need your permission to show the camera
        </Text>
        <Button onPress={requestPermission} title="grant camera permission" />
      </View>
    );
  }

  // if (!permissionMedia) {
  //   // Camera permissions are still loading.
  //   return <View />;
  // }

  // if (!permissionMedia.granted) {
  //   // Camera permissions are not granted yet.
  //   return (
  //     <View style={styles.container}>
  //       <Text style={styles.message}>
  //         We need your permission to access media in the phone
  //       </Text>
  //       <Button
  //         onPress={requestMediaPermission}
  //         title="grant media permission"
  //       />
  //     </View>
  //   );
  // }

  const PreviewNewPhoto = async (photo: any) => {
    // Step 1: Fetch the file (could be an image, PDF, etc.)
    const response = await fetch(photo.uri);
    // Step 2: Convert the response to a Blob
    const blob = await response.blob();
    console.log(blob, "52^::::blob:::");
    // Convert blob to Base64
    const reader = new FileReader();
    reader.onloadend = async () => {
      setImageTestUri(reader.result); // Base64-encoded string
      // console.log("53^::BLOB_SIZE:::", blob.size)
      // console.log("54^^MAXBODLENGTH_AXIOS:::",axios.defaults.maxBodyLength,)
      // return null;
      // console.log("send blob to--->API PYTHON::XXXXr");
      // const formData = new FormData();
      // formData.append("files", blob, "files.jpg");

      // {headers: {
      //   "Content-Type": "multipart/form-data;",
      // },}

      // .post(basedUrlApiLocalhost + "/extract_receipts/xxxxxx", formData)
      // .post(basedUrlLocalhost + "/xx", formData)
      // .post("http://10.0.2.2:5001/xx", formData)
      // .post("https://50a4-175-143-188-207.ngrok-free.app/xx", formData)

      // await axios
      //   .post(basedUrlLocalhost + "/xx", formData)
      //   .then((response) => {
      //     console.log("GETTT:::::RESPONDED::PICTURE", response.data);
      //   })
      //   .catch((error) => {
      //     console.log("errrorr:::RESPOND::PICTURE");
      //     console.error(error);
      //   });

      // const uploadResponse = await fetch(
      //   basedUrlApiLocalhost + "/extract_receipts",
      //   {
      //     method: "POST",
      //     body: formData,
      //   }
      // );
      // const result = await uploadResponse.json();
      // console.log("File successfully uploaded:", result);
    };
    reader.readAsDataURL(blob); // This will convert the blob to Base64
  };

  function toggleCameraFacing() {
    setFacing((current) => (current === "back" ? "front" : "back"));
  }

  let takePic = async () => {
    let options = {
      quality: 1,
      base64: true,
      exif: false,
    };

    if (cameraRef.current == null) {
      console.log("cameraRef NULL..Retry!");
      return;
    }
    let newPhoto:
      | CameraCapturedPicture
      | undefined
      // | Promise<CameraCapturedPicture> 
      =
      await cameraRef.current.takePictureAsync(options);
    // console.log(cameraRef.current)
    // console.log(newPhoto);
    // NewPhoto form website are different type! NewPhoto From Phone are totallly different - DON'T TREAT THE SAME!!!!
    setPhoto(newPhoto);
    PreviewNewPhoto(newPhoto)
  };

  let savePhoto = async () => {
    extraReceiptFromCamera(photo)



    //  NOT SUPPORT BY WEB!
    // saveToLibraryAsync(photo.uri).then(() => {
    //   setPhoto(undefined);
    // });
  };

  const discardPhoto = async () => {
    setPhoto(undefined);
    setImageTestUri(undefined);
  };

  return (
    <View style={styles.container}>
      <CameraView
        style={styles.camera}
        facing={facing}
        ref={cameraRef}
      ></CameraView>
      {imageTestUri && (
        <Image
          source={{ uri: imageTestUri }} // Base64 string works here
          style={{ width: 200, height: 200 }}
        />
      )}
      {/* <View style={styles.buttonContainer}>
          <TouchableOpacity style={styles.button} onPress={toggleCameraFacing}>
            <Text style={styles.text}>Flip Camera</Text>
          </TouchableOpacity>
        </View> */}
      <Button onPress={toggleCameraFacing} title="Flip Camera"></Button>
      <Button title="Take Photo (Set Photo)" onPress={takePic} />
      {photo && <Button title="Saved Photo!" onPress={savePhoto} />}
      <Button title="Discard Photo" onPress={discardPhoto} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    gap: 4,
  },
  message: {
    textAlign: "center",
    paddingBottom: 10,
  },
  camera: {
    flex: 1,
  },
  buttonContainer: {
    flex: 1,
    flexDirection: "row",
    backgroundColor: "transparent",
    margin: 64,
  },
  button: {
    flex: 1,
    alignSelf: "flex-end",
    alignItems: "center",
  },
  text: {
    fontSize: 24,
    fontWeight: "bold",
    color: "white",
  },
});
