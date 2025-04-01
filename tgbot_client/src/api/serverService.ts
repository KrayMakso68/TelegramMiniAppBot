import {api} from "boot/axios";
import {Server} from "src/api/types/serverTypes";
import {HttpStatusCode} from "axios";

export const getServersInfo = async (): Promise<Server[]> => {
  try {
    const response = await api.get('/server/all/available-info');
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("Servers not found:", error);
      return [];
    } else {
      console.error("Error getting servers info from server:", error);
      return [];
    }
  }
}
