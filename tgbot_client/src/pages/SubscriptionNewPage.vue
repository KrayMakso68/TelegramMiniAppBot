<script setup lang="ts">

import {BackButton, MainButton} from "vue-tg";
import TgSection from "components/TgSection.vue";
import {useRouter} from "vue-router";
import {ref} from "vue";

const router = useRouter();
const text = ref('')
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <MainButton text="хуй" @click="newPayment"></MainButton>

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
        <div class="q-mt-md q-pa-sm">
          <q-input
            type="text"
            clearable
            autofocus
            dense
            borderless
            v-model="text"
            label="Имя подключения"
            stack-label
          />

        </div>
      </tg-section>
    </div>

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
</style>
