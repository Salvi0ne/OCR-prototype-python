
export default interface ReceiptItem {
    id: string;
    total_amount: number | string;
    category: string;
    status: string;
    date: string;
    date_created: string;
    date_updated: string | null;
}