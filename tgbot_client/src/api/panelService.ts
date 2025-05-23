import {api} from "boot/axios";
import {ClientCreate, ClientDelete, ClientInfo, ClientUpdate} from "src/api/types/panelTypes";
import {HttpStatusCode} from "axios";

export const getConnectInfoByEmail = async (serverId: number, email: string): Promise<ClientInfo | null> => {
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

export const updateUserSubscriptions = async (): Promise<Record<string, string>> => {
  try {
    const response = await api.post(`/panel/subscription/update-all`);
    return response.data;
  } catch (error: any) {
    console.error("Error updating subscriptions:", error);
    return {status: "Error"};
  }
}

export const addClient = async (clientCreate: ClientCreate): Promise<Record<string, string>> => {
  try {
    let serverId = clientCreate.serverId;
    const response = await api.post(`/panel/${serverId}/client/add`, clientCreate);
    return response.data;
  } catch (error) {
    console.error("Failed to add client:", error)
    return {status: "Error"}
  }
}

export const updateClient = async (clientUpdate: ClientUpdate): Promise<Record<string, string>> => {
  try {
    let serverId = clientUpdate.serverId;
    const response = await api.post(`/panel/${serverId}/client/update`, clientUpdate);
    return response.data;
  } catch (error) {
    console.error("Failed to update client:", error)
    return {status: "Error"}
  }
}

export const deleteClient = async (clientDelete: ClientDelete): Promise<Record<string, string>> => {
  try {
    let serverId = clientDelete.serverId;
    const response = await api.post(`/panel/${serverId}/client/delete`, clientDelete);
    return response.data;
  } catch (error) {
    console.error("Failed to delete client:", error)
    return {status: "Error"}
  }
}
