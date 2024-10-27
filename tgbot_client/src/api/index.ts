// Импорт отдельных сервисов
import { login } from './authService';
import { getCurrentUser, getUserAvatarUrl } from './userService';

// Экспорт сервисов для упрощенного импорта
export const AuthService = {
  login,
};

export const UserService = {
  getCurrentUser,
  getCurrentUserAvatar: getUserAvatarUrl
};
