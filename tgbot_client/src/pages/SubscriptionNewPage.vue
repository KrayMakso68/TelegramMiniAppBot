<script setup lang="ts">

import {BackButton, MainButton, useWebAppMainButton} from "vue-tg";
import TgSection from "components/TgSection.vue";
import {useRouter} from "vue-router";
import {computed, onMounted, Ref, ref, watchEffect} from "vue";
import {Server} from "src/api/types/serverTypes";
import {ServerService, UserService, PanelService} from "src/api";
import {ClientCreate} from "src/api/types/panelTypes";
import CountryFlag from 'vue-country-flag-next'
import AnimatedBanner from "components/AnimatedBanner.vue";


const router = useRouter();
const {disableMainButton, enableMainButton} = useWebAppMainButton();

const isLoadingServers = ref(true);
const inputValue = ref<string | null>(null);
const serverValue = ref<Server | null>(null);
const serverOptions = ref<Server[]>([{id: 0, label:"Не найдено", countryCode: "...", monthPrice: 0, isActive: false}]);
const monthValue = ref<number>(1)
const userBalance = ref<number>(0)


const loadBalance = async () => {
  userBalance.value = await UserService.getCurrentUserBalance();
};

const loadServerOptions = async () => {
  serverOptions.value = await ServerService.getAllServersInfo()
  if (serverOptions.value.length === 0) {
    serverOptions.value = [{id: 1, label:"Не найдено", countryCode: "...", monthPrice: 0, isActive: false}]
  }
  isLoadingServers.value = false;
};

const amount = computed(() => serverValue.value ? serverValue.value.monthPrice * monthValue.value : 0);

const inputRules = computed(() => [
  (val: string | null) => {
    if (val === null || val.trim() === '') return 'Обязательное поле';
    return val.length <= 10 || 'Максимум 10 символов'
  },
  (val: string | null) => {
    if (!val) return true;
    return /^[A-Za-z0-9_]+$/.test(val) || 'Только a-z, 0-9, _';
  },
  (val: string | null) => {
    if (!val) return true;
    return val === val.toLowerCase() || 'Только нижний регистр';
  }
]);

const hasInputError = computed(() => {
  return inputRules.value.some(rule =>
    typeof rule(inputValue.value) === 'string'
  );
});

const hasAmountError = computed(() => {
  return amount.value > userBalance.value;
})

const inputErrorMessage = computed(() => {
  const messages = inputRules.value
    .map(rule => rule(inputValue.value))
    .filter(msg => typeof msg === 'string');
  return messages.join(' ; ');
});

watchEffect(() => {
  if (inputValue.value !== null &&
      serverValue.value !== null &&
      !hasInputError.value &&
      monthValue.value &&
      amount.value <= userBalance.value
  ) {
    enableMainButton();
  } else {
    disableMainButton();
  }
});

const loadingDialog = ref<boolean>(false);
const loadingStatus = ref<boolean>(true);
const loadingError = ref<boolean>(false);

const addClient = async (): Promise<Record<string, string>> => {
  if (serverValue.value && inputValue.value) {
    let data: ClientCreate = {
      shortName: inputValue.value,
      protocol: 'vless',
      serverId:  serverValue.value.id,
      months: monthValue.value,
      price: amount.value
    }
    return await PanelService.addClient(data);
  } else {
    return {'status': 'Error'};
  }
}

const addClientHandler = async () => {
  loadingDialog.value = true;
  let status = await addClient();
  if (status.status === 'OK') {
    loadingStatus.value = false;
  } else {
    loadingStatus.value = false;
    loadingError.value = true;
  }
  setTimeout(() => router.push('/'), 2000)
};

onMounted(() => {
  disableMainButton();
  loadServerOptions();
  loadBalance();
})
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>

  <q-page class="tg-text overflow-auto">
    <tg-section label="Новая подписка">
      <div class="q-mt-sm q-pa-sm">
        <q-input
          lang="en"
          class="q-py-md"
          type="text"
          clearable
          autofocus
          dense
          borderless
          v-model="inputValue"
          label="Имя подключения"
          stack-label
          :rules="inputRules"
          :error="hasInputError"
          :error-message="inputErrorMessage"
        />
        <q-select
          class="select q-py-md"
          type="text"
          clearable
          dense
          borderless
          v-model="serverValue"
          :options="serverOptions"
          label="Сервер"
          stack-label
          :loading="isLoadingServers"
        >
          <template v-slot:option="scope">
            <q-item v-bind="scope.itemProps">
              <q-item-section avatar>
                <div>
                  <country-flag :country="scope.opt.countryCode.toLowerCase()"/>
                </div>
              </q-item-section>
              <q-item-section>
                <q-item-label>{{ scope.opt.label }}</q-item-label>
              </q-item-section>
              <q-item-section side>
                <q-item-label>
                  ₽ {{ scope.opt.monthPrice.toFixed(2) }} мес
                </q-item-label>
              </q-item-section>
            </q-item>
          </template>
          <template v-slot:selected-item="scope" class="row items-center">
            <q-item-section avatar>
              <div>
                <country-flag :country="scope.opt.countryCode.toLowerCase()"/>
              </div>
            </q-item-section>
            <q-item-section>
              <q-item-label>{{ scope.opt.label }}</q-item-label>
            </q-item-section>
          </template>
        </q-select>
        <div class="q-py-sm">
          <div
            class="slider-label"
            :class="{ 'shake-animation': hasAmountError }"
          >
            Количество месяцев
          </div>
          <div class="row items-center q-mt-xs">
            <q-slider
              class="col-11 q-px-sm"
              v-model="monthValue"
              :min="0"
              :max="12"
              :class="{ 'slider-error': hasAmountError }"
            />
            <div class="col-1 text-center" style="color: var(--tg-accent-text-color); font-size: 17px; font-weight: 600">
              {{ monthValue }}
            </div>
          </div>
          <div style="height: 10px">
            <transition
            enter-active-class="animated fadeInDown"
            leave-active-class="animated fadeOutUp"
          >
            <div
              v-show="hasAmountError"
              class="slider-error-message"
            >
              <span>Недостаточно средств на балансе для оплаты!</span>
            </div>
          </transition>
          </div>
        </div>

      </div>
    </tg-section>

    <tg-section class="fixed-bottom">
      <div class="total-text q-px-md q-pt-sm q-pt-sm" style="font-weight: 500">
        Итого: {{amount.toFixed(2)}} ₽
      </div>
    </tg-section>

    <MainButton text="Приобрести" @click="addClientHandler"></MainButton>
  </q-page>

   <q-dialog
     persistent
     v-model="loadingDialog"
     backdrop-filter="blur(4px)"
   >
     <animated-banner v-if="loadingStatus" title="Добавление подписки..." path="stickers/LoadingDuckSticker.json"/>
     <animated-banner v-else-if="!loadingError" title="Подписка добавлена!" path="stickers/OkDuckSticker.json" :loop="false"/>
     <animated-banner v-else title="Ошибка добавления" path="stickers/NotFoundDuckSticker.json"/>
   </q-dialog>

</template>

<style scoped>

.shake-animation {
  animation: q-field-label 0.36s;
  animation-duration: 0.36s;
  animation-timing-function: ease;
  animation-delay: 0s;
  animation-iteration-count: 1;
  animation-direction: normal;
  animation-fill-mode: none;
  animation-play-state: running;
  animation-name: q-field-label;
  animation-timeline: auto;
  animation-range-start: normal;
  animation-range-end: normal;
}
.slider-error-message {
  height: 15px;
  font-size: 11px;
  line-height: 1;
  color: var(--q-negative);
  margin-left: 15px;
}
.slider-label {
  color: var(--tg-subtitle-text-color);
  font-weight: 600;
  font-size: 12px;
  line-height: 147%;
  letter-spacing: 0.01em;
  padding-left: 14px;
}

.fadeInDown {
  animation: fadeInDown 0.3s;
}
.fadeOutUp {
  animation: fadeOutUp 0.3s;
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-10px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeOutUp {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-10px); }
}

::v-deep(.q-field__label) {
  position: absolute;
  top: -4px;
  left: 8px;
  background: var(--tg-section-bg-color);
  padding: 0 6px;
  color: var(--tg-subtitle-text-color);
  font-weight: 600;
  font-size: 16px;
  line-height: 147%;
  letter-spacing: 0.01em;
  z-index: 10;
}
::v-deep(.q-field--focused .q-field__label) {
  color: var(--tg-accent-text-color);
}
::v-deep(.q-field__control) {
  border: 1.8px solid var(--tg-hint-color);
  border-radius: 14px;
  height: 50px;
}
::v-deep(.q-field--focused .q-field__control) {
  border-color: var(--tg-accent-text-color);
}
::v-deep(.q-field__native) {
  padding-top: 0 !important;
  padding-left: 14px;
  color: var(--tg-text-color);
  font-weight: 400;
  font-size: 16px;
  line-height: 150%;
  caret-color: var(--tg-accent-text-color);
}
::v-deep(.q-field__append) {
  color: var(--tg-subtitle-text-color);
  padding-top: 7px;
  padding-right: 10px;
}
::v-deep(.q-field--focused .q-field__append) {
  color: var(--tg-accent-text-color);
}
::v-deep(.q-field__bottom) {
  margin-left: 15px;
  padding-top: 5px;
}


::v-deep(.select .q-field__control .q-field__control-container){
  padding: 0;
}


::v-deep(.q-slider__selection) {
  background: var(--tg-accent-text-color);
}
::v-deep(.q-slider__thumb) {
  color: var(--tg-accent-text-color);
}

.total-text {
  font-size: 1.5rem;
  font-weight: 500;
  line-height: 2rem;
  letter-spacing: normal;
}
</style>
