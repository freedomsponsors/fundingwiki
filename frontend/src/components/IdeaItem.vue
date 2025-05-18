<template>
    <div>
        <div>{{ item.content }}</div>
        <div style="display: flex;flex-direction: row-reverse;">
            <a @click="getSimilar(item.id)">Samilar ideas</a>
            <div v-if="canDelete" style="margin-right: 10px;">
                <a @click="deleteIdea(item.id)">delete</a>
            </div>
            <div v-if="item.createdByUser" style="margin-right: 10px;">{{ item.createdByUser.username }}</div>
        </div>
        <div v-if="show_similar">
            <div v-for="idea_similar in similar_ideas_list" style="border-top: 1px solid #efefef;background-color: #efefef;">
                <div style="padding: 10px;border-bottom: 1px solid #ccc;">{{ idea_similar.content }}</div>
            </div>
        </div>
    </div>
    <ConfirmDialog ref="confirmDialog" />
</template>

<script setup lang="ts">
import { ref, defineEmits } from 'vue'
import {deleteIdeaById, getSimilarIdeas} from '../services/ideas.js'
 
const confirmDialog = ref()

defineProps<{ item: object, canDelete:false}>()

const similar_ideas_list = ref([])
const show_similar = ref(false)
const emit = defineEmits(['delete-idea'])

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

</script>

<style scoped>
.read-the-docs {
color: #888;
}
.idea_item{
    width: 100%;margin-top: 20px;border-bottom: 1px solid #efefef;
}
</style>
  