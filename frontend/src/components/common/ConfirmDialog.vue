<template>
<v-dialog v-model="isOpen" persistent max-width="400">
    <v-card>
    <v-card-title class="text-h6">{{ title }}</v-card-title>
    <v-card-text>{{ message }}</v-card-text>

    <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click="handleCancel">Cancel</v-btn>
        <v-btn color="red" text @click="handleConfirm">Confirm</v-btn>
    </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script setup>
import { ref } from 'vue'

const isOpen = ref(false)
const title = ref('Confirm')
const message = ref('')
let resolveFn = null

// function open(confirmTitle, confirmMessage) {
function open(confirmMessage) {
//   title.value = confirmTitle
  message.value = confirmMessage
  isOpen.value = true

  return new Promise((resolve) => {
    resolveFn = resolve
  })
}

function handleConfirm() {
  isOpen.value = false
  resolveFn(true)
}

function handleCancel() {
  isOpen.value = false
  resolveFn(false)
}

defineExpose({ open })
</script>