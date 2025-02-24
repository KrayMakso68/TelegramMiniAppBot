import {login} from './authService';
import {getCurrentUser, getCurrentUserBalance, getUserAvatarUrl} from './userService';
import {getUserSubscriptionsByServer} from "src/api/subscriptionService";
import {getConnectInfoByEmail} from "src/api/panelService";
import {getPaymentHistoryByDay, newPayment, getPaymentOptions} from "src/api/paymentService";

export const AuthService = {
  login,
};

export const UserService = {
  getCurrentUser,
  getCurrentUserAvatar: getUserAvatarUrl,
  getCurrentUserBalance
};

export const SubscriberService = {
  getUserSubscriptions: getUserSubscriptionsByServer
}

export const PanelService = {
  getConnectInfoByEmail
}

export const PaymentService = {
  getPaymentHistoryByDay,
  newPayment,
  getPaymentOptions
}
