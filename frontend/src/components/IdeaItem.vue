<template>
    <div style="display: flex;">
        <div>
            <div style="display:flex;flex-direction: column;align-items: center;padding-right:10px;">
                <a :class="'vote_a ' + (idea.is_voted_up?'voted_link':'')" data-type="up" @click="ideaVote(idea.id, idea.vote_up_ope)" href="javascript:;">
                    <span class="las la-sort-up" style="font-size:26px;"></span>
                </a>
                <div class="vote_points">{{ idea.point }}</div>
                <a :class="'vote_a ' + (idea.is_voted_down?'voted_link':'')" data-type="down" @click="ideaVote(idea.id, idea.vote_down_ope)" href="javascript:;">
                    <span class="las la-sort-down" style="font-size:26px"></span>
                </a>
            </div>
            <div class="proposal_box" style="">
                <div style="font-size:16px;font-weight: bold;;">{{ idea.solution_count }}</div>
                <div style="color:#ccc">proposals</div>
            </div>
        </div>
        <div style="flex-grow: 1;padding-left: 10px;">
            
            <div v-if="idea.title != idea.description">
                <a @click="gotoIdeaDetail(idea.id)">{{ idea.title }}</a>
                <div style="margin-top: 5px;font-size: 14px;white-space: pre-wrap">{{ idea.description }}</div>
            </div>
            <div v-else><a @click="gotoIdeaDetail(idea.id)">{{ idea.title }}</a></div>
            <div class="idea_tags">
                <div class="tag_item" v-for="tag in idea.tags" :key="tag.id">
                    <div>{{ tag.title }}</div>
                    <div style="color:#999">{{ tag.description }}</div>
                </div>
            </div>
            <div style="display: flex;flex-direction: row-reverse;padding:8px 0">
                <a @click="getSimilar(idea.id)">Similar ideas</a>
                <div v-if="canDelete" style="margin-right: 10px;">
                    <a @click="editIdea(idea.id)" style="margin-right:10px">edit</a>
                    <a @click="deleteIdea(idea.id)">delete</a>
                </div>
                <div v-if="idea.createdByUser" style="margin-right: 10px;">{{ idea.createdByUser.username }}</div>
            </div>
            <div v-if="show_similar">
                <div v-for="idea_similar in similar_ideas_list" style="border-top: 1px solid #efefef;background-color: #efefef;">
                    <div style="padding: 10px;border-bottom: 1px solid #ccc;">{{ idea_similar.content }}</div>
                </div>
            </div>
        </div>
        <ConfirmDialog ref="confirmDialog" />
    </div>
</template>

<script setup lang="ts">
import { ref, defineEmits, watch} from 'vue'
import {deleteIdeaById, getSimilarIdeas, ideasVote, getIdeaById} from '@/services/ideas.js'
 
const confirmDialog = ref()

const props = defineProps<{ item: object, canDelete?: boolean }>()

const idea = ref(props.item)

watch(() => props.item, (newVal, oldVal) => {
  idea.value = props.item
})

const similar_ideas_list = ref([])
const show_similar = ref(false)
const emit = defineEmits(['delete-idea'])
import { useRouter } from 'vue-router'

const router = useRouter()

const getSimilar = async (id) => {
    show_similar.value = !show_similar.value

    if(similar_ideas_list.value.length == 0){
        similar_ideas_list.value = await getSimilarIdeas(id)
    }
}
const deleteIdea = async (id)=>{
    if(await confirmDialog.value.open('Are you sure to delete this idea?')){
        await deleteIdeaById(id)
        window.location.reload()
        // emit('delete-idea', id)
    }
}

const editIdea = (id) => {
    router.push({ path: '/issueadd', query: { editid: id } })
}

const ideaVote = async (id, vote_type)=>{

    let response = await ideasVote(id, vote_type)
    console.log(response)

    idea.value = await getIdeaById(id)
}

let gotoIdeaDetail = (id)=>{
    router.push({ name: 'Idea', params: { id } })
}

</script>

<style scoped>
.read-the-docs {
color: #888;
}
.idea_item{
    width: 100%;margin-top: 20px;border-bottom: 1px solid #efefef;
}
.vote_points {
    padding: 0 10px;
    font-size: 28px;
    line-height: 20px;
}
.voted_link span{
    color:#8DC63F
}
.proposal_box{
    border: 1px solid rgb(245, 130, 36);
    border-radius: 5px;
    padding: 5px;
    font-size: 14px;
    color: rgb(245, 130, 36);
    display:flex;flex-direction: column;align-items: center;
}
.idea_tags{
    display: flex;flex-wrap: wrap;margin-top: 10px;
    gap: 5px;
}
.tag_item{
    background-color: #efefef;
    padding: 5px 10px;
    border-radius: 5px;
}
</style>
  
