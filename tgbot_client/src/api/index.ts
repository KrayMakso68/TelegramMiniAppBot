import {login} from './authService';
import {getCurrentUser, getCurrentUserBalance, getUserAvatarUrl} from './userService';
import {getUserConnects} from "src/api/subscribeService";
import {getConnectInfoByEmail} from "src/api/panelService";

export const AuthService = {
  login,
};

export const UserService = {
  getCurrentUser,
  getCurrentUserAvatar: getUserAvatarUrl,
  getCurrentUserBalance
};

export const SubscriberService = {
  getUserConnects
}

export const PanelService = {
  getConnectInfoByEmail
}
