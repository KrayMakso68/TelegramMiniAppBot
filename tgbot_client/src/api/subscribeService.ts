import {api} from "boot/axios";
import {Connect} from "src/api/types/subscribeTypes";
import {HttpStatusCode} from "axios";

export const getUserConnects = async (): Promise<Connect[] | null> => {
  try {
      const response = await api.get('/subscribe/connects');
      return response.data;
    } catch (error: any) {
        if (error.response.status === HttpStatusCode.NotFound) {
          console.error("User connects not found:", error);
          return [];
        } else {
          console.error("Error getting connects from server:", error);
          return null;
        }
    }
}
