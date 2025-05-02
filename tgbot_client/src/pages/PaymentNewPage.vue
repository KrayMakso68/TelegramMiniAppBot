<script setup lang="ts">
import {useRouter} from "vue-router";
import TgSection from "components/TgSection.vue";
import {BackButton, MainButton, useWebAppNavigation, useWebAppMainButton, useWebAppHapticFeedback} from "vue-tg";
import {PaymentService} from "src/api";
import {computed, onMounted, ref, watchEffect} from "vue";
import {PaymentOption} from "src/api/types/paymentTypes";

const router = useRouter();
const {openLink} = useWebAppNavigation();
const {disableMainButton, enableMainButton} = useWebAppMainButton();
const {impactOccurred} = useWebAppHapticFeedback();


const inputValue = ref<number | null>(null);
const selectValue = ref<PaymentOption | null>(null);
const options = ref<PaymentOption[]>([]);
const isLoading = ref(true);


const loadPaymentOptions = async () => {
  options.value = await PaymentService.getPaymentOptions();
  isLoading.value = false;
};

const newPayment = async () => {
  impactOccurred('medium');
  let path = selectValue.value?.path
  let amount = inputValue.value;

  if (path && amount) {
    let url = await PaymentService.newPayment(path, amount);
    if (url) {
      openLink(url);

      window.addEventListener('focus', () => {
        router.push('/');
      }, { once: true });

    }
  }
};

watchEffect(() => {
  if (inputValue.value !== null && selectValue.value !== null && isValid.value) {
    enableMainButton();
    impactOccurred('light');
  } else {
    disableMainButton();
    impactOccurred('medium');
  }
});

const isValid = computed(() => inputValue.value && inputValue.value >= 2 && inputValue.value <= 15000)

onMounted(() => {
  disableMainButton();
  loadPaymentOptions();
});
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <MainButton text="PAY" @click="newPayment"></MainButton>
  <q-page class="tg-text overflow-auto">
      <tg-section label="Новый платёж">
        <div class="q-pa-sm q-mt-xl">
          <q-input
            class="payment-input hide-spin-buttons"
            label="Сумма пополнения"
            input-class="input"
            type="number"
            borderless
            clearable
            autofocus
            stack-label
            prefix="₽"
            mask="#.##"
            error-message="Cумма от 2₽ до 15000₽"
            :error="!isValid"
            v-model="inputValue"
          />
          <q-select
            class="payment-type q-pt-md"
            type="text"
            clearable
            dense
            borderless
            stack-label
            v-model="selectValue"
            :loading="isLoading"
            :options="options"
            label="Способ оплаты"
          />
        </div>

      </tg-section>
  </q-page>
</template>

<style scoped>
::v-deep(
.hide-spin-buttons input[type="number"]::-webkit-inner-spin-button,
.hide-spin-buttons input[type="number"]::-webkit-outer-spin-button
) {
  -webkit-appearance: none;
  margin: 0;
}

::v-deep(.hide-spin-buttons input[type="number"]) {
  -moz-appearance: textfield;
}

::v-deep(.input) {
  color: var(--tg-accent-text-color);
}

::v-deep(.payment-input .q-field__prefix) {
  color: var(--tg-subtitle-text-color);
  font-weight: 500;
  font-size: 35px;
  padding: 0 6px 0 10px;
}

::v-deep(.payment-input .q-field__append) {
  color: var(--tg-subtitle-text-color);
}

::v-deep(.payment-input .q-field__bottom) {
  margin-left: 25px;
  padding-top: 5px;
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
::v-deep(.payment-input .q-field__label) {
  top: -2px;
}
::v-deep(.q-field--focused .q-field__label) {
  color: var(--tg-accent-text-color);
}
::v-deep(.payment-input .q-field__control) {
  border: 1.8px solid var(--tg-hint-color);
  border-radius: 14px;
  height: 65px;
}
::v-deep(.payment-input .q-field__native) {
  padding: 0;
  color: var(--tg-accent-text-color);
  font-weight: 400;
  font-size: 35px;
  caret-color: var(--tg-accent-text-color);
}
::v-deep(.payment-type .q-field__control) {
  border: 1.8px solid var(--tg-hint-color);
  border-radius: 14px;
  height: 50px;
}
::v-deep(.q-field--focused .q-field__control) {
  border-color: var(--tg-accent-text-color);
}
::v-deep(.payment-type .q-field__native) {
  padding-bottom: 14px !important;
  padding-left: 14px;
  color: var(--tg-text-color);
  font-weight: 400;
  font-size: 18px;
  line-height: 100%;
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


::v-deep(.payment-type .q-slider__selection) {
  background: var(--tg-accent-text-color);
}
::v-deep(.payment-type .q-slider__thumb) {
  color: var(--tg-accent-text-color);
}
</style>
