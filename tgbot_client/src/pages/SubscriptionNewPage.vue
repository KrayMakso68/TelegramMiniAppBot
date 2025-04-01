<script setup lang="ts">

import {BackButton, MainButton} from "vue-tg";
import TgSection from "components/TgSection.vue";
import {useRouter} from "vue-router";
import {computed, onMounted, ref} from "vue";
import {Server} from "src/api/types/serverTypes";
import {ServerService} from "src/api";
import CountryFlag from 'vue-country-flag-next'

const router = useRouter();

const isLoadingServers = ref(true);
const inputValue = ref<string | null>(null);
const serverValue = ref<Server | null>(null);
const serverOptions = ref<Server[]>([{id: 0, label:"Не найдено", countryCode: "...", monthPrice: 0, isActive: false}]);
const monthValue = ref<number>(1)

const loadServerOptions = async () => {
  serverOptions.value = await ServerService.getServersInfo()
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
    return /^[A-Za-z0-9_-]+$/.test(val) || 'Только a-z, 0-9, - , _';
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

const inputErrorMessage = computed(() => {
  const messages = inputRules.value
    .map(rule => rule(inputValue.value))
    .filter(msg => typeof msg === 'string');
  return messages.join(' ; ');
});

onMounted(() => {
  loadServerOptions();

})
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>

  <q-page class="tg-text overflow-auto">

    <div class="q-gutter-y-md">
      <tg-section label="Новая подписка">
        <div class="q-mt-sm q-pa-sm">
          <q-input
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
