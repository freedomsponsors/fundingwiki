<template>
<ul>
    <li class="issue_title" v-for="issue in issueData">
        <div>{{ issue.title }}</div>
    </li>
</ul>
jjjjkkkk
change the template
8888888888888

<v-data-table :items="issueData"></v-data-table>

</template>

<script setup lang="ts">
import { ref } from 'vue'

const el_issues = document.getElementById('issues')
const issueData = ref(JSON.parse(el_issues.textContent))

</script>

<style scoped>
.read-the-docs {
  color: #888;
}
.issue_title{
    text-align: left;
}
</style>
