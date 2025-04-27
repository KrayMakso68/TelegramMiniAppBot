import {api} from "boot/axios";
import {Server} from "src/api/types/serverTypes";
import {HttpStatusCode} from "axios";

export const getAllServersInfo = async (): Promise<Server[]> => {
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

export const getServerInfoById = async (serverId: number): Promise<Server | null> => {
  try {
    const response = await api.get(`/server/${serverId}/available-info`);
    return response.data;
  } catch (error: any) {
    if (error.response.status === HttpStatusCode.NotFound) {
      console.error("Server not found:", error);
      return null;
    } else {
      console.error("Error getting servers info from server:", error);
      return null;
    }
  }
}
