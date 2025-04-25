<script setup lang="ts">
import {onMounted, Ref, ref} from "vue";
import {Subscription} from "src/api/types/subscriptionTypes";
import {PanelService, SubscriptionService} from "src/api";
import AnimatedBanner from "components/AnimatedBanner.vue";

const loading  = ref<boolean>(true);
const subscriptionsByServer: Ref<Record<string, Subscription[]> | null> = ref<Record<string, Subscription[]> | null>(null);

const loadSubscriptions = async () => {
  subscriptionsByServer.value = await SubscriptionService.getUserSubscriptions();
  loading.value = false;
};

const updateSubscriptions = async () => {
  loading.value = true;
  let updateStatus = await PanelService.updateUserSubscriptions()
  if (updateStatus.status == "OK") {
    subscriptionsByServer.value = await SubscriptionService.getUserSubscriptions();
  } else {
    subscriptionsByServer.value = null
  }
  loading.value = false;
};

function formatDate(date: Date | null): string {
  return date ? new Date(date).toLocaleDateString() : "";
}

onMounted(loadSubscriptions);
</script>

<template>
  <q-list v-if="loading">
    <div class="server-header">
      <q-skeleton width="35%" type="text" class="text-subtitle1"/>
    </div>
    <template v-for="index in 3" :key="index">
      <q-item v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <q-skeleton type="circle" size="32px"/>
          </q-avatar>
        </q-item-section>

        <q-item-section>
          <q-item-label lines="1">
            <q-skeleton width="70%" type="text"/>
          </q-item-label>
          <q-item-label caption>
            <q-skeleton width="50%" type="text"/>
          </q-item-label>
        </q-item-section>

        <q-item-section side>
          <q-skeleton type="QBadge"/>
        </q-item-section>

        <q-item-section side top>
          <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
        </q-item-section>
      </q-item>
      <q-separator v-if="index < 3" inset="item" class="tg-separator"/>
    </template>
    <div class="q-pt-sm">
      <q-item
        v-for="index in 2" :key="index"
        v-ripple
        dense
        draggable="false"
        class="q-py-none"
      >
        <q-item-section avatar class="q-pl-sm">
          <q-skeleton type="circle" size="25px"/>
        </q-item-section>

        <q-item-section>
          <q-skeleton width="20%" type="text"/>
        </q-item-section>
      </q-item>
    </div>
  </q-list>

  <q-list v-else-if="subscriptionsByServer && Object.keys(subscriptionsByServer).length !== 0">
    <template v-for="(subscriptions, server) in subscriptionsByServer" :key="server">

      <div class="server-header">
        {{server}}
      </div>

      <template v-for="(subscription, index) in subscriptions" :key="subscription.email">
        <q-item
          :to="{
            path: 'connect-info',
            query: {
              name: subscription.name,
              email: subscription.email,
              serverId: subscription.serverId,
              url: subscription.url,
              unlimited: subscription.endDate === null
            }
          }"
          v-ripple
          draggable="false"
        >
          <q-item-section avatar class="tg-list-item-icon">
            <q-avatar icon='vpn_lock' font-size="24px"/>
          </q-item-section>

          <q-item-section>
            <q-item-label lines="1">{{ subscription.name }}</q-item-label>
            <q-item-label v-if="subscription.endDate" caption class="tg-subtitle-text">
              До: {{ formatDate(subscription.endDate) }}
            </q-item-label>
          </q-item-section>

          <q-item-section side>
            <template v-if="subscription.isActive && !subscription.endDate" >
              <q-badge outline color="amber-9" label='безлимит' />
            </template>
            <template v-else-if="!subscription.isActive">
              <q-badge outline color="red" label='истекло' />
            </template>
            <template v-else>
              <q-badge outline color="green" label='активно' />
            </template>
          </q-item-section>

          <q-item-section side>
            <q-avatar icon='navigate_next' class="tg-subtitle-text"/>
          </q-item-section>
        </q-item>
        <q-separator v-if="index < subscriptions?.length" inset="item" class="tg-separator" />
      </template>
    </template>
    <div class="tg-line-button q-pt-sm">
        <q-item
          dense
          clickable
          draggable="false"
          class="q-py-none"
          :to="'subscription-new'"
        >
          <q-item-section avatar>
            <q-avatar icon='add_circle' font-size="24px"/>
          </q-item-section>

          <q-item-section>
            <q-item-label>Добавить</q-item-label>
          </q-item-section>
        </q-item>
        <q-item
          dense
          clickable
          draggable="false"
          class="q-py-none"
          @click="updateSubscriptions"
        >
          <q-item-section avatar>
            <q-avatar icon='sync' font-size="24px"/>
          </q-item-section>

          <q-item-section>
            <q-item-label>Обновить</q-item-label>
          </q-item-section>
        </q-item>
      </div>
  </q-list>

  <animated-banner
    v-else-if="subscriptionsByServer && Object.keys(subscriptionsByServer).length === 0"
    title="Похоже, у вас нет подписок!"
    path="stickers/ResistanceDog.json"
  >
    <template #button>
      <div class="row q-gutter-sm">
        <q-btn class="col tg-btn" :to="'subscription-new'">Подключить</q-btn>
        <q-btn class="col tg-btn" @click="updateSubscriptions">Обновить</q-btn>
      </div>
    </template>
  </animated-banner>

  <animated-banner
    v-else
    title="Ошибка получения подписок ;("
    path="stickers/ResistanceDog.json"
  >
    <template #button>
      <q-btn class="tg-btn" @click="updateSubscriptions">Обновить</q-btn>
    </template>
  </animated-banner>

</template>

<style scoped>
.tg-list-item-icon {
  color: var(--tg-subtitle-text-color);
}
.tg-line-button {
  color: var(--tg-link-color);
}
.server-header {
  color: var(--tg-hint-color);
  font-size: 14px;
  font-weight: 500;
  line-height: 18px;
  padding: 5px 0 5px 16px;
}
</style>
