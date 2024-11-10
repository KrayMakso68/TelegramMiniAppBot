// Импорт отдельных сервисов
import {login} from './authService';
import {getCurrentUser, getUserAvatarUrl} from './userService';
import {getUserConnects} from "src/api/subscribeService";

// Экспорт сервисов для упрощенного импорта
export const AuthService = {
  login,
};

export const UserService = {
  getCurrentUser,
  getCurrentUserAvatar: getUserAvatarUrl
};

export const SubscriberService = {
  getUserConnects
}
