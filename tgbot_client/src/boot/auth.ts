import { boot } from 'quasar/wrappers'
import { LoginResponse } from "src/api/types/authTypes";
import { login } from "src/api/authService";
import {LocalStorage} from "quasar";

// "async" is optional;
// more info on params: https://v2.quasar.dev/quasar-cli/boot-files
export default boot(async ({ app }) => {
  try {
    const response: LoginResponse | null = await login();
    if (response) {
      LocalStorage.set('token', response.accessToken);
    }
  } catch (error) {
    console.error("Ошибка при входе:", error);
  }
})
