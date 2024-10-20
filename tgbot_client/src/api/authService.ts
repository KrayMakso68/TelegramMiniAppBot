import { api } from 'boot/axios';
import { useWebApp } from "vue-tg";
import { LoginResponse, InitAuthData } from "./types/authTypes";

export const login = async (data: InitAuthData): Promise<LoginResponse | null> => {
  // const { initData } = useWebApp();
  // const data: InitAuthData = { queryString: initData };

  try {
    const response = await api.post('/auth/login', data);
    return response.data;
  } catch (error) {
    console.error("Login failed:", error)
    return null
  }
}
