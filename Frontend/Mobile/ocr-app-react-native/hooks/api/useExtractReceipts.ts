import { basedUrlApiLocalhost } from "@/constants/Api";
import { useState } from "react";
import axios from "axios";
import { ImagePickerAsset } from "expo-image-picker";
import { useNavigatorRoute } from "@/hooks/useNavigatorRoute";
import { CameraCapturedPicture } from "expo-camera";
import * as FileSystem from "expo-file-system";

export const useExtractReceipts = () => {
  const [responseMessage, setResponseMessage] = useState<string | null>(null);

  // const [formAppend, setFormAppend] = useState<any>(null);

  const { handleButtonPress } = useNavigatorRoute();


  const convertImageToBlob = async ( photo: ImagePickerAsset| CameraCapturedPicture | any ) => {
    const response = await fetch(photo.uri);
    const blob = await response.blob();
    // console.log(blob, "52^::::blob:::");
    return blob;
    // // Convert blob to Base64
    // const reader = new FileReader();
    // reader.onloadend = async () => {
    //   // await axios
    //   //   .post(basedUrlLocalhost + "/xx", formData)
    //   //   .then((response) => {
    //   //     console.log("GETTT:::::RESPONDED::PICTURE", response.data);
    //   //   })
    //   //   .catch((error) => {
    //   //     console.log("errrorr:::RESPOND::PICTURE");
    //   //     console.error(error);
    //   //   });
    // };
    // reader.readAsDataURL(blob);

  };

  // ! MAY NOT USED ANYMORE!!!
  async function dataUriToBlob(image: ImagePickerAsset) {

    //! WEB NOT SUPPORTED!!
    // const mimeType = 'image/jpg';
    // const base64 = await FileSystem.readAsStringAsync(image.uri, { encoding: 'base64' });
    // console.log(base64,'::1-11-1::');
    // const blob = await fetch(`data:${mimeType};base64,${base64}`).then(response => response.blob());
    // console.log('::1-22::',blob);
    // const uint8Array = await new Uint8Array(atob(base64).split('').map(char => char.charCodeAt(0)));
    // console.log(uint8Array,'::1-11-2::');
    // const blob = await new Blob([uint8Array], { type: mimeType });
    // console.log(blob,'::1-11-3::');
    // return blob;

    //! ONLY SUPPORT WEB !!
    const mimeTypeMatch = image.uri.match(/^data:(.*?);base64,/);
    let dataUri = mimeTypeMatch ? image.uri : "data:image/jpg;base64," + image.base64;
    const [metadata, base64] = dataUri.split(",");


    // @ts-ignore
    const mimeType = metadata.match(/:(.*?);/)[1];


    console.log(mimeType, metadata,'::::::MMMMMMM:::');

    const byteCharacters = atob(base64);
    const byteArrays = [];
    for (let offset = 0; offset < byteCharacters.length; offset += 512) {
      const slice = byteCharacters.slice(offset, offset + 512);
      const byteNumbers = new Array(slice.length);
      for (let i = 0; i < slice.length; i++) {
        byteNumbers[i] = slice.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
    }

    return new Blob(byteArrays, { type: mimeType });
  }

  const extractMimeTypeAndExtensionFromDataURL = (uri: string) => {
    const mimeTypeMatch = uri.match(/^data:(.*?);base64,/);
    const mimeType = mimeTypeMatch ? mimeTypeMatch[1] : "unknown";

    const mimeTypeToExtension: { [key: string]: string | undefined } = {
      "image/jpeg": "jpg",
      "image/png": "png",
      "image/gif": "gif",
      // Add more MIME types and extensions as needed
    };

    const fileExtension = mimeTypeToExtension[mimeType] || "unknown";

    return { mimeType, fileExtension };
  };

  const extraReceiptFromCamera = async (photo: CameraCapturedPicture | undefined) => {
    if(!photo) {
      console.log("ERROR::::99::useExtractReceipts")
      return false;
    }
    // const { mimeType, fileExtension } = extractMimeTypeAndExtensionFromDataURL(photo.uri);
    // const resolvedPhoto = await photo;
    console.log(photo,'::extraReceiptFromCamera::PHoTO');
    const randomNumber = Math.floor(100 + Math.random() * 900);
    //! Only work with  Web Support!
    extractReceipts([
      {
        uri: photo.uri,
        assetId: String(randomNumber),
        width: photo.width,
        height: photo.height,
        type: "image",
        // fileName:
        //   "phone_camera_took_picture_" + randomNumber + "." + fileExtension ??
        //   "png",
        fileName:
          "phone_camera_took_picture_" + randomNumber + "." + "jpg",
        fileSize: undefined,
        exif: photo.exif,
        base64: photo.base64,
        duration: null,
        mimeType: "image/jpeg",
      },
    ]);
  };

  const extractReceipts = async (receipts: ImagePickerAsset[] | null) => {
    if (!receipts) return;
    let blob_receipt_array = []
    console.log('begin::::');
    for (const r of receipts) {
      // console.log(r,'::receipt::');
      // const blob = await dataUriToBlob(r);
      const blob = await convertImageToBlob(r)
      // console.log('BBBLLOOONNNNBBB')
      // console.log(blob);
      blob_receipt_array.push({blob:blob, receipt: r});
    }

    const formData = new FormData();
    for (const obj of blob_receipt_array) {
      const randomNumber = Math.floor(100 + Math.random() * 900);
      formData.append(
        "files",
        obj.blob,
        obj.receipt.fileName ?? "no_name_" + randomNumber + ".jpg"
      );
    }
    console.log("::CHECK::FORM_DATA::");
    for (const [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }

    // const config = {
    //   headers: {
    //     "Content-Type": "multipart/form-data;",
    //   },
    // };

    try {
      const response = await axios.post(
        basedUrlApiLocalhost + "/extract_receipts",
        formData,
      );

      // console.log("Response:", response.data);
      // setResponseMessage(response.data.message);

      if (response.data.code == 200) {
        handleButtonPress("receipts");
      }
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        setResponseMessage("Error: " + error.response.data.error);
      } else {
        setResponseMessage("Error connecting to API");
      }
      console.error(error);
    }
  };

  const readImageFromWebReturnBase64 = async () => {

  }

  const readImageFromPhoneReturnBase64 = async (image : ImagePickerAsset) => {
    const uri = image.uri;
    // const fileInfo = await FileSystem.getInfoAsync(uri);
    const base64 = await FileSystem.readAsStringAsync(uri, { encoding: 'base64' });
    const photo = {
      base64,
      mimeType: "image/jpg,",
    };
  
    // const dataUrlBase64 = `data:${photo.mimeType};base64,${photo.base64}`;

    // console.log(dataUrlBase64);
    return base64;
    // return dataUrlBase64;
  }

  return {
    responseMessage,
    extractReceipts,
    extraReceiptFromCamera,
  };
};
