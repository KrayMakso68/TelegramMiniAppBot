import { api } from "boot/axios";
import {Payment, PaymentOption} from "src/api/types/paymentTypes";
import {HttpStatusCode} from "axios";

export const getPaymentHistoryByDay = async (): Promise<Record<string, Payment[]> | null> => {
  try {
    const response = await api.get('/payment/history');
    return response.data;
  } catch (error: any) {
    console.error("Error getting payments history from server:", error);
    return null;
  }
};

export const newPayment = async (path: string, amount: number): Promise<string | null> => {
  try {
    const response = await api.post(`/payment${path}`, {'amount': amount});
    return response.data;
  } catch (error: any) {
    console.error("Error getting new payment url from server:", error);
    return null;
  }
};


export const getPaymentOptions = async (): Promise<PaymentOption[]> => {
  try {
    const response = await api.get('/payment/options');
    return response.data;
  } catch (error: any) {
    console.error("Error getting payment options from server:", error);
    return [];
  }

}

