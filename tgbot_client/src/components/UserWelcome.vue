<script setup lang="ts">
import {UserService} from "src/api";
import {onMounted, ref} from "vue";
import {useWebApp} from "vue-tg";

const {initDataUnsafe} = useWebApp();
const avatarUrl = ref<string | null>(null);
const loadAvatar = async () => {
  avatarUrl.value = await UserService.getCurrentUserAvatar();
};

onMounted(loadAvatar);
</script>

<template>
  <transition name="jump-up" appear>
    <div class="text-h5 text-weight-medium">
      Привет,
    </div>
  </transition>
  <transition name="jump-right" appear>
    <div class="row items-center q-gutter-x-sm">
      <div class="text-h4">
        {{initDataUnsafe?.user?.first_name}}
      </div>
      <q-avatar v-if="avatarUrl" size="45px">
        <img :src="avatarUrl" alt="User Avatar" />
      </q-avatar>
      <q-skeleton v-else size="45px" type="QAvatar" />
    </div>
  </transition>
</template>

<style scoped>
.jump-up-enter-active {
  transition: transform 0.5s ease-in-out, opacity 0.5s;
}
.jump-up-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}
.jump-up-enter-to {
  transform: translateY(0);
  opacity: 1;
}
.jump-right-enter-active {
  transition: transform 0.6s ease-in-out, opacity 0.5s;
}
.jump-right-enter-from {
  transform: translateX(-100%);
  opacity: 0;
}
.jump-right-enter-to {
  transform: translateX(0);
  opacity: 1;
}
</style>
