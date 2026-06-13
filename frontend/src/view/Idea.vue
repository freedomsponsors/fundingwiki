<template>
<div>
    <User></User>
</div>
<div style="display: flex;align-items: center;margin-top: 50px;margin-bottom: 100px;flex-direction: column;">
    <div style="display: flex;flex-direction: column; align-items: center;width: 650px;gap: 20px;">
        <IssueForm :key="myIdeasKey" @submit-success="onSubmitSuccess"></IssueForm>
    </div>
</div>

<div style="display: flex;justify-content: space-around;margin-top: 40px;">
    <div style="width: 650px;">
        <div style="border-bottom: 1px solid #efefef;margin-bottom: 10px;"><h2>Idea detail:</h2></div>
        <IdeaItem :item="idea" @delete-idea="onDeleteIdeas"></IdeaItem>
    </div>
</div>
</template>

<script setup lang="ts">
import User from '@/components/User.vue'
import IssueForm from '@/components/IssueForm.vue'
import IdeaItem from '@/components/IdeaItem.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getIdeaById } from '@/services/ideas.js'

const route = useRoute()
const ideaId = route.params.id

const idea = ref({})
onMounted(async ()=>{
    idea.value = await getIdeaById(ideaId)
})

let onDeleteIdeas = async ()=>{
    
}
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