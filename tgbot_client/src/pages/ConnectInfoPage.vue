<script setup lang="ts">
import {BackButton, MainButton} from "vue-tg";
import {useRouter} from "vue-router";
import {ConnectInfo} from "src/api/types/panelTypes";
import TgSection from "components/TgSection.vue";
import TgCodeCard from "components/TgCodeCard.vue";
import {Ref, ref} from "vue";
import {PanelService} from "src/api";


const router = useRouter();
// const {openLink} = useWebAppNavigation();

interface Props {
  name: string;
  email: string;
  serverId: number;
  url: string
}
const props = defineProps<Props>();

const connectInfo: Ref<ConnectInfo | null> = ref<ConnectInfo | null>(null)

const loadInfo = async () => {
  if (!connectInfo.value) {
    connectInfo.value = await PanelService.getConnectInfoByEmail(props.serverId, props.email)
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

// const importConfig = () => {
//   if (props.connectUrl) {
//     let encodedConfig = encodeURIComponent(props.connectUrl);
//     let configUrl = `hiddify://install-config?url=${encodedConfig}`;
//     console.log(configUrl)
//
//     openLink(configUrl);
//   }
// };
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
            {{name}}
          </div>
        </div>
        <div class="q-pa-sm">
          <tg-code-card title="Connection url" :text=url />
        </div>
<!--        <q-btn @click="importConfig">Импортировать</q-btn>-->
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
                  <div class="col-3">Имя :</div>
                  <div class="col">
                    <q-skeleton v-if="!connectInfo" height="21px" type="QChip" class="q-ma-xs"/>
                    <q-chip v-else dense :label="connectInfo.email" color="indigo" text-color="white" class="q-px-sm" style="max-width: 250px"/>
                  </div>
                </div>
                <div class="col row items-center">
                  <div class="col-3">Статус :</div>
                  <div class="col">
                    <q-skeleton v-if="!connectInfo" height="21px" width="40px" type="QChip" class="q-ma-xs"/>
                    <q-chip v-else-if="connectInfo.enable" label="active" dense color="green" text-color="white" class="q-px-sm"/>
                    <q-chip v-else label="disable" dense color="red" text-color="white" class=""/>
                  </div>
                </div>
                <div class="col row items-center">
                  <div class="col-3">Окончание:</div>
                  <div class="col">
                    <q-skeleton v-if="!connectInfo" height="21px" width="120px" type="QChip" class="q-ma-xs"/>
                    <q-chip v-else :label="datetimeToString(connectInfo.expiryTime)" dense color="red" text-color="white" class="q-px-sm"/>
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
    <MainButton text="Продлить подписку"/>
  </q-page>
</template>

<style scoped>

</style>
