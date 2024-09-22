import { useState, useEffect } from "react";
import { useGetReceipts } from "./useGetReceipts";
import { useNavigation } from "@react-navigation/native";
import { useGetReceiptsType } from "./useGetReceipts";

export const useGetVerifiedReceipts: useGetReceiptsType = () => {
  const { receipts, fetchReceipts, ...rest } = useGetReceipts();
  const navigation = useNavigation();

  useEffect(() => {
    async function fetchUnverifiedReceipts() {
      await fetchReceipts("verified");
    }
    const unsubscribe = navigation.addListener("focus", () => {
      fetchUnverifiedReceipts();
    });
    return unsubscribe;
  }, [navigation]);

  return { receipts, fetchReceipts, ...rest };
};
