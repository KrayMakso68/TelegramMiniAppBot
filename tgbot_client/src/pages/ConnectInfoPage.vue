<script setup lang="ts">
import {BackButton} from "vue-tg";
import {useRouter} from "vue-router";
import {Connect} from "src/api/types/subscribeTypes";
import {ConnectInfo} from "src/api/types/panelTypes";
import TgSection from "components/TgSection.vue";
import TgCodeCard from "components/TgCodeCard.vue";
import {Ref, ref} from "vue";
import {PanelService} from "src/api";

const router = useRouter();
const props = defineProps<Connect>();

const connectInfo: Ref<ConnectInfo | null> = ref<ConnectInfo | null>(null)

const loadInfo = async () => {
  if (!connectInfo.value) {
    connectInfo.value = await PanelService.getConnectInfoByEmail(props.email)
  }
};

function bytesToGB(bytes: number): number {
  const gigabytes = bytes / (1024 ** 3);
  return Math.round(gigabytes * 10) / 10;
}

function datetimeToString(dateTime: number): string {
  if (dateTime === 0) {
    return "unlimited"
  } else {
    const formatter = new Intl.DateTimeFormat('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric'
    });
    return formatter.format(dateTime);
  }
}
</script>

<template>
  <BackButton @click="() => router.back()"></BackButton>
  <q-page class="tg-text overflow-auto">
    <div class="q-gutter-y-md">
      <tg-section>
        <div class="q-pa-md">
          <div class="text-subtitle2" style="color: var(--tg-subtitle-text-color);">
            Подключение
          </div>
          <div class="text-h4 text-weight-bold" style="color: var(--tg-section-header-text-color);">
            {{email}}
          </div>
        </div>
        <div class="q-pa-sm">
          <tg-code-card title="Connection url" :text=connectUrl />
        </div>
      </tg-section>

      <tg-section>
        <q-expansion-item
          icon="query_stats"
          header-class="q-pl-lg"
          label="Подробная информация"
          @show="loadInfo"
        >
          <q-card style="background-color: var(--tg-section-bg-color);">
            <q-card-section>
              <div class="column text-no-wrap">

                <div class="col row items-center">
                  <div class="col-3">Name:</div>
                  <div class="col-auto">
                    <q-skeleton v-if="!connectInfo" height="21px" type="QChip" class="q-ma-xs"/>
                    <q-chip v-else dense color="teal" text-color="white" style="margin: 4px">
                      {{connectInfo.email}}
                    </q-chip>
                  </div>
                </div>
                <div class="col row items-center">
                  <div class="col-3">Active :</div>
                  <div class="col-auto">
                    <q-skeleton v-if="!connectInfo" height="21px" width="40px" type="QChip" class="q-ma-xs"/>
                    <q-chip v-else dense color="green" text-color="white">
                      {{connectInfo.enable}}
                    </q-chip>
                  </div>
                </div>
                <div class="col row items-center">
                  <div class="col-3">Expiry time:</div>
                  <div class="col-auto">
                    <q-skeleton v-if="!connectInfo" height="21px" width="120px" type="QChip" class="q-ma-xs"/>
                    <q-chip v-else dense color="red" text-color="white">
                      {{datetimeToString(connectInfo.expiryTime)}}
                    </q-chip>
                  </div>
                </div>

                <div class="col row items-center">
                  <div class="col-3">Download:</div>
                  <div class="col-3 q-pa-sm">
                    <q-circular-progress
                      v-if="!connectInfo"
                      indeterminate
                      rounded
                      size="50px"
                      color="blue"
                    />
                    <q-circular-progress
                      v-else
                      show-value
                      :value="bytesToGB(connectInfo.down)"
                      rounded
                      size="50px"
                      color="blue"
                    >
                      {{bytesToGB(connectInfo.down)}} GB
                    </q-circular-progress>
                  </div>
                  <div class="col-3">Upload:</div>
                  <div class="col-3 q-pa-sm">
                    <q-circular-progress
                      v-if="!connectInfo"
                      indeterminate
                      rounded
                      size="50px"
                      color="blue"
                    />
                    <q-circular-progress
                      v-else
                      show-value
                      :value="bytesToGB(connectInfo.up)"
                      rounded
                      size="50px"
                      color="blue"
                    >
                      {{bytesToGB(connectInfo.up)}} GB
                    </q-circular-progress>
                  </div>
                </div>
              </div>
              <div class="col row">

              </div>
              <div class="col row">

              </div>
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </tg-section>
    </div>
  </q-page>
</template>

<style scoped>

</style>
