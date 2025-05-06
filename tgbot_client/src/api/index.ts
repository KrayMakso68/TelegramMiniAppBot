import {login} from './authService';
import {getCurrentUser, getCurrentUserBalance, getUserAvatarUrl} from './userService';
import {getUserSubscriptionsByServer} from "src/api/subscriptionService";
import {
  getConnectInfoByEmail,
  updateUserSubscriptions,
  addClient,
  updateClient,
  deleteClient
} from "src/api/panelService";
import {getPaymentHistoryByDay, newPayment, getPaymentOptions} from "src/api/paymentService";
import {getAllServersInfo, getServerInfoById} from "src/api/serverService"

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
  updateUserSubscriptions,
  addClient,
  updateClient,
  deleteClient
}

export const PaymentService = {
  getPaymentHistoryByDay,
  newPayment,
  getPaymentOptions
}

export const ServerService = {
  getAllServersInfo,
  getServerInfoById
}
