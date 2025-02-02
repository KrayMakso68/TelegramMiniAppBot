import { api } from "boot/axios";
import {Payment, PaymentOptions} from "src/api/types/paymentTypes";
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


export const getPaymentOptions = async (): Promise<PaymentOptions[]> => {
  try {
    const response = await api.get('/payment/options');
    return response.data;
  } catch (error: any) {
    console.error("Error getting payment options from server:", error);
    return [];
  }

}

