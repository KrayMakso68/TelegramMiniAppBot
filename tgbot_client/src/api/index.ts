import {login} from './authService';
import {getCurrentUser, getCurrentUserBalance, getUserAvatarUrl} from './userService';
import {getUserSubscriptionsByServer} from "src/api/subscriptionService";
import {getConnectInfoByEmail, updateUserSubscriptions} from "src/api/panelService";
import {getPaymentHistoryByDay, newPayment, getPaymentOptions} from "src/api/paymentService";
import {getServersInfo} from "src/api/serverService"

export const AuthService = {
  login,
};

export const UserService = {
  getCurrentUser,
  getCurrentUserAvatar: getUserAvatarUrl,
  getCurrentUserBalance
};

export const SubscriptionService = {
  getUserSubscriptions: getUserSubscriptionsByServer
}

export const PanelService = {
  getConnectInfoByEmail,
  updateUserSubscriptions
}

export const PaymentService = {
  getPaymentHistoryByDay,
  newPayment,
  getPaymentOptions
}

export const ServerService = {
  getServersInfo
}
