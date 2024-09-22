import { basedUrlApiLocalhost } from "@/constants/Api";
import ReceiptItem from "@/constants/Interface/ReceiptItem";
import { useGetReceiptsType } from "@/hooks/api/useGetReceipts";
import { useGetUnverifiedReceipts } from "@/hooks/api/useGetUnverifiedReceipts";
import axios from "axios";
import React, { useState } from "react";
import {
  Button,
  Image,
  View,
  Text,
  FlatList,
  StyleSheet,
  TextInput,
  Modal,
  TouchableOpacity,
  Alert,
} from "react-native";

export default function ReceiptsComponent({
  // hookGetReceipts,
  receipts,
  setReceipts
  
}: {
  // hookGetReceipts: useGetReceiptsType;
  receipts: ReceiptItem[];
  setReceipts: React.Dispatch<React.SetStateAction<any>>;
}) {
  // const { receipts, setReceipts } = hookGetReceipts();
  //   const { receipts, setReceipts }: { receipts: ReceiptItem[]; setReceipts: React.Dispatch<React.SetStateAction<any>> } = useGetUnverifiedReceipts();

  const [isModalVisible, setIsModalVisible] = useState(false);

  const [editedItem, setEditedItem] = useState<ReceiptItem>({
    id: "",
    total_amount: "",
    category: "",
    status: "",
    date: "",
    date_created: "",
    date_updated: null,
  });

  const handleEditPress = (item: ReceiptItem) => {
    setEditedItem(item);
    setIsModalVisible(true);
  };

  const handleModalClose = () => {
    setIsModalVisible(false);
  };

  const handleInputChange = (field: string, value: string) => {
    setEditedItem({ ...editedItem, [field]: value });
  };

  const handleSaveChanges = async () => {
    try {
      const index = receipts.findIndex((item) => item.id === editedItem.id);
      if (index !== -1) {

        // Patch
        await axios.patch(`${basedUrlApiLocalhost}/receipt/${editedItem.id}`, editedItem)
        .then((response) => {
          if (response.status === 200) {
            console.log(response.data,"OK!");
            const updatedReceipts = [...receipts];
            updatedReceipts[index] = editedItem;
            setReceipts(updatedReceipts);
            handleModalClose();
          }
        })
        .catch((error) => {
          console.log("::ERORR::RECEIPTS_COMPONENT")
          handleModalClose();
          console.error(error);
        });
        // const response = await fetch('/api/extract_receipts', {
        //   method: 'POST',
        //   headers: {
        //     'Content-Type': 'application/json',
        //   },
        //   body: JSON.stringify(editedItem),
        // });
        // if (response.ok) {
        //   setReceipts(updatedReceipts);
        // } else {
        //   throw new Error('Failed to update receipt');
        // }
      }
    } catch (error) {
      console.error(error);
      // Handle the error here
    }
  };

  const handleDeleteReceipt = async (id: string) => {
    try {
      const response = await axios.delete(`${basedUrlApiLocalhost}/receipt/${id}`);
      if (response.status === 200) {
        const updatedReceipts = receipts.filter((item) => item.id !== id);
        setReceipts(updatedReceipts);
        Alert.alert("Success", "Receipt deleted successfully!");
      } else {
        throw new Error('Failed to delete receipt');
      }
    } catch (error) {
      console.error(error);
    }
  };

  const renderItem = ({
    item,
    index,
  }: {
    item: ReceiptItem;
    index: number;
  }) => (
    <View style={styles.viewRender}>
      <Text style={styles.textRender}>Receipt {index + 1}</Text>
      <Text style={styles.textRender}>id: {item.id}</Text>
      <Text style={styles.textRender}>category: {item.category}</Text>
      <Text style={styles.textRender}>total_amount: {item.total_amount}</Text>
      <Text style={styles.textRender}>status: {item.status}</Text>
      <Text style={styles.textRender}> date: {item.date}</Text>
      <Text style={styles.textRender}>date_created: {item.date_created}</Text>
      <View style={styles.buttonContainer}>
        <Button title="Edit" onPress={() => handleEditPress(item)}></Button>
        <Button
          color={"red"}
          title="Delete"
          onPress={() => handleDeleteReceipt(item.id)}
        ></Button>
      </View>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={receipts}
        renderItem={renderItem}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.flatList}
      />

      <Modal
        visible={isModalVisible}
        onBackdropPress={handleModalClose}
        transparent
      >
        {editedItem && (
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <TouchableOpacity onPress={handleModalClose}>
                <Text style={styles.closeButton}>Close</Text>
              </TouchableOpacity>
            </View>
            <Text style={{ fontSize: 24, padding: 10, alignSelf: "center" }}>
              Edit Receipt
            </Text>
  
            <TextInput
              style={styles.textInput}
              value={editedItem.date}
              onChangeText={(text) => handleInputChange("date", text)}
              placeholder="Date"
              placeholderTextColor="#AAAAAA"
            />
            <TextInput
              style={styles.textInput}
              value={editedItem.category}
              onChangeText={(text) => handleInputChange("category", text)}
              placeholder="Category"
              placeholderTextColor="#AAAAAA"
            />
            <TextInput
              style={styles.textInput}
              value={editedItem.total_amount.toString()}
              onChangeText={(text) => handleInputChange("total_amount", text)}
              placeholder="Total Amount"
              placeholderTextColor="#AAAAAA"
              keyboardType="numeric"
            />
            <Button title="Save Changes" onPress={handleSaveChanges}></Button>
          </View>
        )}
      </Modal>

    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    // flex: 1,
    // justifyContent: "center",
    // alignItems: "center",
  },
  flatList: {
    flexGrow: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  viewRender: {
    borderWidth: 1,
    borderColor: "gray",
    padding: 10,
  },
  textRender: {
    borderBottomWidth: 1,
    borderColor: "gray",
    paddingBottom: 5,
  },
  buttonContainer: {
    flexDirection: "row",
    justifyContent: "center",
    gap: 10,
    marginVertical: 10,
  },
  modalContent: {
    // position: "absolute",
    // top: "50%",
    // left: "50%",
    // transform: "translate(-50%, -50%)",
    padding: "4%",
    margin: 0,
    borderRadius: 10,
    width: "80%",
    backgroundColor: "white",
  },
  modalHeader: {
    flexDirection: "row",
    justifyContent: "flex-end",
    gap: 10,
    alignItems: "center",
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: "#ccc",
  },
  textInput: {
    height: 40,
    borderColor: "#ccc",
    borderWidth: 1,
    paddingHorizontal: 10,
    paddingVertical: 5,
    fontSize: 16,
    borderRadius: 5,
    marginBottom: 10,
  },
  closeButton: {
    fontSize: 16,
    color: "#007aff",
  },
});
