<template>
<div v-if="ideas_list.length > 0">
    <div style="width: 100%;margin-top: 60px;border-bottom: 1px solid #efefef;"><h3>My ideas</h3></div>
    <div style="width: 100%;">
        <div v-for="(idea, index) in ideas_list" :key="index" class="idea_item">
            <!-- <div>{{ idea.content }}</div> -->
            <IdeaItem :item="idea" @delete-idea="loadIdeas" :can-delete="true"></IdeaItem>
        </div>
    </div>
</div>

</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import {getIdeasMine} from '../services/ideas.js'

import IdeaItem from './IdeaItem.vue'

const ideas_list = ref([])
var loadIdeas = async ()=>{
    ideas_list.value = await getIdeasMine()
}
onMounted(loadIdeas)
</script>

<style scoped>
.read-the-docs {
    color: #888;
}
.issue_title{
    text-align: left;
}
.idea_item{
    width: 100%;margin-top: 20px;border-bottom: 1px solid #efefef;
}
</style>