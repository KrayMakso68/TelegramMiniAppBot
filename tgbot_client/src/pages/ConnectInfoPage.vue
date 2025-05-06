<script setup lang="ts">
import {BackButton, MainButton, useWebAppHapticFeedback} from "vue-tg";
import {useRouter} from "vue-router";
import {ClientDelete, ClientInfo} from "src/api/types/panelTypes";
import TgSection from "components/TgSection.vue";
import TgCodeCard from "components/TgCodeCard.vue";
import {Ref, ref} from "vue";
import {PanelService} from "src/api";
import AnimatedBanner from "components/AnimatedBanner.vue";
import TgInlineBtn from "components/TgInlineBtn.vue";


const router = useRouter();
const {notificationOccurred, impactOccurred} = useWebAppHapticFeedback();
// const {openLink} = useWebAppNavigation();

interface Props {
  id: number;
  name: string,
  email: string,
  serverId: number,
  url: string,
  unlimited: boolean,
  isActive: boolean
}
const props = defineProps<Props>();

const connectInfo: Ref<ClientInfo | null> = ref<ClientInfo | null>(null)

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

const showDialog = ref<boolean>(false);
const confirmDialog = ref<boolean>(true);
const loadingStatus = ref<boolean>(false);
const loadingError = ref<boolean>(false);

const deleteClient = async (): Promise<Record<string, string>> => {
  if (props.id) {
    let data: ClientDelete = {
      id: props.id,
      serverId: props.serverId,
      protocol: "vless",
    }
    return await PanelService.deleteClient(data);
  } else {
    return {'status': 'Error'};
  }
}

const openDialog = () => {
  showDialog.value = true;
  impactOccurred('light');
}

const deleteClientHandler = async () => {
  confirmDialog.value = false;
  loadingStatus.value = true;
  impactOccurred('light');
  let status = await deleteClient();
  if (status.status === 'OK') {
    loadingStatus.value = false;
    notificationOccurred('success');
  } else {
    loadingStatus.value = false;
    loadingError.value = true;
    notificationOccurred('error');
  }
  setTimeout(() => router.push('/'), 2000)
};

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
            </q-card-section>
          </q-card>
        </q-expansion-item>
      </tg-section>

      <tg-section v-if="!props.isActive">
        <q-item
          dense
          clickable
          draggable="false"
          class="q-py-none close-btn"
          @click="openDialog"
        >
          <q-item-section avatar>
            <q-avatar icon='close' font-size="28px"/>
          </q-item-section>

          <q-item-section class="q-pl-sm">
            <q-item-label>Удалить подписку</q-item-label>
          </q-item-section>
        </q-item>
      </tg-section>

    </div>
    <MainButton
      :visible="!props.unlimited"
      @click="router.push({
            path: 'subscription-extension',
            query: {
              id: props.id,
              name: props.name,
              serverId: props.serverId
            }
      });"
      text="Продлить подписку"/>
  </q-page>

  <q-dialog
    persistent
    v-model="showDialog"
    backdrop-filter="blur(5px)"
  >
    <div v-if="confirmDialog">
      <animated-banner title="Удалить подписку?" path="stickers/DeleteDuckSticker.json"/>
      <div class="row justify-around">
        <tg-inline-btn label="Отмена" icon="close" class="col" v-close-popup/>
        <tg-inline-btn label="Удалить" icon="delete" class="col" @click="deleteClientHandler"/>
      </div>
    </div>
<!--    <animated-banner v-if="!confirmDialog && loadingStatus" title="Удаление подписки..." path="stickers/LoadingDuckSticker.json"/>-->
<!--    <animated-banner v-else-if="!confirmDialog && !loadingError" title="Подписка удалена!" path="stickers/OkDuckSticker.json" :loop="false"/>-->
<!--    <animated-banner v-else title="Ошибка удаления" path="stickers/NotFoundDuckSticker.json"/>-->
  </q-dialog>

</template>

<style scoped>
.close-btn {
  color: var(--tg-destructive-text-color);
}
</style>
