<script setup lang="ts">
import NotFoundBanner from "components/NotFoundBanner.vue";
import {onMounted, Ref, ref} from "vue";
import {PaymentService} from "src/api";
import {Payment} from "src/api/types/paymentTypes";

const loading  = ref<boolean>(true);
const payments: Ref<Payment[] | null> = ref<Payment[] | null>(null);

const loadHistory = async () => {
  payments.value = await PaymentService.getPaymentHistory()
  loading.value = false;
};


onMounted(loadHistory);
</script>

<template>
  <q-slide-transition>
    <div>
      <q-list v-if="loading">
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
              <q-item-label caption>
                <q-skeleton width="20%" type="text"/>
              </q-item-label>
            </q-item-section>

            <q-item-section side>
              <div class="text-subtitle2">100₽</div>
            </q-item-section>
          </q-item>
          <q-separator v-if="index < 5" inset="item" class="tg-separator"/>
        </template>
      </q-list>

      <q-list v-else-if="payments && payments.length">
        <template v-for="(payment, index) in payments" :key="index">
          <q-item
            v-ripple
            draggable="false"
          >
            <q-item-section avatar class="tg-list-item-icon">
              <q-avatar icon='up' font-size="25px"/>
            </q-item-section>

            <q-item-section>
              <q-item-label lines="1">{{ payment.createdAt }}</q-item-label>
              <q-item-label caption class="tg-subtitle-text">
                {{ payment.operationType }}
              </q-item-label>
            </q-item-section>

<!--            <q-item-section side>-->
<!--              <template v-if="connect.active && !connect.remainingSeconds" >-->
<!--                <q-badge outline color="amber-9" label='unlimit' />-->
<!--              </template>-->
<!--              <template v-else-if="!connect.active">-->
<!--                <q-badge outline color="red" label='expired' />-->
<!--              </template>-->
<!--              <template v-else>-->
<!--                <q-badge outline color="green" label='active' />-->
<!--              </template>-->
<!--            </q-item-section>-->

            <q-item-section side>
              <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
            </q-item-section>
          </q-item>
          <q-separator v-if="index < payments?.length - 1" inset="item" class="tg-separator" />
        </template>
      </q-list>

      <not-found-banner v-else-if="payments" title="Похоже, у вас нет подписок!">
        <template #button>
          <q-btn class="tg-btn">Подключить</q-btn>
        </template>
      </not-found-banner>

      <not-found-banner v-else title="Ошибка получения подписок ;("/>
    </div>
  </q-slide-transition>
</template>

<style scoped>
.tg-list-item-icon {
  color: var(--tg-accent-text-color);
}
</style>
