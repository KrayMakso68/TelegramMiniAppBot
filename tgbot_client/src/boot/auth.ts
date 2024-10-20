import { boot } from 'quasar/wrappers'
import {InitAuthData, LoginResponse} from "src/api/types/authTypes";
import { AuthService } from "src/api";
import {LocalStorage} from "quasar";
import {useWebApp} from "vue-tg";


export default boot(async ({ app, router }) => {
  const { initData } = useWebApp();

  if (!initData) {
    await router.push('/not-from-telegram'); // перенаправление, если не из Telegram
    return;
  }

  try {
    const data: InitAuthData = { queryString: initData };
    const response: LoginResponse | null = await AuthService.login(data);
    if (response) {
      LocalStorage.set('token', response.accessToken);
    }
  } catch (error) {
    console.error("Ошибка при входе:", error);
  }
})
