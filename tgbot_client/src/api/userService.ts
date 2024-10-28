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
    const response = await api.get(`/user/avatar`);
    const avatarBase64: string = response.data;
    LocalStorage.set('userAvatar', avatarBase64);
    return avatarBase64;
  }

  return cachedAvatarBase64;


  // if (cachedAvatarBase64) {
  //   await fetch(cachedAvatarUrl)
  //     .then(() => cachedAvatarUrl)
  //     .catch((error) => {
  //       console.error("Ошибка проверки аватара:", error);
  //       URL.revokeObjectURL(cachedAvatarUrl);
  //       LocalStorage.remove('userAvatar');
  //     })
  // }
  // try {
  //   const response = await api.get(`/user/avatar`, {responseType: 'blob'});
  //   const avatarUrl: string = URL.createObjectURL(response.data);
  //   LocalStorage.set('userAvatar', avatarUrl);
  //   return avatarUrl;
  // } catch (error) {
  //   console.error("Ошибка при получении аватара с сервера:", error);
  //   return null;
  // }

};
