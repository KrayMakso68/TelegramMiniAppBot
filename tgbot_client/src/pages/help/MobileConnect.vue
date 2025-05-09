<script setup lang="ts">
import {BackButton} from "vue-tg";
import TgSection from "components/TgSection.vue";
import {useRouter} from "vue-router";
import {ref} from "vue";

const router = useRouter();

const step = ref<number>(1)

</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>

  <q-page class="tg-text overflow-auto">
    <tg-section label="Подключение на Мобильном устройстве">
      <div class="">
        <q-stepper
          class="stepper-box tg-text"
          v-model="step"
          vertical
          animated
          flat
        >
          <q-step
            :name="1"
            title="Скачайте приложение клиента"
            icon="download"
            :done="step > 1"
          >
            <p>Для подключения к VPN на устройство необходимо скачать клиент VPN.</p>
            <p>Мы рекомендуем использовать приложение <strong>Hiddify</strong>.</p>
            <q-btn
              label="Offical Website"
              type="a"
              href="https://hiddify.com"
              target="_blank"
              rel="noopener noreferrer"
              icon="open_in_new"
              class="tg-btn q-mb-md"
            />

            <div class="p">Для Android:</div>
            <q-btn
              label="Google Play"
              type="a"
              href="https://play.google.com/store/apps/details?id=app.hiddify.com&pli=1"
              target="_blank"
              icon="open_in_new"
              class="tg-btn q-mb-sm"
            />

            <div class="p">Для IOS:</div>
            <q-btn
              label="App Store"
              type="a"
              href="https://apps.apple.com/us/app/hiddify-proxy-vpn/id6596777532?platform=iphone"
              target="_blank"
              icon="open_in_new"
              class="tg-btn q-mb-sm"
            />

            <div class="p">После установки выберите регион: <strong>Другой</strong></div>
            <q-img
              src="/images/help_mobile/install.png"
              spinner-color="gray"
              class="q-mt-sm q-mb-md"
            />

            <q-stepper-navigation>
              <q-btn @click="step = 2" label="Дальше" class="tg-btn"/>
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="2"
            title="Скопируйте ссылку для подключения"
            icon="content_copy"
            :done="step > 2"
          >
            <p>Приобретая подписку, вам автоматически выдаётся сслылка для подключения к VPN.</p>
            Скопируйте её:

            <q-img
              src="/images/help_mobile/link_copy.png"
              spinner-color="gray"
            />


            <q-stepper-navigation>
              <q-btn @click="step = 3" label="Дальше" class="tg-btn"/>
              <q-btn flat @click="step = 1" label="Назад" class="q-ml-sm" />
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="3"
            title="Добавьте ссылку в приложении"
            icon="add"
            :done="step > 3"
          >
            <div class="p">Зайдите в приложение и нажмите на кнопку добавления подписки</div>
            <q-img
              src="/images/help_mobile/add_button.png"
              spinner-color="gray"
              class="q-mt-sm q-mb-md"
            />

            <div class="p">Нажмите на кнопку 'Добавить из буфера обмена'</div>
            <q-img
              src="/images/help_mobile/copy.png"
              spinner-color="gray"
              class="q-mt-sm q-mb-md"
            />

            <div class="p">Подключение успешно добавлено!</div>
            <q-img
              src="/images/help_mobile/success.png"
              spinner-color="gray"
              class="q-mt-sm q-mb-md"
            />



            <q-stepper-navigation>
              <q-btn @click="step = 4" label="Дальше" class="tg-btn"/>
              <q-btn flat @click="step = 2" label="Назад" class="q-ml-sm" />
            </q-stepper-navigation>
          </q-step>

          <q-step
            :name="4"
            title="Проверка соединения"
            icon="rule"
          >
            <p>Нажмите на кнопку подключения</p>

            <div class="p">Для проверки задержки нажмите на область под главной кнопкой</div>
            <q-img
              src="/images/help_mobile/check.png"
              spinner-color="gray"
              class="q-mt-sm q-mb-md"
            />

            <p>Для отключения нажмите на кнопку подключения снова</p>

            <q-stepper-navigation>
              <q-btn @click="router.push('/')" label="На главную" class="tg-btn"/>
              <q-btn flat @click="step = 3" label="Назад" class="q-ml-sm" />
            </q-stepper-navigation>
          </q-step>
        </q-stepper>
      </div>
    </tg-section>
  </q-page>

</template>

<style scoped>
.stepper-box {
  background-color: var(--tg-section-bg-color);
}
::v-deep(.q-stepper__tab--active) {
  color: var(--tg-accent-text-color) !important;
}
::v-deep(.q-stepper__tab--done) {
  color: var(--tg-accent-text-color) !important;
}
::v-deep(.q-stepper__tab) {
  color: var(--tg-subtitle-text-color);
}
::v-deep(.q-stepper--vertical .q-stepper__dot:after) {
  background-color: var(--tg-secondary-bg-color);
  width: 2px;
}
</style>
