import { api } from "boot/axios";
import {Payment} from "src/api/types/paymentTypes";
import {HttpStatusCode} from "axios";

export const getPaymentHistoryByDay = async (): Promise<Record<string, Payment[]> | [] | null> => {
  try {
    const response = await api.get('/payment/history');
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("User payments not found:", error);
      return [];
    } else {
      console.error("Error getting payments history from server:", error);
      return null;
    }
  }
};

export const newYoomoneyPayment = async (amount: number): Promise<string | null> => {
  try {
    const response = await api.post('/payment/new/yoomoney', {'amount': amount});
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("User payments not found:", error);
      return null;
    } else {
      console.error("Error getting payments history from server:", error);
      return null;
    }
  }
};


