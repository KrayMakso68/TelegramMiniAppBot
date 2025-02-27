<script setup lang="ts">
import NotFoundBanner from "components/NotFoundBanner.vue";
import {onMounted, Ref, ref} from "vue";
import {Subscription} from "src/api/types/subscriptionTypes";
import {SubscriberService} from "src/api";
import TgSection from "components/TgSection.vue";

const loading  = ref<boolean>(true);
const subscriptionsByServer: Ref<Record<string, Subscription[]> | null> = ref<Record<string, Subscription[]> | null>(null);

const loadSubscriptions = async () => {
  subscriptionsByServer.value = await SubscriberService.getUserSubscriptions();
  loading.value = false;
};


onMounted(loadSubscriptions);
</script>

<template>
  <q-slide-transition>
    <div>
<!--      <q-list v-if="loading">-->
<!--        <template v-for="index in 2" :key="index">-->
<!--          <q-item v-ripple>-->
<!--            <q-item-section avatar>-->
<!--              <q-avatar>-->
<!--                <q-skeleton type="QAvatar"/>-->
<!--              </q-avatar>-->
<!--            </q-item-section>-->

<!--            <q-item-section>-->
<!--              <q-item-label lines="1">-->
<!--                <q-skeleton width="40%" type="text"/>-->
<!--              </q-item-label>-->
<!--              <q-item-label caption>-->
<!--                <q-skeleton width="20%" type="text"/>-->
<!--              </q-item-label>-->
<!--            </q-item-section>-->

<!--            <q-item-section side top>-->
<!--                <q-avatar icon='navigate_next' class="tg-subtitle-text"/>-->
<!--            </q-item-section>-->
<!--          </q-item>-->
<!--          <q-separator v-if="index < 2" inset="item" class="tg-separator"/>-->
<!--        </template>-->
<!--      </q-list>-->

<!--      <q-list v-else-if="subscriptionsByServer && Object.keys(subscriptionsByServer).length !== 0">-->

      <q-list>
        <template v-for="(subscriptions, server) in subscriptionsByServer" :key="server">
          <tg-section :label=server custom-class="custom-tg-section-header">
            <template v-for="(subscription, index) in subscriptions" :key="subscription.email_name">
              <q-item
                :to="{
                      path: 'connect-info',
                      query: {
                        emailName: subscription.emailName,
                        serverId: subscription.serverId,
                        url: subscription.url
                      }
                     }"
                v-ripple
                draggable="false"
              >
                <q-item-section avatar class="tg-list-item-icon">
                  <q-avatar icon='vpn_lock' font-size="24px"/>
                </q-item-section>

                <q-item-section>
                  <q-item-label lines="1">{{ subscription.emailName }}</q-item-label>
<!--                  <q-item-label caption class="tg-subtitle-text">-->
<!--                    {{ subscription.emailName }}-->
<!--                  </q-item-label>-->
                </q-item-section>

                <q-item-section side>
                  <template v-if="subscription.isActive && !subscription.endDate" >
                    <q-badge outline color="amber-9" label='unlimit' />
                  </template>
                  <template v-else-if="!subscription.isActive">
                    <q-badge outline color="red" label='expired' />
                  </template>
                  <template v-else>
                    <q-badge outline color="green" label='active' />
                  </template>
                </q-item-section>

                <q-item-section side>
                  <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
                </q-item-section>
              </q-item>
              <q-separator v-if="index < subscriptions?.length - 1" inset="item" class="tg-separator" />
            </template>
          </tg-section>
        </template>

      </q-list>

<!--      <not-found-banner v-else-if="subscriptionsByServer && Object.keys(subscriptionsByServer).length === 0" title="Похоже, у вас нет подписок!">-->
<!--        <template #button>-->
<!--          <q-btn class="tg-btn">Подключить</q-btn>-->
<!--        </template>-->
<!--      </not-found-banner>-->

<!--      <not-found-banner v-else title="Ошибка получения подписок ;("/>-->
    </div>
  </q-slide-transition>
</template>

<style scoped>
.tg-list-item-icon {
  color: var(--tg-subtitle-text-color);
}
:deep(.custom-tg-section-header) {
  color: var(--tg-subtitle-text-color);
  font-size: 14px;
  font-weight: 500;
  line-height: 18px;
  padding-bottom: 5px;
}
</style>
