import {api} from "boot/axios";
import {User} from "src/api/types/userTypes";

export const getUser = async (): Promise<User> => {
  const response = await api.get('/auth/user');
  return response.data;

}
