<script setup lang="ts">
import NotFoundBanner from "components/NotFoundBanner.vue";
import {onMounted, Ref, ref} from "vue";
import {PaymentService} from "src/api";
import {OperationType, Payment, PaymentStatus} from "src/api/types/paymentTypes";

const loading = ref<boolean>(true);
const paymentsGroups: Ref<Record<string, Payment[]> | [] | null> = ref<Record<string, Payment[]> | [] | null>(null);

const loadHistory = async () => {
  paymentsGroups.value = await PaymentService.getPaymentHistoryByDay()
  loading.value = false;
};

onMounted(loadHistory);
</script>

<template>
  <div>
    <q-list v-if="loading">
      <div class="text-subtitle2 tg-subtitle-text q-ml-md q-mt-md">
        <q-skeleton width="20%" type="text"/>
      </div>
      <template v-for="index in 5" :key="index">
        <q-item  v-ripple>
          <q-item-section avatar>
            <q-avatar>
              <q-skeleton type="QAvatar"/>
            </q-avatar>
          </q-item-section>

          <q-item-section>
            <q-item-label lines="1">
              <q-skeleton width="40%" type="text"/>
            </q-item-label>

          </q-item-section>

          <q-item-section side>
            <div class="text-subtitle2" style="width: 45px">
              <q-skeleton type="text"/>
            </div>
          </q-item-section>
        </q-item>
        <q-separator v-if="index < 5" inset="item" class="tg-separator"/>
      </template>
    </q-list>

    <q-list v-if="paymentsGroups">
      <div v-for="(payments, date) in paymentsGroups" :key="date">
        <div class="text-subtitle2 tg-subtitle-text q-ml-md q-mt-md">{{ date }}</div>
        <template v-for="(payment, index) in payments" :key="index">
          <q-item
            v-ripple
            draggable="false"
          >
            <q-item-section avatar>
              <q-avatar v-if="payment.operationType === OperationType.DEPOSIT" icon='east' font-size="25px" class="pay-deposit"/>
              <q-avatar v-else icon='west' font-size="25px" class="pay-withdrawal"/>
            </q-item-section>

            <q-item-section>
              <template v-if="payment.operationType === OperationType.DEPOSIT">
                <q-item-label lines="1">
                  Пополнение баланса
                </q-item-label>
              </template>
              <template v-else>
                <q-item-label lines="1">
                  Оплата
                </q-item-label>
                <q-item-label caption class="tg-subtitle-text">
                  {{ payment?.title }}
                </q-item-label>
              </template>
            </q-item-section>

            <q-item-section side>
              <template v-if="payment.status === PaymentStatus.COMPLETED" >
                <q-badge outline color="positive" label='Ок' />
              </template>
              <template v-else-if="payment.status === PaymentStatus.PENDING">
                <q-badge outline color="warning" label='Обработка' />
              </template>
              <template v-else>
                <q-badge outline color="negative" label='Ошибка' />
              </template>
            </q-item-section>

            <q-item-section side>
              <div class="text-subtitle1 text-weight-bold">{{ payment.amount }} ₽</div>
            </q-item-section>
          </q-item>
          <q-separator v-if="index < payments?.length - 1" inset="item" class="tg-separator" />
        </template>
        <q-separator class="tg-separator" />
      </div>
    </q-list>

    <not-found-banner v-else-if="!loading" title="Нет записей"/>

  </div>
</template>

<style scoped>
.pay-deposit {
  color: var(--tg-accent-text-color);
}
.pay-withdrawal {
  color: var(--tg-destructive-text-color);
}
</style>
