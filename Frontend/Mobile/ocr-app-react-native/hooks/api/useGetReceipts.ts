import { useState, useEffect } from "react";
import axios from "axios";
import { basedUrlApiLocalhost, emulatorApiLocahost } from "@/constants/Api";
import ReceiptItem from "@/constants/Interface/receiptItem";

export interface useGetReceiptsType {
    (): {
      fetchReceipts: (status: string) => Promise<void>;
      receipts: ReceiptItem[];
      setReceipts: React.Dispatch<React.SetStateAction<ReceiptItem[]>>;
      error: null;
      setError: React.Dispatch<React.SetStateAction<any>>;
      loading: boolean;
      setLoading: React.Dispatch<React.SetStateAction<boolean>>;
    };
}

export const useGetReceipts: useGetReceiptsType = () => {
  const [receipts, setReceipts] = useState([] as ReceiptItem[]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchReceipts = async (status: string) => {
    try {
      console.log(basedUrlApiLocalhost,'?..?')
      const response = await axios.get(
        basedUrlApiLocalhost + "/receipts/" + status
        // emulatorApiLocahost + "/receipts/" + status
      );
      console.log(response.data.data)
      console.log(response.data.data)
      setReceipts(response.data.data);
    } catch (error: any) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return {
    fetchReceipts,
    receipts,
    setReceipts,
    error,
    setError,
    loading,
    setLoading,
  } ;
};
