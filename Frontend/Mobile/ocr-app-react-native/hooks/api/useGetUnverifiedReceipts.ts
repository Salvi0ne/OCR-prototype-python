import { useState, useEffect } from "react";
import { useGetReceipts } from "./useGetReceipts";
import { useGetReceiptsType } from "./useGetReceipts";
import { useNavigation } from "@react-navigation/native";

export const useGetUnverifiedReceipts: useGetReceiptsType = () => {
  const { receipts, fetchReceipts, ...rest } = useGetReceipts();
  const navigation = useNavigation();

  useEffect(() => {
    async function fetchUnverifiedReceipts() {
      await fetchReceipts("unverified");
    }
    const unsubscribe = navigation.addListener("focus", () => {
      fetchUnverifiedReceipts();
    });
    return unsubscribe;
  }, [navigation]);

  return { receipts,fetchReceipts, ...rest };
};
