import { api } from "boot/axios";
import { User } from "src/api/types/userTypes";
import {LocalStorage} from "quasar";

export const getCurrentUser = async (): Promise<User> => {
  const response = await api.get('/user');
  return response.data;
}

export const getUserAvatarUrl = async (): Promise<string | null> => {
  const cachedAvatar = LocalStorage.getItem<string>('userAvatar');

  if (!cachedAvatar) {
    const response = await api.get(`/user/avatar`, {responseType: 'blob'});
    const imageUrl = URL.createObjectURL(response.data);
    LocalStorage.set('userAvatar', imageUrl);
    return imageUrl;
  }
  return cachedAvatar
};
