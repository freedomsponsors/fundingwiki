<template>
<div>
    <User></User>
</div>
<div style="display: flex;align-items: center;margin-top: 50px;margin-bottom: 60px;flex-direction: column;">
    <div style="display: flex;flex-direction: column; align-items: center;width: 650px;gap: 20px;">
        <IssueForm :key="myIdeasKey" @submit-success="onSubmitSuccess"></IssueForm>
    </div>
</div>

<div style="display: flex;justify-content: space-around;margin-top: 20px;">
    <div>
        <div style="width: 650px;">
            <div class="page_section_title"><h2>Idea detail:</h2></div>
            <IdeaItem :item="idea" @delete-idea="onDeleteIdeas"></IdeaItem>
        </div>
        <SolutionList :issue="idea"></SolutionList>
        <div style="width: 650px;">
            <div class="page_section_title">
                <h2 v-if="idea.count_solution >= 0">{{ idea.count_solution === 0 ? 'Propose a solution' : 'Propose another solution' }}</h2>
            </div>
            <SolutionForm :issue="idea" @submit-success="onSolutionSubmitSuccess"></SolutionForm>
        </div>
    </div>
</div>
</template>

<script setup lang="ts">
import User from '@/components/User.vue'
import IssueForm from '@/components/IssueForm.vue'
import IdeaItem from '@/components/IdeaItem.vue'
import SolutionForm from '@/components/SolutionForm.vue'
import SolutionList from '@/components/SolutionList.vue'
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
let onSolutionSubmitSuccess = async ()=>{
    // Refresh the idea details after a new solution is submitted
    idea.value = await getIdeaById(ideaId)
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
.page_section_title{
    border-bottom: 1px solid #efefef;
    margin-bottom: 10px;
    margin-top: 20px;
}
</style>