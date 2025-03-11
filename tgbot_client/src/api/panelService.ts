import {api} from "boot/axios";
import {ConnectInfo} from "src/api/types/panelTypes";
import {HttpStatusCode} from "axios";
import {Subscription} from "src/api/types/subscriptionTypes";

export const getConnectInfoByEmail = async (serverId: number, email: string): Promise<ConnectInfo | null> => {
  try {
    const response = await api.get(`/panel/${serverId}/client/info-by-email/${email}`);
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("Connect info not found:", error);
      return null;
    } else {
      console.error("Error getting connect info from server:", error);
      return null;
    }
  }
}

export const updateUserSubscriptions = async (): Promise<Record<string, Subscription[]> | null> => {
  try {
    const response = await api.post(`/panel/subscription/update-all`);
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("Connect info not found:", error);
      return null;
    } else {
      console.error("Error getting connect info from server:", error);
      return null;
    }
  }
}
