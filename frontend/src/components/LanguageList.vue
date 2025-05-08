<template>
<ul>
    <li class="issue_title" v-for="(item, index) in data">
        <div>{{ index }} : {{ item }}</div>
    </li>
</ul>
<v-btn v-for="item in data">{{item}}</v-btn>    
</template>

<script setup lang="ts">
import { ref } from 'vue'

const el = document.getElementById('languages')
const data = ref(JSON.parse(el.textContent))

</script>

<style scoped>
.read-the-docs {
    color: #888;
}
.issue_title{
    text-align: left;
}
</style>
    