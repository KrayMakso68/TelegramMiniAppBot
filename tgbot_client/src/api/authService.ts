import { api } from 'boot/axios';
import { LoginResponse, InitAuthData } from "./types/authTypes";

export const login = async (data: InitAuthData): Promise<LoginResponse | null> => {
  try {
    const response = await api.post('/auth/login', data);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error)
    return null
  }
}
