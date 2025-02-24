import {api} from "boot/axios";
import {Subscription} from "src/api/types/subscriptionTypes";
import {HttpStatusCode} from "axios";

export const getUserSubscriptionsByServer = async (): Promise<Record<string, Subscription[]> | null> => {
  try {
    const response = await api.get('/subscription/servers');
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("User connects not found:", error);
      return {};
    } else {
      console.error("Error getting connects from server:", error);
      return null;
    }
  }
}

// export const importConfig = async (config: string) => {
//   await api.get(`/subscribe/import-config?config=${config}`);
// }
