import {api} from "boot/axios";
import {ConnectData} from "src/api/types/panelTypes";

export const getConnectByEmail = async (email: string): Promise<ConnectData | null> => {
  try {
      const response = await api.get(`client/info_by_email/${email}`);
      return response.data;
    } catch (e) {
      return null;
    }
}
