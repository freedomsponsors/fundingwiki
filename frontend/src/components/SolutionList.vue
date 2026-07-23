<template>
    <div v-if="data_list.length > 0" style="width: 650px;">
        <div v-if="data_list.length == 1" class="page_section_title"><h2>1 Proposed solution</h2></div>
        <div v-else class="page_section_title"><h2>{{ data_list.length }} Proposed solutions</h2></div>
        <div>
            <div class="solution-item" v-for="(item, index) in data_list" :key="index">
                <div>
                    <div>{{ item.content }}</div>
                    <div class="solution-meta">
                        {{ item.createdByUser.username }}
                        <a v-if="item.if_mine" @click="handleEdit(item)" style="margin-left:10px">edit</a>
                    </div>
                </div>
                <div>
                    <SolutionCommentForm :solution="item" @submit-success="onSolutionCommentSubmitSuccess(item)"></SolutionCommentForm>
                </div>
                <div style="">
                    <SolutionCommentList :comment_list="item.techsolutioncomment_set" :refresh-flag="item.commentRefreshFlag"></SolutionCommentList>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import {getSolution} from '@/services/solution.js'
import SolutionCommentForm from '@/components/SolutionCommentForm.vue'
import SolutionCommentList from '@/components/SolutionCommentList.vue'

const data_list = ref([])
const emit = defineEmits(['edit-proposal'])

const props = defineProps({
    issue: {
        type: Object,
        required: true
    }
})
console.log(props.issue.id)

// onMounted(async ()=>{
//     data_list.value = await getSolution(props.issue.id)
// })

watch(() => props.issue.id, (newVal, oldVal) => {
    if (newVal) {
        getSolution(newVal).then((response) => {
            data_list.value = response
        })
    }
}, { deep: true })

let onSolutionCommentSubmitSuccess = async (targetItem)=>{
    getSolution(props.issue.id).then((response) => {
        data_list.value = response
    })
}

const handleEdit = (item) => {
    emit('edit-proposal', item)
}

</script>

<style scoped>
.solution-item {
    width: 100%;
    border-bottom: 1px solid #efefef;
    padding: 10px 0;
}
.page_section_title{
    border-bottom: 1px solid #ccc;
    margin-bottom: 10px;
    margin-top: 40px;
}
.solution-meta{
    text-align: right;
    color: #888;
}
</style>
