<script setup lang="ts">

import {BackButton, MainButton} from "vue-tg";
import TgSection from "components/TgSection.vue";
import {useRouter} from "vue-router";
import {computed, onMounted, ref} from "vue";
import {Server} from "src/api/types/serverTypes";
import {ServerService} from "src/api";

const router = useRouter();

const isLoadingServers = ref(true);
const textValue = ref<string | null>(null);
const serverValue = ref<Server | null>(null);
const serverOptions = ref<Server[] | null>(null);
const monthValue = ref<number>(1)

const loadServerOptions = async () => {
  serverOptions.value = await ServerService.getServersInfo()
  if (!serverOptions.value) {
    serverOptions.value = [{id: 1, label:"Не найдено", country_code: "...", month_price: 0, is_active: false}]
  }
  isLoadingServers.value = false;
};

const amount = computed(() => serverValue.value ? serverValue.value.month_price * monthValue.value : 0);

onMounted(() => {
  loadServerOptions();

})
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>

  <q-page class="tg-text overflow-auto">

    <div class="q-gutter-y-md">
      <tg-section label="Новая подписка">
<!--        <div class="q-mx-md q-mt-xl q-pb-lg">-->
<!--          <div style="font-size: 16px;" class="tg-subtitle-text">Сумма пополнения</div>-->
<!--          <q-input-->
<!--            class="payment-input hide-spin-buttons"-->
<!--            input-class="input"-->
<!--            type="number"-->
<!--            borderless-->
<!--            clearable-->
<!--            autofocus-->
<!--            prefix="₽"-->
<!--            mask="#.##"-->
<!--            error-message="Cумма от 2₽ до 15000₽"-->
<!--            :error="!isValid"-->
<!--            v-model="inputValue"-->
<!--          />-->
<!--          <q-separator class="tg-separator"></q-separator>-->
<!--          <q-select-->
<!--            v-model="selectValue"-->
<!--            :loading="isLoading"-->
<!--            :options="options"-->
<!--            borderless-->
<!--            dark-->
<!--            class="payment-type q-mt-sm"-->
<!--            clearable-->
<!--            label="Способ оплаты"-->
<!--          />-->
<!--        </div>-->
        <div class="q-mt-sm q-pa-sm">
          <q-input
            class="q-py-md"
            type="text"
            clearable
            autofocus
            dense
            borderless
            v-model="textValue"
            label="Имя подключения"
            stack-label
            error-message="Не более 10 символов"
            :error="!isValid"
          />
          <q-select
            class="select q-py-md"
            type="text"
            clearable
            dense
            borderless
            v-model="serverValue"
            :loading="isLoadingServers"
            :options="serverOptions"
            label="Сервер"
            stack-label
          />
          {{serverOptions}}
          <div class="q-py-sm">
            <div style="color: var(--tg-subtitle-text-color);font-weight: 600;font-size: 12px;
                line-height: 147%; letter-spacing: 0.01em; padding-left: 14px;">
              Количество месяцев
            </div>
            <div class="row items-center q-my-xs">
              <q-slider
                class="col-11 q-px-sm"
                v-model="monthValue"
                :min="0"
                :max="12"
              />
              <div class="col-1 text-center" style="color: var(--tg-accent-text-color); font-size: 17px; font-weight: 600">
                {{ monthValue }}
              </div>
            </div>
          </div>


        </div>
      </tg-section>

      <tg-section class="fixed-bottom">
        <div class="total-text q-px-md q-pt-sm q-pt-sm" style="font-weight: 500">
          Итого: {{amount}} ₽
        </div>
      </tg-section>

    </div>
    <MainButton text="Приобрести" @click=""></MainButton>
  </q-page>
</template>

<style scoped>
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
