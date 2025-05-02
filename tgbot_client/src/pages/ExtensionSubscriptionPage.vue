<script setup lang="ts">

import TgSection from "components/TgSection.vue";
import {BackButton, MainButton, useWebAppMainButton, useWebAppHapticFeedback} from "vue-tg";
import {useRouter} from "vue-router";
import {computed, onMounted, ref, watchEffect} from "vue";
import {PanelService, ServerService, UserService} from "src/api";
import AnimatedBanner from "components/AnimatedBanner.vue";
import {ClientUpdate} from "src/api/types/panelTypes";

const router = useRouter();
const {enableMainButton, disableMainButton} = useWebAppMainButton();
const {impactOccurred, notificationOccurred} = useWebAppHapticFeedback();

interface Props {
  id: number,
  name: string,
  serverId: number
}
const props = defineProps<Props>();

const monthPrice = ref<number>(0);
const monthValue = ref<number>(1);
const userBalance = ref<number>(0);
const amount = computed(() => monthPrice.value * monthValue.value);
const loadingDialog = ref<boolean>(false);
const loadingStatus = ref<boolean>(true);
const loadingError = ref<boolean>(false);

const hasAmountError = computed(() => amount.value > userBalance.value)


const loadMonthPrice = async () => {
  let server = await ServerService.getServerInfoById(props.serverId);
  if (server) {
    monthPrice.value = server.monthPrice
  }
}

const loadBalance = async () => {
  userBalance.value = await UserService.getCurrentUserBalance();
};

const extendClient = async (): Promise<Record<string, string>> => {
  if (!hasAmountError.value && amount.value) {
    let data: ClientUpdate = {
      id: props.id,
      serverId: props.serverId,
      months: monthValue.value,
      price: amount.value
    }
    return await PanelService.updateClient(data);
  } else {
    return {'status': 'Error'};
  }
}

const extendClientHandler = async () => {
  loadingDialog.value = true;
  impactOccurred('light');
  let status = await extendClient();
  if (status.status === 'OK') {
    loadingStatus.value = false;
    notificationOccurred('success');
  } else {
    loadingStatus.value = false;
    loadingError.value = true;
    notificationOccurred('warning');
  }
  setTimeout(() => router.push('/'), 2000)
};

watchEffect(() => {
  if (monthValue.value && !hasAmountError.value && monthPrice.value) {
    enableMainButton();
    impactOccurred('light');
  } else {
    disableMainButton();
    impactOccurred('medium');
  }
});

onMounted(() => {
  loadBalance();
  loadMonthPrice();

})
</script>

<template>

  <BackButton @click="() => router.back()"></BackButton>

  <q-page class="tg-text overflow-auto">

    <tg-section label="Продление подписки">
      <div class="q-pa-md">
        <div class="text-subtitle2" style="color: var(--tg-subtitle-text-color);">
          Подключение
        </div>
        <div class="text-h5 text-weight-bold" style="color: var(--tg-section-header-text-color);">
          {{name}}
        </div>
      </div>
      <div class="q-py-sm">
        <div
          class="slider-label"
          :class="{ 'shake-animation': hasAmountError }"
        >
          Количество месяцев
        </div>
        <div class="row items-center q-mt-xs q-px-sm">
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

    </tg-section>

    <tg-section class="fixed-bottom">
      <div class="total-text q-px-md q-pt-sm q-pt-sm" style="font-weight: 500">
        Итого: {{amount.toFixed(2)}} ₽
      </div>
    </tg-section>

  </q-page>

  <MainButton text="Продлить" @click="extendClientHandler"></MainButton>

  <q-dialog
     persistent
     v-model="loadingDialog"
     backdrop-filter="blur(4px)"
   >
     <animated-banner v-if="loadingStatus" title="Обновление подписки..." path="stickers/LoadingDuckSticker.json"/>
     <animated-banner v-else-if="!loadingError" title="Подписка обновлена!" path="stickers/OkDuckSticker.json" :loop="false"/>
     <animated-banner v-else title="Ошибка обновления" path="stickers/NotFoundDuckSticker.json"/>
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
