import { api } from "boot/axios";
import { User } from "src/api/types/userTypes";
import {LocalStorage} from "quasar";

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get('/user');
  return response.data;
}

export const getUserAvatarUrl = async (): Promise<string | null> => {
  const cachedAvatarBase64: string | null = LocalStorage.getItem<string>('userAvatar');

  if (!cachedAvatarBase64) {
    try {
      const response = await api.get(`/user/avatar`);
      const avatarBase64: string = response.data;
      LocalStorage.set('userAvatar', avatarBase64);
      return avatarBase64;
    } catch (error) {
      console.error("Error getting avatar from server:", error);
      return null;
    }
  }
  return cachedAvatarBase64;
};

export const getCurrentUserBalance = async (): Promise<number> => {
  const response = await api.get('/user/balance');
  return response.data;
}
