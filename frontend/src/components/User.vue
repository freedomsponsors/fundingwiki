<template>
  <div style="display: flex;flex-direction: row-reverse;">
    <div v-if="login_info.logged_in == 1" style="display: flex;gap: 10px;">
      <div>{{ login_info.username }}</div>
      <div><a href="/logout">Login out</a></div>
    </div>
    <div v-else><a href="/login/">Login in</a></div>
  </div>

</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {getCurrentUserInfo} from '../services/user.js'

const login_info = ref({
  logged_in:0,
  username:''
})
onMounted(async ()=>{
  login_info.value = await getCurrentUserInfo()
})
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
