<script setup lang="ts">
import {useRouter} from "vue-router";
import TgSection from "components/TgSection.vue";
import {BackButton, MainButton, useWebAppNavigation, useWebAppMainButton} from "vue-tg";
import {PaymentService} from "src/api";
import {computed, onMounted, ref, watchEffect} from "vue";
import {PaymentOption} from "src/api/types/paymentTypes";

const router = useRouter();
const {openLink} = useWebAppNavigation();
const {disableMainButton, enableMainButton} = useWebAppMainButton();


const inputValue = ref<number | null>(null);
const selectValue = ref<PaymentOption | null>(null);
const options = ref<PaymentOption[]>([]);
const isLoading = ref(true);


const loadPaymentOptions = async () => {
  options.value = await PaymentService.getPaymentOptions();
  isLoading.value = false;
};

const newPayment = async () => {
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
  } else {
    disableMainButton();
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
    <div class="q-gutter-y-md">
      <tg-section label="Новый платёж">
        <div class="q-mx-md q-mt-xl q-pb-lg">
          <div style="font-size: 16px;" class="tg-subtitle-text">Сумма пополнения</div>
          <q-input
            class="payment-input hide-spin-buttons"
            input-class="input"
            type="number"
            borderless
            clearable
            autofocus
            prefix="₽"
            mask="#.##"
            error-message="Cумма от 2₽ до 15000₽"
            :error="!isValid"
            v-model="inputValue"
          />

          <q-select
            v-model="selectValue"
            :loading="isLoading"
            :options="options"
            borderless
            dark
            class="payment-type"
            clearable
            label="Способ оплаты"
          />
        </div>

      </tg-section>
    </div>
  </q-page>
</template>

<style scoped>
.payment-input {
  font-size: 35px;
  caret-color: var(--tg-accent-text-color);
}

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
}

::v-deep(.payment-input .q-field__append) {
  color: var(--tg-subtitle-text-color);
}

::v-deep(.payment-input .q-field__bottom) {
  margin-left: 25px;
  padding-top: 0;
}


::v-deep(.payment-type .q-field__native) {
  font-size: 20px;
  color: var(--tg-accent-text-color);
  padding-left: 10px;
  padding-top: 4px;
  padding-bottom: 0;
}
::v-deep(.payment-type .q-field__label) {
  color: var(--tg-subtitle-text-color);
}
::v-deep(.payment-type .q-field__append) {
  color: var(--tg-subtitle-text-color);
  padding-top: 15px;
}
</style>
