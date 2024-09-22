import ReceiptsComponent from "@/components/ReceiptsComponent";
import { basedUrlApiLocalhost } from "@/constants/Api";
import { useGetUnverifiedReceipts } from "@/hooks/api/useGetUnverifiedReceipts";
import axios from "axios";
import React, { Fragment } from "react";
import { Alert, Button, Text, View } from "react-native";

export default function Receipts() {
  const { receipts, setReceipts } = useGetUnverifiedReceipts();

  const submit_receipts_to_verify = (receipts: any[]) => {
    const formData = new FormData();

    receipts.forEach((r) => {
      formData.append('ids[]', r.id);
    });
    // console.log("id::::", formData.getAll("ids"));
    axios
      .post(`${basedUrlApiLocalhost}/submit_receipts_to_verify`, formData,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((response) => {
        console.log(response.data);
        Alert.alert('Receipts Submitted Successfully! -  check Home ...')
        setReceipts([]);
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <Fragment>
      <Text style={{ fontSize: 24, paddingTop: 16, paddingLeft: 16 }}>
        Receipts Check{" "}
      </Text>
      <ReceiptsComponent receipts={receipts} setReceipts={setReceipts} />
      <View style={{ padding: 16, margin: 16 }}>
        <Button
          title="Submit Receipts"
          onPress={() => submit_receipts_to_verify(receipts)}
          color="#841584"
        />
      </View>
    </Fragment>
  );
}
