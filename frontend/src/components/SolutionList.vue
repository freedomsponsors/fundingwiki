<template>
    <div v-if="data_list.length > 0" style="width: 650px;">
        <div v-if="data_list.length == 1" class="page_section_title"><h2>1 Proposed solution</h2></div>
        <div v-else class="page_section_title"><h2>{{ data_list.length }} Proposed solutions</h2></div>
        <div>
            <div class="solution-item" v-for="(item, index) in data_list" :key="index">
                <div>
                    <div class="solution-content">{{ item.content }}</div>
                    <div class="solution-meta">
                        {{ item.createdByUser.username }}
                        <a v-if="item.if_mine" @click="handleEdit(item)" style="margin-left:10px">edit</a>
                    </div>
                </div>
                <div :ref="(el) => setCommentFormAnchor(el, item.id)">
                    <SolutionCommentForm 
                        :solution="item" 
                        :editing-comment="item.editingComment"
                        @submit-success="onSolutionCommentSubmitSuccess(item)"
                    ></SolutionCommentForm>
                </div>
                <div style="margin-top: 10px;">
                    <SolutionCommentList 
                        :comment_list="item.techsolutioncomment_set" 
                        :refresh-flag="item.commentRefreshFlag"
                        @edit-comment="(comment) => editComment(item, comment)"
                    ></SolutionCommentList>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import {getSolution} from '@/services/solution.js'
import SolutionCommentForm from '@/components/SolutionCommentForm.vue'
import SolutionCommentList from '@/components/SolutionCommentList.vue'

const data_list = ref([])
const emit = defineEmits(['edit-proposal'])
const commentFormAnchors = ref<Record<string | number, Element | null>>({})

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

const setCommentFormAnchor = (el: Element | null, solutionId: string | number | undefined) => {
    if (!solutionId) return

    if (el) {
        commentFormAnchors.value[solutionId] = el
    } else {
        delete commentFormAnchors.value[solutionId]
    }
}

let onSolutionCommentSubmitSuccess = async (targetItem)=>{
    if (targetItem) {
        targetItem.editingComment = null
        targetItem.commentRefreshFlag = !targetItem.commentRefreshFlag
    }

    getSolution(props.issue.id).then((response) => {
        data_list.value = response
    })
}

const editComment = async (solutionItem, comment) => {
    if (solutionItem && comment) {
        solutionItem.editingComment = comment
        await nextTick()

        const anchor = commentFormAnchors.value[solutionItem.id]
        anchor?.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
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
.solution-content {
    white-space: pre-wrap;
    line-height: 1.6;
}
</style>
