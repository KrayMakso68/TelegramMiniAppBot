import {login} from './authService';
import {getCurrentUser, getCurrentUserBalance, getUserAvatarUrl} from './userService';
import {getUserConnects, importConfig} from "src/api/subscribeService";
import {getConnectInfoByEmail} from "src/api/panelService";
import {getPaymentHistoryByDay, newYoomoneyPayment} from "src/api/paymentService";

export const AuthService = {
  login,
};

export const UserService = {
  getCurrentUser,
  getCurrentUserAvatar: getUserAvatarUrl,
  getCurrentUserBalance
};

export const SubscriberService = {
  getUserConnects,
  importConfig
}

export const PanelService = {
  getConnectInfoByEmail
}

export const PaymentService = {
  getPaymentHistoryByDay,
  newYoomoneyPayment
}
