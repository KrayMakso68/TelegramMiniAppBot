import {api} from "boot/axios";
import {Connect} from "src/api/types/subscribeTypes";

export const getUserConnects = async (): Promise<Connect[]> => {
  try {
      const response = await api.get('/subscribe/connects');
      return response.data;
    } catch (error) {
      console.error("Error getting connects from server:", error);
      return [];
    }
}
